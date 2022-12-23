import requests
from bs4 import BeautifulSoup
import json

download = {
    "free_file_sync": ["https://freefilesync.org/download.php","https://www.dropbox.com/s/kr0b297r12hmx86/sublime_text_build_4143_x64_setup.exe?dl=1"],

    "midi_ox": ["http://www.midiox.com/zip/midioxse.exe","https://www.dropbox.com/s/uzehscuf3t0c4p7/midioxse.exe?dl=1"]
}

# specify the url
ffs_download_url = 'https://freefilesync.org/download.php'
parsec_download_url = "https://builds.parsec.app/package/parsec-windows.exe"
# myFFmpeg_download_url = "https://www.myffmpeg.com/myFFmpegsetup64bit.exe"
myFFmpeg_download_url = "https://www.myffmpeg.com/download.html"
netSetMan_download_url = "https://www.netsetman.com/en/freeware"
# rufus_github_url = ["pbatard","rufus"]
rufus_download_url = "https://rufus.ie/en/"
sublime_download_url = "https://www.sublimetext.com/"
tailscale_download_url = "https://tailscale.com/download/"
tightvnc_download_url = "https://www.tightvnc.com/download.php"
realvnc_download_url = "https://www.realvnc.com/en/connect/download/viewer/windows/"
rename_download_url = "https://www.bulkrenameutility.co.uk/Download.php"
putty_download_url = "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html"
github_download_url = "https://desktop.github.com"
disugise_download_url = "https://download.disguise.one/"
artnetominator_download_url = "https://www.lightjams.com/artnetominator/artnetominator.msi"
midiox_download_url = "http://www.midiox.com/zip/midioxse.exe"
protokol_download_url = "https://hexler.net/protokol"


def parse_html_for_link(download_url: list):
    # find the index of the character immediately after the "://" substring
    index_start = download_url[0].find("://") + 3
    # find the index of the first "/" character that appears after index_start
    index_end = download_url[0].find("/",index_start)
    # extract the base URL of the website from the download_url string
    base_url = download_url[0][:index_end]

    # send a request to the website
    response = requests.get(download_url[0])

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
    

    # print(html)

    # find the index of the character immediately after the "http" substring
    index_start = download_link.rfind("http")

    if index_start == -1 or index_start < download_link.rfind(" "):
        index_start = download_link.rfind("href=") + 6
        # extract the download name from the html string
        download_name = html[index_start:index_end]
        # concatenate the base URL and the download name to create the full download link
        download_link = base_url + download_name
        # print("DIRECT LINK NOT GIVEN, USING BASE")
        # print(index_start,download_name)
    else:
        # extract the download name from the html string
        download_link = html[index_start:index_end]

    try:
        print("STATUS CODE", requests.get(download_link).status_code)

        # return the result of the request_download function
        print(f"DOWNLOADING FROM: {download_link}")
        return download_link

    except:
        print("getting from dropbox")
        return download_url[1]


def get_github(filename: str, owner: str, repo: str):
    # define the URL of the GitHub releases page
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    # send a request to the GitHub API to get the latest release
    response = requests.get(url)

    # check the status code of the response
    if response.status_code == 200:
        # parse the JSON data
        data = json.loads(response.text)
        # get the URL of the .exe file
        exe_url = data['assets'][0]['browser_download_url']

        get_download(filename,exe_url)

def get_download(file_name: str, download_link: list):
    print(f"DOWNLOADING: {file_name}")

    response = requests.get(parse_html_for_link(download_link), stream=True)

    if response.status_code == 200:
        # get the total size of the file
        total_size = int(response.headers.get('content-length', 0))
        # initialize a variable to store the number of bytes downloaded so far
        downloaded = 0
        # initialize a variable to store the last progress that was printed
        last_progress = -1
        
        with open(file_name,'wb') as f:
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
    
    

# ---------------------------------------------------------------------------- #
#                                  NOT WORKING                                 #
# ---------------------------------------------------------------------------- #


# get_download("BulkRenameUtility.exe",rename_download_url)
# get_download("Putty.msi",putty_download_url)
# get_download("github.exe",github_download_url)
# get_download("disguise.exe",disugise_download_url)

# ---------------------------------------------------------------------------- #
#                                    WORKING                                   #
# ---------------------------------------------------------------------------- #
# get_download("myFFmpeg.exe",myFFmpeg_download_url)
# get_download("FreeFileSync.exe",ffs_download_url)
# get_download("NetSetMan.exe",netSetMan_download_url)
# get_download("Rufus.exe",rufus_download_url)
# get_download("TightVNC.msi",tightvnc_download_url)
# get_download("RealVNC.exe",realvnc_download_url)
# get_download("protokol.exe",protokol_download_url)



# ---------------------------------------------------------------------------- #
#                                DIRECT DOWNLOAD                               #
# ---------------------------------------------------------------------------- #
# get_download("Artnetominator.msi",artnetominator_download_url)
# get_download("Parsec.exe",parsec_download_url) 
# get_download("midiox.exe",download["midi_ox"])


# ---------------------------------------------------------------------------- #
#                                 FROM DROPBOX                                 #
# ---------------------------------------------------------------------------- #
# get_download("FreeFileSync.exe",download["free_file_sync"])




