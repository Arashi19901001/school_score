# -*- coding: utf-8 -*-
# 根据专业名称，获取专业id, 拿到专业id之后, 可以根据id, 获取开设了该专业的学科的学校的相关信息
import time
import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}


def get_id_by_major_name(name):
    name_to_id = dict()
    url = "https://api.eol.cn/gkcx/api/?access_token=&keyword={}&level1=1&level2=&page=1&signsafe=&size=20&uri=apidata/api/gk/special/lists".format(name)
    res = requests.get(url, headers=headers)
    r = res.json()
    for d in r["data"]["item"]:
        name_to_id[d["name"]] = d["special_id"]

    total = int(r["data"]["numFound"])
    max_page = total / 20
    if total % 20 != 0:
        max_page += 1
    i = 2
    while i <= max_page:
        url = "https://api.eol.cn/gkcx/api/?access_token=&keyword={}&level1=1&level2=&page={}&signsafe=&size=20&uri=apidata/api/gk/special/lists".format(name, i)
        res = requests.get(url, headers=headers)
        r = res.json()
        for d in r["data"]["item"]:
            name_to_id[d["name"]] = d["special_id"]
        i += 1
        time.sleep(1)

    if not name_to_id:
        print("未找到该专业")
        return

    for k in name_to_id:
        print("{}: {}".format(k, name_to_id[k]))


if __name__ == "__main__":
    import sys
    name = sys.argv[1]
    get_id_by_major_name(name)
