from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
import time
from PIL import Image

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


PATH = "C:\\Users\\ADMIN\\Desktop\\scraping\\chromedriver.exe"

wd = webdriver.Chrome(PATH, options=options)

def get_img(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scroll(0, document.body.scrollHeight);")
        time.sleep(delay)
    
    url = "https://www.google.com/search?q=tzuyu&sxsrf=AOaemvLl2OVm6bX2OoRV0RKsq1RtZpMUhA:1641129216624&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiryfLfkpP1AhXeSmwGHZ7_AfMQ_AUoAXoECAEQAw&biw=1536&bih=754&dpr=1.25#imgrc=SrQjj8PGk5I4bM"
    wd.get(url)
    
    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips: max_images]:
            try:
                img.click()
                time.sleep(delay)
            
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f'Found {len(image_urls)}')
    
    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
        
        print("NOICE")
    except Exception as e:
        print("FAILED -", e)

urls = get_img(wd, 1, 10)

for i, url in enumerate(urls):
    download_image("img/", url, str(i) + ".jpg")

wd.quit()

