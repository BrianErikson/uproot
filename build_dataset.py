import os.path
import io
import pathlib
import glob
import requests
import zipfile
import pandas

BUILD_DIR = './build'
INDEX_URL = 'http://s.idigbio.org/idigbio-downloads/3f37324f-a860-4686-998c-9f6f37c50408.zip'


def get_record(uri, extract_path):
    file_prefix = uri.split('?')[0].split('/')[-1]
    search_path = pathlib.Path(extract_path, file_prefix)
    glob_list = glob.glob(f'{search_path}*')
    if len(glob_list) < 1:
        response = requests.get(uri, allow_redirects=True)
        file_name = response.url.split('/')[-1]
        file_path = pathlib.Path(extract_path, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"{glob_list[0]} already exists.")


def get_data():
    data_dir = pathlib.Path(BUILD_DIR, "dataset")
    extract_path = pathlib.Path(data_dir, 'multimedia')
    csv_path = pathlib.Path(data_dir, "multimedia.csv")

    if len(os.listdir(extract_path)) >= 1e+5:
        return

    if not os.path.exists(csv_path):
        os.makedirs(data_dir, exist_ok=True)
        response = requests.get(INDEX_URL)
        with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        print("Downloaded dataset index")

    os.makedirs(extract_path, exist_ok=True)

    df = pandas.read_csv(csv_path)

    uris = df['ac:accessURI'].tolist()
    for uri in uris:
        get_record(uri, extract_path)


if __name__ == '__main__':
    get_data()
