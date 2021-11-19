import os
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

#############################
# Get request to website
#############################

save_path = 'C://Users//PC3010//Desktop//new//'

quotation_data = []

period = 0

class data:
    request_main_path= 'https://www.fe-siken.com/kakomon/'
    request_year=''
    request_path = ''

    def full_path(self):
        return self.request_main_path+self.request_year+self.request_path

def get_url():
    for y in range(1, 31):
        year = str(y)+'_aki/'
        for question in range(1, 81):
            new_data = data()
            new_data.request_year = year
            new_data.request_path = 'q'+str(question)+'.html'
            if new_data.full_path() != None:
                quotation_data.append(new_data)

        year = str(y)+'_haru/'
        for question in range(1, 81):
            new_data = data()
            new_data.request_year = year
            new_data.request_path = 'q'+str(question)+'.html'
            if new_data.full_path() != None:
                quotation_data.append(new_data)

def save_html(content, data):
    try:
        path = save_path + data.request_year;
        if not os.path.isdir(path):
            os.makedirs(path)  

        file_name = path + data.request_path

        file = open(file_name,'w')
        file.write(content)
        file.close()
    except ValueError:
        print (ValueError)

def download(url, data):
    path = save_path + data.request_year + "img";
    if not os.path.isdir(path):
        os.makedirs(path)  

    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(path, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def download_all_data(data):
    request_full_path = data.full_path()
    r = requests.get(request_full_path)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')

        answers = soup.find_all("div",{"class":"ansbg"})

        save_html(str(answers[1]), data);

        images = answers[1].find_all("img");

        for image in images:
            image_url = image.attrs.get("src")
            if image_url:
                file_path = data.request_main_path + data.request_year + image_url
                download(file_path, data)

    else:
        print("not has data at: " + data.request_path)


get_url()

for data in quotation_data:
    if period >= 500:
        print("sleep 5s")
        time.sleep(5)
        period = 0
    else:
        download_all_data(data)
        print(data.full_path())
        period = period + 1

#test = data()
#test.request_main_path='https://www.fe-siken.com/kakomon/'
#test.request_year='15_haru/'
#test.request_path='q5.html'
#download_all_data(test)
#print(test.full_path())
