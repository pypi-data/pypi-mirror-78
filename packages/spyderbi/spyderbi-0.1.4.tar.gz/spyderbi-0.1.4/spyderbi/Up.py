import getdata
import json
class Person():
    mid = ""
    need = ["mid","name","sex","sign","level","birthday","coins","following","follower","black"]#following关注数,follower,粉丝数,"black",黑名单
    def __init__(self,mid):
        self.mid = mid

    def getbasic(self):
        info = {}
        url = "https://api.bilibili.com/x/space/acc/info?mid="+self.mid+"&jsonp=jsonp"
        dict_json=getdata.getdict(url)

        if dict_json["code"] != 0:
            raise Exception("invalid mid")
        else:
            for i,j in dict_json["data"].items():
                if i in self.need:
                    info[i]=j

        url = "https://api.bilibili.com/x/relation/stat?vmid="+self.mid+"&jsonp=jsonp"
        dict_json=getdata.getdict(url)
        if dict_json["code"] != 0:
            raise Exception("invalid mid")
        else:
            for i,j in dict_json["data"].items():
                if i in self.need:
                    info[i]=j
        return info

class up(Person):
    sumcount = 0
    videolist = []
    videotype ={}#用来表示用户有多少稿件,每个稿件是什么区的
    moreinfo = {}#有些数据无法通过前面api获得,只能这么搞关于发布时间和时长之类的
    videoneed = ["created","length","is_union_video","typeid"]
    def __init__(self,mid):
        super(Person,self).__init__()
        self.mid =mid

    def getvideos(self):
        pn = 1
        page =100
        url = "https://api.bilibili.com/x/space/arc/search?mid="+self.mid+"&;pn=1&ps=100&jsonp=jsonp"
        dict_json=getdata.getdict(url)
        if dict_json["code"] != 0 :
            raise Exception("can't do that")
        jsgood=json.dumps(dict_json["data"]["list"],indent=1,ensure_ascii=False)
        print(jsgood)
        self.videotype = dict_json["data"]["list"]["tlist"]
        for key,value in self.videotype.items():
            self.sumcount += value["count"]
        for i in dict_json["data"]["list"]["vlist"]:
            self.videolist.append(str(i["aid"]))
            self.moreinfo[i["aid"]] = {}
            for keyj,valuej in i.items():
                if keyj in self.videoneed:
                    self.moreinfo[i["aid"]][keyj] = valuej

        while page<self.sumcount:
            pn+=1
            page+=100
            url = "https://api.bilibili.com/x/space/arc/search?mid="+self.mid+"&;pn="+str(pn)+"&ps=100&jsonp=jsonp"
            dict_json=getdata.getdict(url)
            if dict_json["code"] != 0 :
                raise Exception("can't do that")
            for i in dict_json["data"]["list"]["vlist"]:
                self.videolist.append(str(i["aid"]))
                for keyj,valuej in i.items():
                    if keyj in self.videoneed:
                        self.moreinfo[i["aid"]][keyj] = valuej
        return self.videolist
    def timetranslate(self):
        if self.moreinfo !={}:
            for key,value in self.moreinfo.items():
                value["created"] = getdata.gettime(value["created"])
            print("translate time successful")
        else:
            print("can't translate")

