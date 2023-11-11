from selenium import webdriver
import random
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
import time
import json
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from DataPipeline import ReviewsDataPipeline
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
loc = os.path.dirname(__file__)
os.chdir(loc)

options =  Options()

user_agents = [i.strip() for i in open("user_agents.txt").readlines()]
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

for page in range(3319, 8023):
    url = f"https://www.trustpilot.com/review/wise.com?page={page}"
    # url = f"https://www.trustpilot.com/review/www.paypal.com?page={page}"
    # print(url)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(user_agents)})
    # print(driver.execute_script("return navigator.userAgent;"))
    driver.get(url)

    start = time.time()
    webdriver.support.ui.WebDriverWait(driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
    stop = time.time()

    platform = driver.find_element(By.ID, "business-unit-title")\
        .find_element(By.CLASS_NAME, "title_displayName__TtDDM").text.replace(" ", "")

    reviews_cards = driver.find_element(By.CLASS_NAME, "styles_reviewsContainer__3_GQw").find_elements(By.CLASS_NAME, "styles_cardWrapper__LcCPA")

    # if not os.path.exists(f"./data/{platform}.txt"):
    #     open(f"./data/{platform}.txt")
    f = open(f"./data/{platform}/{platform}_page_{page}.txt", "a+")
    for review in reviews_cards:
        data = {}
        data["platform"] = platform
        url1 = review.find_element(By.CLASS_NAME, "styles_reviewContent__0Q2Tg").find_element(By.TAG_NAME, "a").get_attribute("href")
        id1 = url1.split("/")[-1]
        data["id"] = id1

        stars_string = review.find_element(By.CLASS_NAME, "styles_reviewHeader__iU9Px").get_attribute("data-service-review-rating")
        stars = int(stars_string)
        data["stars"] = stars

        title = review.find_element(By.CLASS_NAME, "typography_heading-s__f7029").text
        data["title"] = title

        message = review.find_element(By.CLASS_NAME,"typography_body-l__KUYFJ").text
        data["message"] = message

        date_time = review.find_element(By.TAG_NAME, "time").get_attribute("datetime")
        review_date, review_time_string = date_time.split("T")
        review_time = review_time_string.split(".")[0]
        data["review_date"] = review_date
        data["review_time"] = review_time
        try:
            reply_content = review.find_element(By.CLASS_NAME, "styles_content__Hl2Mi")
            date_time_reply = reply_content.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            reply_date, reply_time_string = date_time_reply.split("T")
            reply_time = reply_time_string.split(".")[0]
            # reply_message = reply_content.find_element(By.CLASS_NAME, "styles_message__shHhX").text
            data["CompanyReply"] = reply_content.text
            data["CompanyReplyDate"] = reply_date
            data["CompanyReplyTime"] = reply_time
        except NoSuchElementException:
            data["CompanyReply"] = None
            data["CompanyReplyDate"] = None
            data["CompanyReplyTime"] = None
        
        f.write(str(data)+"\n")
        # print(data)
    time.sleep(random.randint(0,3))
    f.close()
    
