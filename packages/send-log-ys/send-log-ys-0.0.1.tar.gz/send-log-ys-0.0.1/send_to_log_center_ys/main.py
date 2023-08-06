import json

import requests
from datetime import datetime


URL = "http://log.ys.com/log/save"


class Log:
    def __init__(self, url=None, project=None, module=None, user=None):
        self.map = {
            "project": project or "wikenTest",
            "module": module or "test1",
            "user": user or "7921",
            "level": "error",
        }
        self.content_lst = []
        self.message = {}
        self.url = url or URL


class LogOpt(Log):
    # def __init__(self,  url, project, module, user):
    #     super(LogOpt, self).__init__(url, project, module, user)
    #
    def print(self, val, key):
        if key != "":
            self.content_lst.append({key: val, "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")})
        else:
            self.content_lst.append({"content": val, "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")})

    def print_input(self, val):
        self.message["input"] = val

    def print_return(self, val):
        self.message["result"] = val

    def add_field(self, index, val):
        self.map["field" + str(index)] = val

    def level(self, level):
        self.map["level"] = level

    def send(self):
        self.message["process"] = self.content_lst
        self.map["message"] = json.dumps(self.message, ensure_ascii=False)
        self.map["time"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f") + "+08:00"
        r = requests.post(self.url, json=self.map)
        return r.text


if __name__ == '__main__':
    log = LogOpt()
    log.print("test ifno", "key")
    log.print({"aa": "aa", "bb": "bbb"}, "测试异常")
    log.print("test ifno", "异常2")
    log.print_input("inputinfo ")
    log.print_return("result info")
    log.level("info")
    a = log.send()
    print(a)



