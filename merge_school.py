# -*- coding: utf-8 -*-
# 将文件夹下的不同文件按学校进行合并
import os
import re
import csv
from collections import defaultdict


def get_legal_files(file_dir):
    """
    获取合法的文件
    """
    file_list = list()
    for subdir, dirs, files in os.walk(file_dir):
        for f in files:
            file_path = os.path.join(subdir, f)
            file_list.append(file_path)
    print(file_list)
    return file_list


def merge_schools(file_dir):
    file_list = get_legal_files(file_dir)
    major = defaultdict(list)
    for f in file_list:
        g = re.search("\d{4,4}_(\w+)_\d+\.csv", f)
        if g:
            m = g.group(1)
            print("获取{}的数据".format(f))
            with open(f, "r") as r:
                head = r.readline().strip()
                for line in r:
                    line = line.strip()
                    major[line].append(m)
        else:
            print("舍弃{}的数据".format(f))

    file_name = "学校汇总.csv"
    with open(file_name, "w", encoding='utf-8-sig') as f:
        w = csv.writer(f)
        head = head.split(",")
        head.append("开设专业")
        w.writerow(head)
        for d in major:
            data = d.split(",")
            data.append(" ".join(major[d]))
            w.writerow(data)


if __name__ == "__main__":
    merge_schools(".")
