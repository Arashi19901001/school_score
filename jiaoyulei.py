# -*- coding: utf-8 -*-
# 获取所有教育类相关专业及学校的信息
import requests
import time
from school_score_by_major import SchoolScoreByMajor


def get_edu_related_school():
    url = "https://api.eol.cn/gkcx/api/?access_token=&keyword=%E6%95%99%E8%82%B2&level1=1&level2=&page=1&signsafe=&size=20&uri=apidata/api/gk/special/lists"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    time.sleep(1)
    r = res.json()
    id_to_name = dict()
    for d in r["data"]["item"]:
        if d["level3_name"] == "教育学类":
            id_to_name[d["special_id"]] = d["name"]
    for id_ in id_to_name:
        print("{}:{}".format(id_to_name[id_], id_))
    for id_ in id_to_name:
        print("*" * 50)
        print("正在查询{}:{}".format(id_to_name[id_], id_))
        s = SchoolScoreByMajor(id_, id_to_name[id_])
        s.gen_json()


if __name__ == "__main__":
    get_edu_related_school()
