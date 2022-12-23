import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import ftplib
from timeout import timeout
from menu import MENU_version

@dataclass
class APPLICATION:
    name: str
    link: str

free_file_sync = APPLICATION("FreeFileSync.exe","https://freefilesync.org/download.php")
parsec = APPLICATION("Parsec.exe","https://builds.parsec.app/package/parsec-windows.exe")
midi_ox = APPLICATION("Midi-Ox.exe","http://www.midiox.com/zip/midioxse.exe")
myffmpeg = APPLICATION("myFFmpeg.exe","https://www.myffmpeg.com/download.html")
netsetman = APPLICATION("NetSetMan.exe","https://www.netsetman.com/en/freeware")
rufus = APPLICATION("Rufus.exe","https://rufus.ie/en/")
sublime = APPLICATION("Sublime.exe","https://www.sublimetext.com/")
tailscale = APPLICATION("Tailscale.exe","https://tailscale.com/download/")
tightvnc = APPLICATION("TightVNC.msi","https://www.tightvnc.com/download.php")
realvnc = APPLICATION("RealVNC.exe","https://www.realvnc.com/en/connect/download/viewer/windows/")
artnetominator = APPLICATION("Artnetominator.msi", "https://www.lightjams.com/artnetominator/artnetominator.msi")
protokol = APPLICATION("Protokol.exe","https://hexler.net/protokol")
bulk_rename_utility = APPLICATION("BulkRenameUtility.exe","https://www.bulkrenameutility.co.uk/Download.php")
obs = APPLICATION("OBS-Studio.exe","https://obsproject.com/download")
disguise = APPLICATION("d3.exe", "False")
ndi = APPLICATION("NDI-Tools.exe","https://www.ndi.tv/tools/#download-tools")
github = APPLICATION("Github.exe","https://central.github.com/deployments/desktop/desktop/latest/win32")


def download_from_archive(file_to_search: str):
    print("DOWNLOADING FROM ARCHIVE")
    file_found = False

    ftp = ftplib.FTP("tedcharlesbrown.synology.me")
    ftp.login("anonymous", "ftplib-example-1")
    ftp.cwd("/Application_Installers")

    files = ftp.nlst()

    versions = 0
    m_versions = MENU_version("Download Versions", "MULTIPLE VERSIONS FOUND, WHICH VERSION TO DOWNLOAD")

    for file in files:
        if file.lower().find(file_to_search.lower()[:-4]) != -1:
            file_to_download = file
            file_found = True
            m_versions.add_option(file)
            versions += 1

    if file_found:
        if versions > 1:
            m_versions.enter()
            file_to_download = m_versions.wait_for_input()
        # Download the file
        with open("applications/"+file_to_download, 'wb') as f:
            print(f"FOUND {file_to_download} FROM ARCHIVE, PLEASE WAIT")
            ftp.retrbinary(f'RETR {file_to_download}', f.write) 
            print("DOWNLOAD COMPLETE")
        
    else:
        print("NOT IN ARCHIVE")

    ftp.quit()
    
def parse_html_for_link(app: APPLICATION, verbose: bool):

    # print(type(app))
    if type(app) == str:
        link = app
    else:
        link = app.link

    if ".exe" in link or ".msi" in link:
        download_link = link
    else:
        # find the index of the character immediately after the "://" substring
        index_start = link.find("://") + 3
        # find the index of the first "/" character that appears after index_start
        index_end = link.find("/",index_start)
        # extract the base URL of the website from the download_url string
        base_url = link[:index_end]

        # send a request to the website
        response = requests.get(link)

        # parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # convert the parsed HTML content to a string and encode it as UTF-8
        html = str(soup.prettify().encode('utf-8'))
        
        # find the index of the character immediately after the ".exe" substring
        index_end = -1
        if html.find(".exe") != -1:
            index_end = html.find(".exe") + 4
        elif html.find(".msi") != -1:
            index_end = html.find(".msi") + 4

        # extract the download link from the html string
        download_link = html[:index_end]

        # find the index of the character immediately after the "http" substring
        index_start = download_link.rfind("http")

        if index_start == -1 or index_start < download_link.rfind(" "):
            if verbose:
                print("DIRECT LINK NOT GIVEN, USING BASE")
            index_start = download_link.rfind("href=") + 6
            # extract the download name from the html string
            download_name = html[index_start:index_end]
            # concatenate the base URL and the download name to create the full download link
            download_link = base_url + download_name
            
            # print(index_start,download_name)
        else:
            # extract the download name from the html string
            download_link = html[index_start:index_end]

    try:
        requests.get(download_link).status_code
        # return the result of the request_download function
        if verbose:
            print(f"DOWNLOADING FROM: {download_link}")
        return download_link
    except:
        return False


