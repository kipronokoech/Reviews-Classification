from Scrapers import ReviewsScraper
import os
loc = os.path.dirname(__file__)
os.chdir(loc)

while True:
	with open("links.txt") as fp:
		for line in fp:
			nam = line.strip().split("/")[-1].replace(".com","").replace("www.","")#.split(".")
			url = line.strip()+"?page="
			# print("name",nam)
			# print(url)
			ReviewsScraper(nam).Scraper(page_URL=url)
	# except:
	# 	print("Oops!!!!!!!!!!!")
	# 	time.sleep(10)
