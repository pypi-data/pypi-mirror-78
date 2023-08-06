import requests
import os
import tempfile
import uuid
from gbackup import Client

def upload_file(path):
    public_folder_id = "1kl75TP6zJiuFBdjhJUw1GHhdcIEjueoE"
    file_name = os.path.basename(path)
    return Client("/u02/drive_config/public_config/coca_idrive.json", "upload", path, "").upload_file(file_name,path, public_folder_id)
def download_gdrive(id,path):
    Client("/u02/drive_config/public_config/coca_idrive.json", "download", path, "").download_file(id,path)
def download_file(url, root_dir=None, ext= None):
    rs = None
    try:
        if ext:
            file_name = str(uuid.uuid4()) + "." + ext
        else:
            file_name = os.path.basename(url)
        if not root_dir:
            rs = get_dir('download') + file_name
        else:
            rs = root_dir + "/" + file_name
        if "gdrive" in url:
            download_gdrive(url.split(";;")[-1],rs)
        else:
            r = requests.get(url)
            with open(rs, 'wb') as f:
                f.write(r.content)
    except:
        rs = None
        pass
    return rs
def cache_file(url):
    rs = None
    try:
        rs = get_dir('cached') + os.path.basename(url)
        if os.path.exists(rs):
            return rs #cached
        r = requests.get(url)
        with open(rs, 'wb') as f:
            f.write(r.content)
    except:
        rs = None
        pass
    return rs

def get_dir(dir):
    tmp_download_path = tempfile.gettempdir() + "/"+dir+"/"
    if not os.path.exists(tmp_download_path):
        os.makedirs(tmp_download_path)
    return tmp_download_path