
import requests
from bs4 import BeautifulSoup

url = "https://db.netkeiba.com/race/202003010202"
r=requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
soup_span = soup.find_all("span")
allnum=int((len(soup_span)-9)/3)#馬の数

#馬の情報
soup_txt_l=soup.find_all(class_="txt_l")
name=[]#馬の名前
for num in range(allnum):
    name.append(soup_txt_l[4*num].contents[1].contents[0])

jockey=[]#騎手の名前
for num in range(allnum):
    jockey.append(soup_txt_l[4*num+1].contents[1].contents[0])

soup_txt_r=soup.find_all(class_="txt_r")
horse_number=[]#馬番
for num in range(allnum):
    horse_number.append(soup_txt_r[1+5*num].contents[0])
    
runtime=[]#走破時間
for num in range(allnum):
    runtime.append(soup_txt_r[2+5*num].contents[0])

odds=[]#オッズ
for num in range(allnum):
    odds.append(soup_txt_r[3+5*num].contents[0])

soup_nowrap = soup.find_all("td",nowrap="nowrap",class_=None)
pas = []#通過順
for num in range(allnum):
    pas.append(soup_nowrap[3*num].contents[0])

weight = []#体重
for num in range(allnum):
    weight.append(soup_nowrap[3*num+1].contents[0])
    
soup_tet_c = soup.find_all("td",nowrap="nowrap",class_="txt_c")
sex_old = []#性齢
for num in range(allnum):
    sex_old.append(soup_tet_c[6*num].contents[0])

handi = []#斤量
for num in range(allnum):
    handi.append(soup_tet_c[6*num+1].contents[0])

last = []#上がり
for num in range(allnum):
    last.append(soup_tet_c[6*num+3].contents[0].contents[0])

pop = []#人気
for num in range(allnum):
    pop.append(soup_span[3*num+11].contents[0])

houseInfo = [name,jockey,horse_number,runtime,odds,pas,weight,sex_old,handi,last,pop]


#レースの情報
sur=str(soup_span[7]).split("/")[0].split(">")[1][0]
rou=str(soup_span[7]).split("/")[0].split(">")[1][1]
dis=str(soup_span[7]).split("/")[0].split(">")[1].split("m")[0][-4:]
con=str(soup_span[7]).split("/")[2].split(":")[1][1]
wed=str(soup_span[7]).split("/")[1].split(":")[1][1]
soup_smalltxt = soup.find_all("p",class_="smalltxt")
detail=str(soup_smalltxt).split(">")[1].split(" ")[1]
date=str(soup_smalltxt).split(">")[1].split(" ")[0]
clas=str(soup_smalltxt).split(">")[1].split(" ")[2].replace(u'\xa0', u' ').split(" ")[0]
title=str(soup.find_all("h1")[1]).split(">")[1].split("<")[0]
raceInfo = [[title],[date],[detail],[clas],[sur],[dis],[rou],[con],[wed]]#他と合わせるためにリストの中にリストを入れる

#払い戻しの情報
payBack = soup.find_all("table",summary='払い戻し')
payBackInfo=[]#単勝、複勝、枠連、馬連、ワイド、馬単、三連複、三連単の順番で格納

def appendPayBack1(varSoup):#複勝とワイド以外で使用
    varList = []
    varList.append(varSoup.contents[3].contents[0])
    varList.append(varSoup.contents[5].contents[0])
    payBackInfo.append(varList)

def appendPayBack2(varSoup):#複勝とワイドで使用
    varList = []
    for var in range(3):
        varList.append(varSoup.contents[3].contents[2*var])
        varList.append(varSoup.contents[5].contents[2*var])
    payBackInfo.append(varList)

appendPayBack1(payBack[0].contents[1])#単勝
appendPayBack2(payBack[0].contents[3])#複勝
appendPayBack1(payBack[0].contents[5])#枠連
appendPayBack1(payBack[0].contents[7])#馬連
appendPayBack2(payBack[1].contents[1])#ワイド
appendPayBack1(payBack[1].contents[3])#馬単
appendPayBack1(payBack[1].contents[5])#三連複
appendPayBack1(payBack[1].contents[7])#三連単

import csv
with open('./test_data.csv', 'w', newline='',encoding="UTF-8") as f:
    csv.writer(f).writerows(houseInfo)
    csv.writer(f).writerows(raceInfo)
    csv.writer(f).writerows(payBackInfo)