import mysql.connector
import sqlite3
from ast import literal_eval
import json

class ReviewsDataPipeline(object):
	def __init__(self):
		self.establish_connection()
		self.create_table()
	def establish_connection(self):
		self.connection = mysql.connector.connect(
			host = "localhost", #or 127.0.0.1
			port = "3306",
			user = "root",
			password = "destinyx2719*KE",
			database = "reviews",
			auth_plugin = "mysql_native_password")
		self.cursor = self.connection.cursor()

	def create_table(self):
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS trustpilot_reviews_table
			(
				stars INT(5),
				review_title TEXT,
				review_body TEXT,
				platform TEXT,
				review_date DATE,
				id TEXT,
				CompanyReply TEXT,
				CompanyReplyDate TEXT,
				CompanyReplyTime TEXT
			)
			""")
	def store(self,item):
		self.cursor.execute("""SET NAMES utf8mb4""")
		self.cursor.execute("""
			INSERT INTO trustpilot_reviews_table VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",\
			(
				item["stars"],
				item["review_title"],
				item["review_body"],
				item["platform"],
				item["review_date"],
				item["id"],
				item["CompanyReply"],
				item["CompanyReplyDate"],
				item["CompanyReplyTime"]
			))
		self.connection.commit()


s = ReviewsDataPipeline()
s.create_table()


if __name__ == "__main__":
	with open(file="./output/transferwise.txt",mode="r", encoding="utf8") as fp:
		for index, line in enumerate(fp):
			# print(index)
			line = literal_eval(line)
			# print(json.dumps(line,indent=3))
			s.store(line)
