import requests
import pandas as pd
import os
import time
from tqdm import tqdm
import json
import hashlib


os.environ['http_proxy'] = ''

APIURL = "http://localhost:8896"


def add_articles():
    print("==== Add articles")
    # df = pd.read_excel("../data/law_details/data_law_filter.xlsx")
    df = pd.read_excel("/home/sen/semantic/law_article_full.xlsx")
    data = df[
        [
            "law_title",
            "article_number",
            "article_title",
            "article_content",
            "law_id",
            "article_id",
        ]
    ]
    data = json.loads(data.to_json(orient="records"))

    already_add_articles = set()
    filter_data = []
    for row in data:
        law_title = row["law_title"]
        article_number = row["article_number"]
        id = f"{law_title} {article_number}"

        if id in already_add_articles:
            continue

        # TODO: replace external_article_id, external_law_id with real values from other database
        # row["external_article_id"] = hashlib.md5(
        #    f'{"law_title"}-{"article_number"}'.encode("utf-8")
        # ).hexdigest()
        # row["external_law_id"] = hashlib.md5(
        #    f'{"law_title"}'.encode("utf-8")
        # ).hexdigest()
        row["external_article_id"] = row["article_id"]
        row["external_law_id"] = row["law_id"]
        row["display_article_title"] = ""



        del row["article_id"]
        del row["law_id"]

        filter_data.append(row)
        already_add_articles.add(id)

    from tqdm import tqdm

    for data in tqdm(filter_data):
        res = requests.post(f"{APIURL}/article/insert", json={"articles": [data]})
        try:
            res = res.json()
            code = res["code"]
            if code != 2000:
                print(res)
        except Exception as err:
            print(res.text)


def remove_all_articles():
    print("==== Test remove all articles")
    res = requests.delete(f"{APIURL}/article/delete-all?drop_milvus=true")
    res = res.json()
    print(res)


if __name__ == "__main__":
    #remove_all_articles()
    add_articles()