# def get_github(filename: str, owner: str, repo: str):
#     # define the URL of the GitHub releases page
#     url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

#     # send a request to the GitHub API to get the latest release
#     response = requests.get(url)

#     # check the status code of the response
#     if response.status_code == 200:
#         # parse the JSON data
#         data = json.loads(response.text)
#         # get the URL of the .exe file
#         exe_url = data['assets'][0]['browser_download_url']

#         get_download(filename,exe_url)

def download_from_web(response, app):

    if type(app) == str:
        name = app
    else:
        name = app.name

    if ".exe" in response.url or ".msi" in response.url:
        index_start = response.url.rfind("/")
        name = response.url[index_start:]
    elif response.headers.get("Content-Disposition"):
        # Get the value of the Content-Disposition header
        content_disposition = response.headers.get("Content-Disposition")
        # Split the value by ";" to get a list of key-value pairs
        index_start = content_disposition.find("filename=") + 10
        name = content_disposition[index_start:-1]


        # print(response.url)

    if response.status_code == 200:
        # get the total size of the file
        total_size = int(response.headers.get('content-length', 0))
        # initialize a variable to store the number of bytes downloaded so far
        downloaded = 0
        # initialize a variable to store the last progress that was printed
        last_progress = -1
        
        with open("applications/"+name,'wb') as f:
            for data in response.iter_content(chunk_size=4096):
                # update the number of bytes downloaded
                downloaded += len(data)
                # write the data to the file
                f.write(data)
                # check if the total size is known
                if total_size > 0:
                    # calculate the download progress as a percentage
                    progress = int(downloaded / total_size * 100)
                    # only print the progress if it is a multiple of 10 and if it is different from the last progress that was printed
                    if progress % 10 == 0 and progress != last_progress:
                        print(f'Download progress: {progress}%')
                        last_progress = progress
    else:
        print("Error downloading file:", response.status_code)

def get_download(app: APPLICATION, archive: bool):
    print(f"DOWNLOADING: {app.name[:-4]}")

    if app.link == "False" or archive:
        pass
    elif parse_html_for_link(app, False):
        response = requests.get(parse_html_for_link(app, True), stream=True)
        download_from_web(response, app)
        return
    download_from_archive(app.name)
        
def custom_download(link: str):
    if parse_html_for_link(link, False):
        response = requests.get(parse_html_for_link(link, True), stream=True)
        download_from_web(response, "custom.exe")
    else:
        print("COULD NOT FETCH DOWNLOAD")

# ---------------------------------------------------------------------------- #
#                                  NOT WORKING                                 #
# ---------------------------------------------------------------------------- #



get_download(github, False)

# get_download(disguise)

# ---------------------------------------------------------------------------- #
#                                    WORKING                                   #
# ---------------------------------------------------------------------------- #
# custom_download("https://freefilesync.org/download.php")
# get_download("myFFmpeg.exe",myFFmpeg_download_url)
# get_download("NetSetMan.exe",netSetMan_download_url)
# get_download("Rufus.exe",rufus_download_url)

# get_download(free_file_sync)
# get_download(tailscale)
# get_download(tightvnc)
# get_download(realvnc)
# get_download(protokol)
# get_download(obs, False)
# get_download(ndi, False)

# ---------------------------------------------------------------------------- #
#                                DIRECT DOWNLOAD                               #
# ---------------------------------------------------------------------------- #
# get_download("Artnetominator.msi",artnetominator_download_url)
# get_download(parsec) 
# get_download("applications/midiox.exe",download["midi_ox"])


# ---------------------------------------------------------------------------- #
#                                 FROM DROPBOX                                 #
# ---------------------------------------------------------------------------- #
# get_download(bulk_rename_utility)



