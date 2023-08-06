import xlrd
import csv
import random
import exrex


# Edit the module Here

def seperate_list(s, de=" "):
    k = s.split(de)
    arr = []
    for i in k:
        x = i.replace(".", "1")
        if (i.isdigit()):
            arr.append(int(i))
        elif (x.isdigit()):
            arr.append(float(i))
        elif (i.isdigit() == False):
            arr.append(i)
    return arr


def separate_list_int(s, de=" "):
    k = s.split(de)
    arr = []
    for i in k:
        arr.append(int(i))
    return arr


def separate_list_str(s, de=" "):
    k = s.split(de)
    arr = []
    for i in k:
        arr.append(i)
    return arr


def text_to_inp(s, e="  ", r=" "):
    p = []
    with open(s, "r") as f:
        k = [l.rstrip("\n") for l in f]
        x = []
        for i in k:
            x.append(i.split(e))
        for i in x:
            ar = []
            for j in i:
                b = j.replace(".", "1")
                if (j.isdigit()):
                    ar.append(int(j))
                elif (b.isdigit()):
                    ar.append(float(j))
                elif (j.isdigit() == False):
                    j.strip()
                    if (" " in j):
                        k = input(
                            "Your File Contains String '{}', if you want to consider them as normal string type 'str' or for string array type 'str-arr': ".format(j))
                        if (k == 'str'):
                            ar.append(j)
                        elif (k == 'str-arr'):
                            ar.append(seperate_list(j, r))
                    else:
                        ar.append(j)
            p.append(ar)
    return p


def csv_to_inp(s, e=",", r=" "):
    ar = []
    with open(s, "r") as f:
        lines = csv.reader(f, delimiter=e)
        for line in lines:
            k = []
            for ele in line:
                c = ele.replace(".", "1")
                if (ele.isdigit()):
                    k.append(int(ele))
                elif (c.isdigit()):
                    k.append(float(ele))
                elif (ele.isdigit() == False):
                    ele.strip()
                    if (" " in ele):
                        v = input(
                            "Your File Contains String '{}', if you want to consider them as normal string type 'str' or for string array type 'str-arr': ".format(ele))
                        if (v == 'str'):
                            k.append(ele)
                        elif (v == 'str-arr'):
                            k.append(seperate_list(ele, r))
                    else:
                        k.append(ele)
            ar.append(k)
    return ar


def dummy_inp(k):
    arr = []
    for i in k:
        if (i[0] == "int"):
            k = random.randint(i[1], i[2])
            arr.append(k)
        elif (i[0] == "float"):
            num = round(random.uniform(i[2], i[3]), i[1])
            arr.append(num)
        elif (i[0] == "str"):
            st = exrex.getone(i[1])
            arr.append(st)
        elif (i[0] == "int-arr"):
            ar = []
            for j in range(0, i[1]):
                k = random.randint(i[2], i[3])
                ar.append(k)
            arr.append(ar)
        elif (i[0] == "float-arr"):
            ar = []
            for j in range(0, i[1]):
                k = round(random.uniform(i[3], i[4]), i[2])
                ar.append(k)
            arr.append(ar)
        elif (i[0] == "string-arr"):
            ar = []
            for j in range(0, i[1]):
                st = exrex.getone(i[2])
                ar.append(st)
            arr.append(ar)
    return arr


def xls_to_inp(s, r=" "):
    workbook = xlrd.open_workbook(s)
    sheet = workbook.sheet_by_index(0)
    data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)]
            for r in range(sheet.nrows)]
    for i in range(len(data)):
        for j in range(len(data[i])):
            if (type(data[i][j]) == float):
                if (data[i][j] % 1 == 0):
                    data[i][j] = int(data[i][j])
    for i in range(len(data)):
        for j in range(len(data[i])):
            if (type(data[i][j]) == str):
                data[i][j].strip()
                if (" " in data[i][j]):
                    v = input(
                        "Your File Contains String '{}', if you want to consider them as normal string type 'str' or for string array type 'str-arr': ".format(data[i][j]))
                    if (v == 'str-arr'):
                        data[i][j] = seperate_list(data[i][j], r)
    return data
