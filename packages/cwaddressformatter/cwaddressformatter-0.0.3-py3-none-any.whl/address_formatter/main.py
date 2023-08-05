# -*- coding: utf-8 -*-

import re
import csv
import cn2an

def sadd(x):
    x.reverse()
    if len(x) >= 2:
        x.insert(1,kin[0])
        if len(x) >= 4:
            x.insert(3,kin[1])
            if len(x) >= 6:
                x.insert(5,kin[2])
                if len(x) >= 8:
                    x.insert(7,kin[3])
                    if len(x) >= 10:
                        x.insert(9,kin[0])
                        if len(x) >= 12:
                            x.insert(11,kin[1])

    x=fw(x)
    x=d1(x)
    x=d2(x)
    x=dl(x)
    return x
    
    
def rankis():
    rank=[]
    for i in range(9999999):
        i=list(str(i))
        for j in i:
            i[(i.index(j))]=num[int(j)]
        i=sadd(i)
        rank.append(i)
    return rank


def d1(x):
    if '零' in x:
        a=x.index('零')
        if a==0:
            del x[0]
            d1(x)
        else:
            if x[a+2] in ['十','百','千','萬','零']:
                if x[a+1] != '萬':
                    del x[a+1]
                    d1(x)     
    return x
def d2(x):
    try:
        a=x.index('零')
        if x[a-1] in ['十','百','千','零']:
            del x[a-1]
            d2(x[a+1])
    except:pass
    return x

def fw(x):
    if len(x) >= 9:
        if x[8] == '零':
            del x[8]
    return x
def dl(x):
    try:
        if x[0]=='零':
            del x[0]
            del1(x)
    except:pass
    x.reverse()
    x=''.join(x)
    return x

exceptChar = {
    "二一號": "21號"
}
def zh2digit(string):
    if string == "":
        return ""

    if string in exceptChar:
        return exceptChar[string]

#   print("uchars_chinese:", uchars_chinese)
#   print(cn2an.transform(uchars_chinese, "cn2an"))
    return cn2an.transform(string, "cn2an")

# 數字轉國字
def digit2zh(ustring):
    if not ustring:
        return ""
    return cn2an.transform(ustring, "an2cn")

    a2cChar = {
        "之": "-",
        "~": "-",
        "F": "樓",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
    }
    rstring = ""
    d = 0
    ustring = zh2digit(ustring)
    # print(ustring)

    digit = re.findall('\d+', ustring)
    # print(digit)
    if digit and int(digit[0]) >= 10:
        rstring = ustring
    else:
        # print(match.groups())
        for i in range(len(ustring)):
            idx = len(ustring)-i-1
            if ustring[idx] in a2cChar:
                if d > 0:
                    ten = ""
                else:
                    ten = ""
                d += 1
                rstring = a2cChar[ustring[idx]] + ten + rstring
            else:
                d = 0
                rstring = ustring[idx] + rstring


    return rstring

def findAdds(address, addr):
    # print(address)
    tmp = [address.find(x) for x in addr]
    # print(addr,tmp)
    if len(tmp) > 0:
        for i in tmp:
            if i >= 0:
                if addr == ('之'):
                    # print("----TEST")
                    return zh2digit(address), ""
                else:
                    return address[0:i+1], address[i+1:]
        
    return "", address


openRoad = []
with open('opendata108road.csv', newline='') as csvfile:

  rows = csv.DictReader(csvfile)

  # 以迴圈輸出指定欄位
  for row in rows:
    openRoad.append(row['road'])



def getAddress(address):
    original = address
# r'((.*)(市|縣))?((.*)(區|市|鄉|鎮))?((.*)(村|里))?((.*)鄰)?((.*)(路|街|道))?((.*)段)?((.*)巷)?((.*)弄)?((.*)號)?((.*)(樓|F))?(.*)')

    
#city, cityName, cityUnit, district, districtName, districtUnit, village, villageName, villageUnit, neighbor, neighborName, road, roadName, roadUnit, sec, secUnit, lane, landName, alley, alleyName, no, noName, floor, floorName, floorUnit, other

    city, address = findAdds(address, ("縣","市"))
    district, address = findAdds(address, ("鄉", "區","市","鎮"))
    village, address = findAdds(address, ("里", "村"))
    neighbor, address = findAdds(address, ("鄰"))
    road, address = findAdds(address, ("大樓","街","路","大道","城"))
    sec, address = findAdds(address, ("段"))
    lane, address = findAdds(address, ("巷"))
    alley, address = findAdds(address, ("弄"))
    no, address = findAdds(address, ("號"))
    floor, address = findAdds(address, ("樓"))
    room, address = findAdds(address, ("室"))
    dash, address = findAdds(address, ("之"))
    
    # if road == '苓雅一路':
    #     print("Address:", original)
    #     print("city:", city, "district:", district, "village:", village, "neighbor:", neighbor)
    #     print("road:", road,  "sec:", sec, "lane:", lane, "alley:", alley)
    #     print("no:", no, "floor:", floor, "room:", room, "address:", address, "dash:", dash)
    #     print("")

    if road:
        if city in ('市','縣','新市'):
            road = city+road

        if village in ('美村','仁里','豐村','力里'):
            road = village+road


    else:
        if neighbor:
            road = village + neighbor
        else:
            road = village
    
    if (district is not None and district[-3:] in ('工業區', '學園區', '園區', '市','鎮')):
        if road:
            road = district + road
        else:
            road = district

    if not road and not no:
        # print("PASS")
        return original

    
    if road not in openRoad:
        # print(road)
        road = digit2zh(road)

    sec = digit2zh(sec)
    lane = zh2digit(lane)
    alley = zh2digit(alley)
    # floorName = zh2digit(floorName)
    # floorUnit = zh2digit(floorUnit)
    no = zh2digit(no)
    floor = zh2digit(floor)
    def replaceDash(string):
        string = string.replace("之", "-")
        string = string.replace("一", "-")
        return string
    address = replaceDash(address)
    dash = replaceDash(dash)
    no = replaceDash(no)

    # print("no:" , no)
    # if road == '村圓山路':
    #     print("Address:", original)
    #     print("city:", city, "district:", district, "village:", village, "neighbor:", neighbor)
    #     print("road:", road,  "sec:", sec, "lane:", lane, "alley:", alley)
    #     print("no:", no, "floor:", floor, "room:", room, "address:", address, "dash:", dash)
    #     print("")
    

    str = "".join([road, sec, lane, alley, no, floor, room, dash, address])
    str = str.replace("F", "樓")
    str = str.replace("~", "-")
    
    return str

# print(getAddress("福鎮街43-2號"))


if __name__ == '__main__':
    pass