"""
Law
document_type: ("luật" OR "nghị định" OR "thông tư" OR "nghị quyết" OR "pháp lệnh")
http://solrcc.toaan.gov.vn/solr/Law/select?fl=id%2Ctitle&indent=true&q.op=OR&q=document_type%3A%20(%22lu%E1%BA%ADt%22%20OR%20%22ngh%E1%BB%8B%20%C4%91%E1%BB%8Bnh%22%20OR%20%22th%C3%B4ng%20t%C6%B0%22%20OR%20%22ngh%E1%BB%8B%20quy%E1%BA%BFt%22%20OR%20%22ph%C3%A1p%20l%E1%BB%87nh%22)&rows=100000

LawDetail
http://solrcc.toaan.gov.vn/solr/LawDetail/select?fl=id%2Ctitle%2Carticle_id%2Carticle%2Ccontent&indent=true&q.op=OR&q=*&rows=150000

"""
import os
import json
import traceback

import tqdm

lawdetail_path = "/home/sontv17/cyberbot/k8s-nth-guideline/tla-deployment-guideline/database/2. solr_init_code/solr_data"
law_path = "/home/sontv17/Desktop/select.json"

map_law_id_to_article = dict()
for filename in os.listdir(lawdetail_path):
    print(f"reading {filename}...")
    articles = json.load(open(os.path.join(lawdetail_path, filename), "r"))
    for article in articles:
        law_id = article["law_id"][0]
        
        if law_id in map_law_id_to_article:
            map_law_id_to_article[law_id].append(article)
        else:
            map_law_id_to_article[law_id] = [article]

print(f"reading {law_path}")
laws = json.load(open(law_path, "r"))["response"]["docs"]

output = []
for law in tqdm.tqdm(laws):
    law_id = law["id"]
    law_title = law["title"][0]
    
    articles = map_law_id_to_article.get(law_id, [])
    
    if articles:
        for article in articles:
            try:
                output.append({
                    "law_id": law_id,
                    "article_id": article["id"],
                    "law_title": law_title,
                    "article_number": article.get("article_id", ""),
                    "article_title": article.get("title", ""),
                    "article_content": article.get("content", "")
                })
            except:
                print("ERROR")
                print(article)
                traceback.print_exc()
        
print("Saving to output.json ...")
with open("output.json", "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print("Done")
    
