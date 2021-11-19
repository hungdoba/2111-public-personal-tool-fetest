import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

#############################
# Get request to website
#############################

save_path = r'C:\Users\PC3020\Desktop\new'

quotation_data = []

class data:
    request_main_path= 'https://www.fe-siken.com/kakomon/'
    request_year=''
    request_path = ''

    def full_path(self):
        return self.request_main_path+self.request_year+self.request_path

def get_url():
    for y in range(13, 31):
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

def save_html(content, request_year, request_path):
    try:
        path = request_year.replace("/","") + "-" + request_path
        file = open(os.path.join(save_path,path),'w')
        file.write(content)
        file.close()
    except ValueError:
        print (ValueError)

def download(url, pathname):
    pathname = os.path.join(pathname,"img")
    if not os.path.isdir(pathname):
        os.makedirs(pathname)  

    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
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

        #print(answers[1].prettify())
        save_html(str(answers[1]), data.request_year, data.request_path);

        images = answers[1].find_all("img");

        for image in images:
            image_url = image.attrs.get("src")
            if image_url:
                file_path = data.request_main_path + data.request_year + image_url
                download(file_path, save_path)

    else:
        print("not has data at: " + data.request_path)


get_url()

for data in quotation_data:
    download_all_data(data)
    print(data.full_path())

#test = data()
#test.request_main_path='https://www.fe-siken.com/kakomon/'
#test.request_year='15_haru/'
#test.request_path='q5.html'
#download_all_data(test)
#print(test.full_path())
