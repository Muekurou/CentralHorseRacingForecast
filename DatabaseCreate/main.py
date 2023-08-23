import requests
from bs4 import BeautifulSoup

url = "https://db.netkeiba.com/race/202003010202"
r= requests.get(url)

soup = BeautifulSoup(r.content, "html.parser") 

payBack = soup.find_all("table", summary='払い戻し')
payBackList = [] # 単勝, 複勝， 馬連， ワイド， 馬単， 三連複， 三連単

def appendPayBack_for_MultipleWins_and_Wide(varSoup):
    varList = []
    for var in range(3):
        varList.append(varSoup.contents[3].contents[2*var])
        varList.append(varSoup.contents[5].contents[2*var])
    payBackList.append(varList)
    
def appendPayBackOthers(varSoup):
    varList = []
    varList.append(varSoup.contents[3].contents[0])
    varList.append(varSoup.contents[5].contents[0])
    payBackList.append(varList)

appendPayBackOthers(payBack[0].contents[1]) # 単勝
appendPayBack_for_MultipleWins_and_Wide(payBack[0].contents[3]) # 複勝
appendPayBackOthers(payBack[0].contents[5]) # 枠連
appendPayBackOthers(payBack[0].contents[7]) # 馬連
appendPayBack_for_MultipleWins_and_Wide(payBack[1].contents[1]) # ワイド
appendPayBackOthers(payBack[1].contents[3]) # 馬単
appendPayBackOthers(payBack[1].contents[5]) # 三連複
appendPayBackOthers(payBack[1].contents[7]) # 三連単

print(payBackList)