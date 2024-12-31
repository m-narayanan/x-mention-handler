from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

def login_to_twitter(driver, email, username, password):
    driver.get("https://x.com/login")
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
    email_field.send_keys(email)
    next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Next"]')))
    next_button.click()
    time.sleep(1)
    try:
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        username_field.send_keys(username)
        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Next"]')))
        next_button.click()
        time.sleep(1)
    except:
        print("Username field not found, moving to password entry")
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys(password)
    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Log in"]')))
    login_button.click()
    time.sleep(5)
    print("Logged into Twitter successfully!")

def get_mentions(driver):
    driver.get("https://x.com/notifications/mentions")
    time.sleep(5)
    mentions = []
    try:
        mentions_containers = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='cellInnerDiv']")))
        for container in mentions_containers:
            try:
                user_link_element = container.find_element(By.XPATH, ".//a[contains(@href,'/status')]")
                tweet_id = user_link_element.get_attribute('href').split('/')[-1]
                user_element = container.find_element(By.XPATH, ".//span[contains(text(),'@')]")
                user_name = user_element.text
                if user_name != f"@{os.getenv('TWITTER_USERNAME')}":
                    mentions.append({'user':user_name,'id':tweet_id})
            except NoSuchElementException:
                print("Skipping mention without tweet link.")
    except Exception as e:
        print(f"Error getting mentions: {e}")
    return mentions

def take_screenshot(driver, url, output_path):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='css-175oi2r r-1oszu61 r-1niwhzg r-18u37iz r-16y2uox r-2llsf r-13qz1uu r-1wtj0ep'])[1]")))
    driver.set_window_size(1920, 1080)
    time.sleep(2)
    driver.save_screenshot('temp_full_page.png')
    full_image = Image.open('temp_full_page.png')
    main_content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='css-175oi2r r-1f2l425 r-13qz1uu r-417010 r-18u37iz'])[1]")))
    location = main_content.location
    size = main_content.size
    left, top = int(location['x']) + 490, int(location['y']) + 57
    right, bottom = int(location['x'] + size['width']) - 250, int(location['y']) + 610
    cropped_image = full_image.crop((left, top, right, bottom))
    cropped_image.save(output_path)
    if os.path.exists('temp_full_page.png'):
        os.remove('temp_full_page.png')

replied_tweets = {}

def reply_to_mention(driver, tweet_id, image_path):
    if tweet_id in replied_tweets:
        return
    
    tweet_url = f"https://x.com/anyuser/status/{tweet_id}"
    driver.get(tweet_url)
    try:
        reply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='r-4qtqp9 r-yyyyoo r-dnmrzs r-bnwqim r-lrvibr r-m6rgpd r-50lct3 r-1srniue'])[1]"))
        )
        reply_button.click()

        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';", file_input)
        file_input.send_keys(os.path.abspath(image_path))

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[@data-testid='tweetButton'])[1]"))
        )

        tweet_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[@data-testid='tweetButton'])[1]"))
        )
        tweet_button.click()
        replied_tweets[tweet_id] = True
    except Exception as e:
        print(f"Error replying to tweet: {e}")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        login_to_twitter(driver, os.getenv('TWITTER_EMAIL'), os.getenv('TWITTER_USERNAME'), os.getenv('TWITTER_PASSWORD'))
        time.sleep(5)
        while True:
            try:
                mentions = get_mentions(driver)
                for mention in mentions:
                    user_name = mention['user'].replace("@","")
                    tweet_id = mention['id']
                    target_url = f"https://x.com/{user_name}"
                    screenshot_output_path = f"{user_name}_profile.png"
                    take_screenshot(driver, target_url, screenshot_output_path)
                    reply_to_mention(driver, tweet_id, screenshot_output_path)
            except Exception as e:
                print(f"Inner loop Exception: {e}")
            time.sleep(60)
    except Exception as e:
        print(f"Main exception: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()