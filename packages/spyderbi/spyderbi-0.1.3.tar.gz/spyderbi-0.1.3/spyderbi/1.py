import requests
import json
from translate import translate

def printspace(deep):
    print(deep,end="")
    for i in range(deep):
        print("    ",end ="")
def prints(data,deep):
    q ={}
    z= []
    if type(data) != type(q):
        printspace(deep)
        print(data)
        return
    for i in data.keys():
        newdata = data[i]
        if type(q) == type(newdata):
            printspace(deep)
            print(i)
            prints(newdata, deep+1)
        else:
            printspace(deep)
            print(i)
        if type(z)== type(newdata):
            for j in newdata:
                prints(j, deep+1)
trans = translate()
trans.getbv("BV197411d7uG")
av = trans.putav()
url = "https://api.bilibili.com/x/space/arc/search?mid=349550991&;pn=1&ps=25&jsonp=jsonp "
#已知bv


# url = "http://api.bilibili.com/x/v2/reply?jsonp=jsonp&;type=1&oid="+str(av)

p = requests.get(url)
q ={}
print(type(q))
res_p = p.content.decode()
dict_json = json.loads(res_p)
# # for i in dict_json.keys():
# #     if type(dict_json[i]) == type(q):
# #         for i in dict_json[i].keys():
# #             print(i)
# times =0
# answer = {}
# for i in dict_json["data"]["replies"]:
#     print(i["member"]["uname"])
#     print(i["member"]["level_info"]["current_level"])
#     answer[i["content"]["message"]] = []
#     if i["replies"] !=None:
#         for j  in i["replies"]:
#             answer[i["content"]["message"]].append(j["content"]["message"])

# print(answer)

print(dict_json)

