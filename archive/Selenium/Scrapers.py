from selenium import webdriver
import random
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
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

class ReviewsScraper(object):
    def __init__(self, name):
        self.name = name
    def BrowserOptions(self):
        options =  Options()
        options.binary_location = "/usr/bin/firefox"
        # options.add_argument("--headless")

        user_agents = ["'user-agent':'Mozilla/5.0 (Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'",
                        "'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:102.0) Gecko/20100101 Firefox/102.0'",
                        "'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:105.0) Gecko/20100101 Firefox/105.0'",
                        "'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'",
                        "'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34'",
                        "'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15'",
                        "'user-agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'",
                        "'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'",
                        "'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'",
                        "'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34'",
                        "'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'",
                        "'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Linux i686; rv:105.0) Gecko/20100101 Firefox/105.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'",
                        "'user-agent':'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:105.0) Gecko/20100101 Firefox/105.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'",
                        "'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'"]
        user_agent1 = random.choice(user_agents)
        #options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
        options.add_argument(user_agent1)

        return options
    def Scraper(self,page_URL):
        base_url = page_URL
        #fp = webdriver.FirefoxProfile()
        #fp.set_preference("network.cookie.cookieBehavior", 2)

        # options.add_argument("--user-data-dir=/home/kiprono/.config/google-chrome")

        # driver = webdriver.Chrome(executable_path="/home/kiprono/chromedriver", options=options)

        driver = webdriver.Chrome(options=self.BrowserOptions())

        f = open("output/{}.txt".format(self.name),"a+")
        # s = ReviewsDataPipeline()
        # s.create_table()
        with open("output/{}.txt".format(self.name),"r") as fp:
            done = [i.strip("\n") for i in fp.readlines()]

        number_done = len(done)

        # base_url = "https://www.trustpilot.com/review/{}.com".format(self.name)

        page_number = 1
        while True:
            if page_number < number_done/20:
               page_number = page_number + 1
               #print("page: {}-{}already done. Skipping.".format(page_number,self.name))
               continue
            page_URL = base_url+str(page_number)
            driver.get(page_URL)
            if not "page" in driver.current_url and page_number!=1:
                #print("It is done")
                break
            #print(driver.current_url)
            WebDriverWait(driver, 55).until(EC.presence_of_element_located((By.ID, "business-unit-title")))
            platform = driver.find_element(By.ID, "business-unit-title").find_element(By.TAG_NAME, "span").text

            reviews_list = driver.find_elements(By.CLASS_NAME,"styles_cardWrapper__LcCPA")
            #print(len(reviews_list))
            for index, review in enumerate(reviews_list):
                item = {}
                item["platform"] = platform
                WebDriverWait(review, 55).until(EC.presence_of_element_located((By.CLASS_NAME, "styles_reviewHeader__iU9Px")))
                stars_string = review.find_element(By.CLASS_NAME, "styles_reviewHeader__iU9Px").get_attribute("data-service-review-rating")
                stars = int(stars_string)
                item["stars"] = stars
                # try:
                #     review_date_string = review.find_element(By.CLASS_NAME, "review-content-header__dates").find_element(By.TAG_NAME, "time").get_attribute("datetime")
                # except (NoSuchElementException, TimeoutException):
                review_date_raw = review.find_element(By.CLASS_NAME, "styles_datesWrapper__RCEKH").find_element(By.TAG_NAME, "time").get_attribute("datetime")
                #review_date_string1 = json.loads([i for i in review_date_raw if "publishedDate" in i][0])
                review_date_string = review_date_raw.replace("Z","")

                review_date, review_time_string = review_date_string.split("T")
                review_time = review_time_string.split(".")[0]
                item["review_date"] = review_date #["publishedDate"].split("T")[0]
                item["review_time"] = review_time
                review_title = review.find_element(By.CLASS_NAME, "styles_reviewContent__0Q2Tg").find_element(By.TAG_NAME,"a").text
                item["review_title"] = review_title.strip()
                try:
                    review_text = review.find_element(By.CLASS_NAME, "styles_reviewContent__0Q2Tg").find_element(By.TAG_NAME,"p").text
                    item["review_body"] = review_text.strip("\n")
                except:
                    item["review_body"] = None

                item["user"] = review.find_element(By.TAG_NAME, "article").find_element(By.TAG_NAME, "a").get_attribute("href").split("/")[-1]
                
                try:
                    item["CompanyReply"] = " ".join([i.text.strip() for i in review.find_element(By.CLASS_NAME, "styles_content__Hl2Mi").find_elements(By.CLASS_NAME, "typography_body-m__xgxZ_")])
                    reply_date_string = review.find_element(By.CLASS_NAME, "styles_replyInfo__FYSje").find_element(By.TAG_NAME, "time").get_attribute("datetime")
                    reply_date, reply_time_string = reply_date_string.split("T")
                    reply_time = reply_time_string.split(".")[0]
                    item["CompanyReplyDate"] = reply_date
                    item["CompanyReplyTime"] = reply_time
                except:
                    item["CompanyReply"] = None
                    item["CompanyReplyDate"] = None
                    item["CompanyReplyTime"] = None
                # s.store(item)
               # print(item)
                f.write(str(item)+"\n")

            # platform = response.css(".header-section").css("span::text").extract_first()
            time.sleep(5)
           # exit()
            page_number = page_number + 1
        f.close()
