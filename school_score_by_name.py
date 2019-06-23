# -*- coding: utf-8 -*-
# import traceback
import requests
import time
import csv


class SchoolScoreByName:
    def __init__(self, name, max_page, year="2018", province="33"):
        # max_page的范围自己去找, 在https://gkcx.eol.cn/school/search?schoolflag=&argschtype=%E6%99%AE%E9%80%9A%E6%9C%AC%E7%A7%91&province=&recomschprop=&keyWord1=师范
        # 填上查询条件
        # 我这是查询条件是师范, 一共有7页
        # 33为浙江, 其他省份自己查找
        self.max_page = int(max_page)
        self.name = name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        self.year = year
        self.province = province
        self.id_to_schoolname = dict()
        self.id_to_schooltype = dict()

    def get_school_id(self):
        i = 1
        school_ids = list()
        while i <= self.max_page:
            print("正在查询第{}页学校信息".format(i))
            url = "https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_dual_class=&keyword={}&page={}&province_id=&request_type=1&school_type=&&signsafe=&size=20&sort=view_total&type=&uri=apigkcx/api/school/hotlists".format(self.name, i)
            res = requests.get(url, headers=self.headers)
            time.sleep(1)
            r = res.json()
            for school in r["data"]["item"]:
                school_ids.append(school["school_id"])
                self.id_to_schoolname[str(school["school_id"])] = school["name"]
                if school["school_type"] == 6000:
                    self.id_to_schooltype[str(school["school_id"])] = "普通本科"
                elif school["school_type"] == 6001:
                    self.id_to_schooltype[str(school["school_id"])] = "专科（高职）"
                elif school["school_type"] == 6002:
                    self.id_to_schooltype[str(school["school_id"])] = "独立学院"
                elif school["school_type"] == 6003:
                    self.id_to_schooltype[str(school["school_id"])] = "中外合作办学"
                elif school["school_type"] == 6007:
                    self.id_to_schooltype[str(school["school_id"])] = "其他"
            i += 1
        return school_ids

    def _get_school_score(self, school_id):
        url = "https://static-data.eol.cn/www/2.0/schoolprovinceindex/{}/{}/{}/3/1.json".format(str(self.year), str(school_id), str(self.province))
        res = requests.get(url, headers=self.headers)
        try:
            r = res.json()
        except Exception:
            print(res.text)
            # traceback.print_exc()
            time.sleep(0.2)
            return {}
        time.sleep(0.2)
        return r["data"]['item']

    def gen_json(self):
        school_ids = self.get_school_id()
        print(self.id_to_schoolname)
        file_name = "{}_{}_{}.csv".format(self.year, self.name, self.province)
        with open(file_name, "w", encoding='utf-8-sig') as f:
            w = csv.writer(f)
            s = ["学校名", "办学类型", "最高分", "平均分", "最低分", "最低排名", "省控线", "录取批次"]
            w.writerow(s)
            for i in school_ids:
                print("正在查询学校{}:{}的分数线".format(i, self.id_to_schoolname[str(i)]))
                data = self._get_school_score(i)
                if not data:
                    print("无法查询到学校{}:{}的分数线".format(i, self.id_to_schoolname[str(i)]))
                    s = [self.id_to_schoolname[str(i)], self.id_to_schooltype[str(i)], "--", "--", "--", "--", "--", "--"]
                    w.writerow(s)
                    continue
                for d in data:
                    s = [self.id_to_schoolname[str(d["school_id"])], self.id_to_schooltype[d["school_id"]], d["max"], d["average"], d["min"], d["min_section"], d["proscore"], d["local_batch_name"]]
                    w.writerow(s)


if __name__ == "__main__":
    # usage example: python3 school_score_by_name.py 师范 7
    import sys
    name = sys.argv[1]
    max_page = sys.argv[2]
    s = SchoolScoreByName(name, max_page)
    s.gen_json()
