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
import math
try:
    from intent import Loki_badminton
    from intent import Loki_baseball
except:
    from .intent import Loki_badminton
    from .intent import Loki_baseball


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = ""
LOKI_KEY = ""
from ArticutAPI import ArticutAPI
import re
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
    resultDICT["badminton"] =0
    resultDICT["baseball"] =0
    lokiRst = LokiResult(inputLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # badminton
                if lokiRst.getIntent(index, resultIndex) == "badminton":
                    resultDICT = Loki_badminton.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)
                    resultDICT["badminton"] +=resultDICT["badminton"] 

                # baseball
                if lokiRst.getIntent(index, resultIndex) == "baseball":
                    resultDICT = Loki_baseball.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)
                    resultDICT["baseball"]  += resultDICT["baseball"] 

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

if __name__ == "__main__":
    articut = ArticutAPI.Articut(level="lv2")
    pat = "</?[a-zA-Z]+?_?[a-zA-Z]+?>"
    inputSTR = """「大鬍子」JamesHarden離隊宣言惹怒不少火箭隊友，在他確定轉戰籃網後，火箭今(15)日以109:105擊敗馬刺，前一哥撒手走人後馬上終止2連敗，火箭主帥StephenSilas表示此役勝利對重建相當重要。休賽季就高喊「賣我」的Harden在前天再度敗給湖人的賽後記者會直接表達對球隊不滿，更稱無法修復關係了，結果昨天就傳出籃網和其他3隊完成共識，今天宣布加盟。儘管少了主將，火箭比賽照樣要打，今天面對馬刺卯足全力，本季大爆發的ChristianWood攻下27分15籃板，頂替Harden首度先發的後衛SterlingBrown役住次高的23分，力退6人得分上雙的馬刺。「這是場特別的勝利。」Silas賽後表示，「對於球隊重建相當重要，對球員們意義重大，今天我們展現了鬥志，這一直是我們堅信理念，看到球員拿出這樣的表現實在太棒了。"""
    parseResultDICT = articut.parse(inputSTR)
    inputLIST = []
    count_baseball = 0
    count_badminton = 0
    for p in parseResultDICT["result_pos"]:
        if len(p) == 1:
            pass
        else:
            inputLIST.append(re.sub(pat, "", p))
    for i in range(0, math.ceil(len(inputLIST)/20)):
        resultDICT = runLoki(inputLIST[i*20:(i+1)*20])
        try: 
            count_baseball += resultDICT["baseball"]
        except:
            pass
        try: 
            count_badminton += resultDICT["badminton"]
        except:
            pass
    resultDICT["baseball"] = count_baseball  
    resultDICT["badminton"] = count_badminton
    print("Result => {}".format(resultDICT)) 

#[int(e) for e in list(myDICT.values())]