import win32com.client
import os
# no module named pywintypes error:
# https://www.youtube.com/watch?v=ClGNW7_lxc4


# configure
TARGET_SENDER = "licensing@fabasoft.com"
curr_user = os.environ.get('USERNAME')
SAVE_PATH = "C:/Users/" + curr_user + "/Downloads/"

# connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)   # 6 = Inbox

# get items, sort by ReceivedTime (descending = newest first)
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)

# process the last 20 emails
count = 0
message = messages.GetFirst()

while message and count < 20:
    try:
        sender = getattr(message, "SenderEmailAddress", None)
        if sender and sender.lower() == TARGET_SENDER.lower():
            print(f"Matched email from: {sender}, Subject: {message.Subject}")

            for att in message.Attachments:
                newtitle = att.FileName.split("(")[-1]
                newtitle = newtitle.split(")")[0]
                newtitle += ".license"
                file_path = os.path.join(SAVE_PATH, newtitle)
                print(f"   Saving attachment: {newtitle}")
                att.SaveAsFile(file_path)

        count += 1
        message = messages.GetNext()

    except Exception as e:
        print("Error reading message:", e)
        message = messages.GetNext()
