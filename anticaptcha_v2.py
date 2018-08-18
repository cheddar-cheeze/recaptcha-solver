from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import shutil
import cv2
from tensorflow_dir import label_image

def solve():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", "167.249.181.228")
    profile.set_preference("network.proxy.http_port", 8080)
    profile.update_preferences()
    browser = webdriver.Firefox(firefox_profile=profile)
    browser.delete_all_cookies()
    browser.get('http://localhost:5000')
    iframe = browser.find_element_by_tag_name('iframe')
    iframe.click()
    browser.switch_to_frame(1)
    bs = BeautifulSoup(browser.page_source, 'html.parser')
    rows = bs.find_all('tr')
    classifier = bs.find('strong')
    print( "What we're looking for:" + str(classifier.string))
    height = len(list(rows))
    width = len(list(rows[0].children))
    img = bs.find('img')
    response = requests.get(img.get('src'), stream=True)
    if response.status_code == 200:
        with open('captchas/full_captcha.jpg', 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
            f.close()
    captcha = cv2.imread('captchas/full_captcha.jpg')
    img_height, img_width = captcha.shape[:2]
    crop_y = img_height // height
    crop_x = img_width // width
    for index, val in enumerate(rows):
        for index2, val2 in enumerate(rows[0].children):
            cv2.imwrite('captchas/captcha_cropped' + str(index) + str(index2) + '.jpg', captcha[crop_y*index:(index+1)*crop_y, crop_x*index2:(index2+1)*crop_x])
            label_image.main('../captchas/captcha_cropped' + str(index) + str(index2) + '.jpg')
    browser.quit()
solve()