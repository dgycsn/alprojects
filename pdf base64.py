import os

curr_user = os.environ.get('USERNAME')
mydir = "C:/Users/" + curr_user +"/Documents/"
os.chdir(mydir)

import base64

# Example doc
contcontent = ""

# Decode
pdf_data = base64.b64decode(contcontent)

# Save to file
##with open("output.docx", "wb") as f:
##    f.write(pdf_data)
##
##print("PDF saved as output.pdf")
