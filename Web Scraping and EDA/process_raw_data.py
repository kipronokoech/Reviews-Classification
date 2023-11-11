import json, os
from ast import literal_eval
import pandas as pd

loc = os.path.dirname(__file__)
os.chdir(loc)

for platform in ["Wise", "Paypal"]:
    all_details = []
    for file in os.listdir(f"./data/{platform}"):
        # Looping through text files containing the reviews data
        data = [literal_eval(i.strip()) for i in open(f'./data/{platform}/{file}').readlines()]
        all_details.extend(data)
    # Convert the list data into pandas DataFrame.
    df = pd.DataFrame(all_details)

    # Joining date and times for review date and company reply date to made datetime then turn the 
    # result into a valida pandas dataframe.
    df["review_datetime"]  = df["review_date"] +"T"+ df["review_time"]
    df["company_reply_datetime"] = df["CompanyReplyDate"] + "T" + df["CompanyReplyTime"]
    df = df.drop(["review_date", "review_time", "CompanyReplyDate", "CompanyReplyTime"], axis=1)

    with open (f"{platform}_file.json", "w+") as file:
        json.dump(df.to_dict(orient="records"), file, indent=3)