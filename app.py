import os
import urllib.request

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.constants import BLACK_SRC
from utils.database import Database
from utils.folder import (PICTURE_FOLDER, check_folder_distribution,
                          get_folder_by_generation, get_path_by_generation)

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
ROOT_FOLDER = os.getenv('ROOT_FOLDER')
OS = os.getenv('OS_DESCRIPTION')

check_folder_distribution()

db = Database()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# create webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
wait = WebDriverWait(driver, 45)

# get openai website
driver.get("https://labs.openai.com/auth/login")

# get elements
driver.implicitly_wait(25)
email_input = driver.find_element(By.CLASS_NAME, 'input')
email_input.send_keys(EMAIL)

email_submit_div = driver.find_element(By.CLASS_NAME, 'c8b8a7e41')
email_submit_button = driver.find_element(By.CSS_SELECTOR,'button')
email_submit_button.submit()

driver.implicitly_wait(25)
password_input = driver.find_element(By.ID, 'password')
password_input.send_keys(PASSWORD)

password_submit_div = driver.find_element(By.CLASS_NAME, 'c8b8a7e41')
password_submit_button = driver.find_element(By.CSS_SELECTOR,'button')
password_submit_button.submit()

CURRENT_GENERATION = db.get_current_generation()

for generation_index, generation in enumerate(range(CURRENT_GENERATION, 3)):

    source_path = get_path_by_generation(generation)
    current_generation_folder = get_folder_by_generation(generation)
    next_generation_path = get_path_by_generation(generation+1)
    
    if CURRENT_GENERATION<=0:
        file_list = os.listdir(source_path)
        db.load_initial_data(file_list)
        
        CURRENT_GENERATION = db.get_current_generation()
        
    file_list = db.get_current_pictures(CURRENT_GENERATION)
    for index, picture in enumerate(file_list):
        
        driver.implicitly_wait(25)
        upload_picture = driver.find_element(By.CSS_SELECTOR, "span[role = 'button']")
        upload_picture.click()

        pyautogui.write(' ', interval=0.25)
        
        if index or generation_index:
            if OS =='Windows':
                pyautogui.hotkey('alt','up')
            else:
                pyautogui.hotkey('command', 'up')
        else:
            pyautogui.write(ROOT_FOLDER) 
            pyautogui.press('enter')
            
            pyautogui.write(PICTURE_FOLDER) 
            pyautogui.press('enter')

        pyautogui.write(current_generation_folder) 
        pyautogui.press('enter')

        pyautogui.write(picture[0]) 
        pyautogui.press('enter')

        driver.implicitly_wait(25)
        modal_dialog = driver.find_element(By.CLASS_NAME, 'modal-dialog')
        modal_section = modal_dialog.find_elements(By.CLASS_NAME, 'crop-modal-section')[-1]
        crop_button  = modal_section.find_elements(By.CSS_SELECTOR, 'button')[0]
        crop_button.click()

        driver.implicitly_wait(25)
        modal_dialog = driver.find_element(By.CLASS_NAME, 'modal-dialog')
        modal_section = modal_dialog.find_elements(By.CLASS_NAME, 'crop-modal-section')[-1]
        crop_button  = modal_section.find_elements(By.CSS_SELECTOR, 'button')[-1]
        crop_button.click()

        driver.implicitly_wait(25)
        grid_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'task-page-generations-grid')))

        generated_images = grid_element.find_elements(By.CLASS_NAME,'generated-image')

        for index, image in enumerate(generated_images):
            img = image.find_element(By.TAG_NAME,'img')
            img_src = BLACK_SRC
            picture_name = picture[0].split('.')[0]
            while img_src == BLACK_SRC:
                img_src = img.get_attribute('src')


            urllib.request.urlretrieve(img_src, next_generation_path / f"{picture_name}-{index+1}.png")
            db.insert_new_picture(f"{picture_name}-{index+1}.png",CURRENT_GENERATION+1)

        driver.implicitly_wait(25)
        db.update_picture(picture[0], 1)

        driver.get('https://labs.openai.com/')
        
        driver.implicitly_wait(25)
