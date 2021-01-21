#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

import requests
import re
import math
try:
    from intent import Loki_mock_polite_2
except:
    from .intent import Loki_mock_polite_2


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"

from ArticutAPI import ArticutAPI
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []

        try:
            result = requests.post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": INTENT_FILTER
            })

            if result.status_code == requests.codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST):
    resultDICT = {}
    resultDICT["mock"] =0
    lokiRst = LokiResult(inputLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # mock_polite_2
                if lokiRst.getIntent(index, resultIndex) == "mock_polite_2":
                    resultDICT = Loki_mock_polite_2.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)
                    resultDICT["mock"] += 0
                    

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

if __name__ == "__main__":
    articut = ArticutAPI.Articut(level="lv2")
    pat = "</?[a-zA-Z]+?_?[a-zA-Z]+?>"
    #inputSTR = """女生穿名牌就代表 想要男生提供奢華生活嗎?
#其實不是的，像我一個女性朋友 雖然平日外出也是一身名牌包
#但她就是可以跟一個其貌不揚的男生交往
#說是看上對方的才華
#有一次我就好奇問她，她男友的才華是什麼?
#「他可以單手開瑪莎拉蒂耶~!」
#我的女性朋友如此回答我"""

    #inputSTR = """（中央社記者鍾榮峰台北21日電）台灣期貨交易所今天表示，已取得美國商品期貨交易委員會（CFTC）核發台灣指數公司台灣上市上櫃生技醫療指數期貨交易許可，即日起美國人可直接交易台灣生技期貨契約。期交所指出，生技醫療是台灣重點發展產業，類股成交值次於電子類股及金融保險類股。台灣生技指數涵蓋上市、櫃生技類股中具市值代表性股票，可表彰台灣生技醫療股票績效，並設有成分股權重上限，可避免因單一股票權重過高，使指數無法反映整體產業發展趨勢問題。
    #期交所去年6月8日推出台灣生技期貨，契約乘數每點新台幣50元，依1月20日指數收盤水準3871.82點，契約規模約新台幣20萬元，期交所指出交易門檻相對低，可作為國人交易新選擇及產業風險管理工具。此次取得CFTC核發交易許可，可進一步吸引更多外資參與交易，提升市場流動性與國際知名度。"""
    
    #inputSTR = """【蔡英文喊團結就可以擋病毒？】
#北部某醫院院內新冠肺炎群聚感染再擴大，目前已有4名醫護感染，蔡英文說「病毒再厲害，也比不過人心的團結」，原來光喊話就能抵擋病毒？
#陳時中則說「沒看到洞，但有一些細縫」。但同樣地，在陳時中身上也看到許多「隙縫」。
#指揮中心明訂接受公費採檢者，採檢後3天內避免出入公眾場所。然而陳時中接受採檢後，隔天就主持疫情記者會。原來，指揮中心訂定的SOP誰都不能違反，但陳時中可以。
#陳時中還很委屈的說「自己當然也想休息，但因職責所在。」難道指揮中心都沒人，只剩下陳時中要違反規則來開記者會？
#相較陳時中可接受採檢，但身處新冠肺炎群聚感染醫院的醫生，想自行報名採檢卻遭拒，醫師擔心傳染孩子，已1個禮拜不敢回家。
#指揮官可以優先採檢，可以不用遵守SOP，小醫師想採檢還要排隊，蔡英文、蘇貞昌狂喊要為醫護人員打氣，但真的有為台灣的醫護人員做些什麼嗎？
#北部某醫院院內感染擴大，醫院的SOP到底有沒有落實？前線資源短缺是否短缺？這些「隙縫」會不會成為防疫的大洞？
#這些都是必須警惕檢討並盡速補好破口，而非蔡英文文青式的喊「團結」，就可以抵擋病毒。"""
    
    inputSTR ="""古有愚公移山，今有魏公募資，爐渣聖地的金主希望能夠開發爐渣樂園，想出用拍電影當宣傳的方式，
請出只會複製成功模式的老人來當門神，一堆酸民笑魏公：『計畫那麼大，阿是在畫唬爛喔， 募款募到你死，爐渣樂園都蓋不起
來吧』魏公反駁死酸民說：「我就算老死，但我死後還有子子孫孫可以繼續這項偉業，錢只會
越募越多，園區怎會蓋不起來呢？」(見《列子．湯問》鎮瀾宮媽祖聽了非常感動，北斗武財神聽了也非常感動，祂們會派人幫忙的，大家不要失去信心，天使金主會出現，樂園和電影總有一天會完成的"""

    parseResultDICT = articut.parse(inputSTR)
    inputLIST = []
    count_mock = 0
    for p in parseResultDICT["result_pos"]:
        if len(p) == 1:
            pass
        else:
            inputLIST.append(re.sub(pat, "", p))
    for i in range(0, math.ceil(len(inputLIST)/20)):
        resultDICT = runLoki(inputLIST[i*20:(i+1)*20])
        try: 
            count_mock  += resultDICT["mock"]
        except:
            pass
    
        
    resultDICT["mock"] = count_mock
    print("mock politeness score: {}".format(count_mock/len(inputLIST)))
    #print("Result => {}".format(resultDICT))