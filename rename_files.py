import os

curr_user = os.environ.get('USERNAME')
mydir = "\\\\?\\C:\\Users\\" + curr_user + "\\Desktop\\"
foldername = "3 Leistungserbringung"
##foldername = "New Folder"

maxlen = 230
maxfolderlen = 100

currfolder = mydir + foldername
# could parallelize but whatever
for dirpath, dirnames, filenames in os.walk(currfolder):
##    print(dirpath) ## current directory (relative path to beginning of walk)
##    print(dirnames) ## list of folders in current directory
##    print(filenames) ##list of files in current directory
    
    # if folder is too long, reduce to first x characters
##    if len(dirpath) > maxlen:
##        currfolder = os.path.basename(dirpath)
##        newfolder = dirpath[:len(dirpath) + maxfolderlen - len(currfolder)]
##        try:
##            os.rename(dirpath,newfolder)
##            print(f"renamed {dirpath} to {newfolder}")
##        except FileExistsError:
##            # if same file exists multiple times, rename
##            os.rename(dirpath,newfolder + "(2)")
##            print(f"renamed {dirpath} to {newfolder}")
##        
##        dirpath = newfolder 
            
    for filename in filenames:
        currfile = dirpath + "\\" + filename
        if len(currfile) > maxlen:
            currfilename, file_extension = os.path.splitext(filename)
            newfilename = currfile[:maxlen-5] + file_extension
            try:
                os.rename(currfile,newfilename)
                print(f"renamed {currfile} to {newfilename}{file_extension}")
            except FileExistsError:
                # if same file exists multiple times, rename
                if currfilename[-1] == ")":
                    copycount = currfilename[:-1].split("(")[-1]
                    print(copycount)
                    try:
                        copycount = int(copycount)
                        copycount += 1
                    except:
                        copycount = 1
                else:
                    copycount = 1
                print(copycount)
                newfilename = currfile[:maxlen-5]+ "(" + str(copycount) + ")" + file_extension
                os.rename(currfile,newfilename)
                print(f"renamed {currfile} to {newfilename}")
                
                
    
