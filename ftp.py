import ftplib
 
ftp = ftplib.FTP("tedcharlesbrown.synology.me")
ftp.login("anonymous", "ftplib-example-1")
ftp.cwd("/Application_Installers")

files = []
folders = []
 
tree = []

ftp.dir(tree.append)

# Print the list of files
for branch in tree:
    # Split the line by whitespace
    elements = branch.split()
    # The file name is the last element
    parsed_name = elements[-1]
    if branch.startswith('d'):
        folders.append(parsed_name)
        # print(f"{file_name} is a directory")
    else:
        files.append(parsed_name)
        # print(f"{file_name} is a file")

# file = files[0]

file_to_search = "ARTNETominator"

for file in files:
    if file.lower().find(file_to_search.lower()) != -1:
        # Download the file
        with open(file, 'wb') as f:
            ftp.retrbinary(f'RETR {file}', f.write) 


 
ftp.quit()