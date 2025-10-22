import os
import re
import time
import random
import requests
from folder_structure import list_tree

# wiki does not allow api calls w/o user agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
headers = {
    "User-Agent": user_agent
}

# curr_user = os.environ.get('USERNAME')
# rootdir = "C:/Users/" + curr_user + "/Downloads/"
rootdir = "C:\\"

folder = "repository"

repository_names = ["Physics","History","Marketing", "Sales", "Technology"]

random.seed(1)
errors = []
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
    for i in range(10):
        try:
            r = requests.get(url, params=params, headers=headers)
            return r.json()["query"]["categorymembers"]
        except Exception as e:
            errors.append(str(e) + str(i))
            time.sleep(1)
    return []

base = 0.8
max_depth = 3
downloaded_pages = set()
visited_categories = set()
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
    
    # retry 10 times to create folder
    for i in range(10):
        try:
            os.makedirs(newroot, exist_ok = True)
            break
        except Exception as e:
            errors.append(str(e) + str(i))
            time.sleep(1)
            continue

    if not os.path.exists(newroot): return
    
    # if no new folder can be created, save pages
    if recursion > max_depth or random.random() > base**recursion or categories == []:
        pages = get_category_members(folder, cmtype="page")
        
        for page in pages:
            title = page["title"]
            if title in downloaded_pages:
                continue
            downloaded_pages.add(title)
            filename = (newroot + parse_title(title))[:250] + ".txt"
            text = get_wiki_page(title)
            
            # retry 10 times to write file
            for i in range(10):
                try:
                    with open(filename , "w", encoding="utf-8") as f:
                        f.write(text)
                        f.close()
                        break
                except Exception as e:
                    errors.append(str(e) + str(i))
                    time.sleep(1)
                    continue
        return

    
    # otherwise create new folders
    for cat in categories:
        if cat in visited_categories:
            continue
        visited_categories.add(cat)
        newcategories = get_category_members(cat, "subcat")
        titles = [c["title"].split("Category:")[-1] for c in newcategories]
        
        # Now pick a random subset of 3–20
        k = random.randint(min(3, len(titles)), min(20, len(titles)))
        picked = random.sample(titles, k)
        
        create_folders(newroot, cat, picked, recursion + 1)
        
        
def get_wiki_page(title):
    """ 
    for a given title, get page as string 
    """ 
    url = "https://en.wikipedia.org/w/api.php" 
    params = { 
        "action": "query", 
        "prop": "extracts", 
        "explaintext": True, 
        "titles": title, 
        "format": "json" } 
    r = requests.get(url, params=params, headers=headers).json() 
    page = next(iter(r["query"]["pages"].values())) 
    return page.get("extract", "")


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
