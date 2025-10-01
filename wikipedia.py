import os
import re
import random
import requests
from folder_structure import list_tree
from bs4 import BeautifulSoup

# wiki does not allow api calls w/o user agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
headers = {
    "User-Agent": user_agent
}

# curr_user = os.environ.get('USERNAME')
# rootdir = "C:/Users/" + curr_user + "/Downloads/"
rootdir = "C:\\"

folder = "repository"

repository_names = ["History","Marketing", "Sales"]

random.seed(2)
#%%

def get_category_members(category, cmtype="page|subcat", limit=50):
    """
    returns all pages and subcategories of a given category
    e.g. https://en.wikipedia.org/wiki/Category:Physics

    Parameters
    ----------
    category : category, e.g. "Pyhsics"
    cmtype : get whatever is under the given category
    limit : return first x entries
    """
    
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": limit,  # set high (max 500)
        "cmtype": cmtype,
        "format": "json"
    }
    r = requests.get(url, params=params, headers=headers)
    return r.json()["query"]["categorymembers"]

base = 0.8
max_depth = 5
def create_folders(root, folder, categories, recursion = -1):
    """
    recursively create nested folders

    Parameters
    ----------
    root : root directory
    folder : foldername to be created
    categories : categories to download from wiki
    recursion : recursion level, useful to limit nesting
    """
    newroot = root + folder + "\\"
    if len(newroot) > 255:
        return
    
    if not os.path.exists(newroot):
        try:
            os.makedirs(newroot)
        except:
            return
    
    # if no new folder can be created, save pages
    if recursion > max_depth or random.random() > base**recursion or categories == []:
        pages = get_category_members(folder, cmtype="page")
        
        for page in pages:
            title = page["title"]
            filename = (newroot + parse_title(title))[:250] + "_.txt"
            text = get_wiki_text_with_equations(title)
            try:
                with open(filename , "w", encoding="utf-8") as f:
                    f.write(text)
                    f.close()
            except:
                continue
        return

    
    # otherwise create new folders
    for cat in categories:
        newcategories = get_category_members(cat, "subcat")
        titles = [c["title"].split("Category:")[-1] for c in newcategories]
        
        # Now pick a random subset of 3–20
        k = random.randint(min(3, len(titles)), min(20, len(titles)))
        picked = random.sample(titles, k)
        
        create_folders(newroot, cat, picked, recursion + 1)
        
        
def get_wiki_text_with_equations(title):
    """
    Get Wikipedia page text as plain string, but preserve equations
    using their original LaTeX ($...$).
    
    Parameters
    ----------
    title : title of page
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json"
    }
    r = requests.get(url, params=params, headers= headers)
    r.raise_for_status()
    data = r.json()

    # Parse HTML
    html = data["parse"]["text"]["*"]
    soup = BeautifulSoup(html, "html.parser")

    # Replace <math> with its original LaTeX (from <annotation>)
    for m in soup.find_all("math"):
        annotation = m.find("annotation", {"encoding": "application/x-tex"})
        if annotation:
            latex = annotation.get_text()
            m.replace_with(f"${latex}$")
        else:
            # fallback: keep MathML text if no TeX source
            m.replace_with(f"${m.get_text()}$")

    # Extract plain text
    text = soup.get_text()
    return text


def parse_title(title, replacement = "_"):
    """
    Replace characters not allowed in Windows filenames
    
    Parameters
    ----------
    title : title of document
    replacement: char to replace forbidden characters
    """
    # Forbidden characters: \ / : * ? " < > |
    forbidden = r'[\\/:*?"<>|]'
    safe = re.sub(forbidden, replacement, title)

    # Remove trailing dots or spaces
    safe = safe.rstrip(" .")
    return safe
    
    
#%%

create_folders(rootdir, folder, repository_names)         

# print folder tree at the end
list_tree(rootdir + folder, False, sort = False)
