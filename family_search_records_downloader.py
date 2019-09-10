import os
import requests
import json
import errno
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = '/usr/bin/google-chrome'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def request(driver):
    s = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        s.cookies.set(cookie['name'].encode("utf-8").replace('"', ''), cookie['value'].encode("utf-8").replace('"', ''))
    return s

def login(driver):
    login_url = "https://www.familysearch.org/auth/familysearch/login?fhf=true&returnUrl=%2F&ldsauth=false"
    driver.get(login_url)
    user_name = driver.find_element_by_name("userName").send_keys('ing.pereira')
    password = driver.find_element_by_name("password").send_keys('movilnet')
    driver.find_element_by_tag_name("form").submit()

def get_image_id(list, index):
    return list[index].split('/')[-2]

def get_record_payload(list, index_image, catalog, folder):
    ark_image_id = get_image_id(list, index_image)
    return {
      "type": "image-data",
      "args": {
        "imageURL": "https://www.familysearch.org/dz/v1/" + ark_image_id,
        "state": {
          "i": str(index_image),
          "cat": catalog,
          "imageOrFilmUrl": "/ark:/" + folder + "/" + ark_image_id,
          "catalogContext": catalog,
          "viewMode": "i",
          "selectedImageIndex": index_image
        },
        "locale": "en"
      }
    }

def get_images_list(req, authToken, dgsNum, catalog):
    json_params = {
      "type": "film-data",
      "args": {
        "dgsNum": dgsNum,
        "state": {
          "cat": catalog,
          "catalogContext": catalog,
          "viewMode": "i",
          "selectedImageIndex": -1
        },
        "locale": "en",
        "sessionId": authToken,
        "loggedIn": True
      }
    }
    results = req.post(
        "https://www.familysearch.org/search/filmdatainfo",
        json = json_params,
        headers = {
        "referer": temp_url,
        "authorization": "Bearer " + authToken,
        "origin": "https://www.familysearch.org",
        "accept": "application/json, application/json",
        "content-type": "application/json"
        }
    )
    response = json.loads(results.content)
    list = response['images']
    return list

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
temp_url = "https://www.familysearch.org/ark:/61903/3:1:3Q9M-CSDK-YSS2-K"

login(driver)

driver.get(temp_url)

waitForRecordToLoad = WebDriverWait(driver, 10)
waitForRecordToLoad.until(expected_conditions.visibility_of_element_located((By.XPATH, "//canvas")))

authToken = driver.get_cookie("fssessionid")["value"]
req = request(driver)

catalog = "990690"
dgsNum = "007979779"
folder = "61903"
records_download_folder = os.getcwd() + '/' + dgsNum + "_" + catalog + "_" + folder

make_sure_path_exists(records_download_folder)

list = get_images_list(req, authToken, dgsNum, catalog)

for i in range(1036, 1182):
    print("Downloading record " + str(i) + " ...")
    record_payload = get_record_payload(list, i-1, catalog, folder)
    record_results = req.post(
        "https://www.familysearch.org/search/filmdatainfo",
        json = record_payload,
        headers = {
        "referer": temp_url,
        "authorization": "Bearer " + authToken,
        "origin": "https://www.familysearch.org",
        "accept": "application/json, application/json",
        "content-type": "application/json"
        }
    )

    record = json.loads(record_results.content)

    url = record['meta']['links']['image-stream-image-dist']['href']
    download_file = records_download_folder + "/" + str(i) + "_" + get_image_id(list, i-1) + ".jpg"
    image = req.get(url)

    with open(download_file, 'wb') as f:
        f.write(image.content)

driver.close()
