import json
import sys
import requests
import urllib.parse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    with open(sys.argv[1]) as f:
        data=json.load(f)
except FileNotFoundError:
    print("seems like post collection name is wrong or file don't exist in the path :(")
    exit()

proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
url=""
head={}
host=""
i=1

for item in data['item']:
    # Call API Title
    j=str(i)
    print(j+"."+" "+item['name'])
    i+=1
    print(host)
    
    # Call API URL
    try:
        if "BASE_URL" in item['request']['url']['raw']:
            obj=data['variable'][0]['value']
            host=urllib.parse.urlsplit(obj).hostname
            temp=item['request']['url']['raw']
            url="http://"+temp.replace("{{BASE_URL}}",host)
        else:
            url=item['request']['url']['raw']
            host=urllib.parse.urlsplit(item['request']['url']['raw']).hostname
    except:
        print("Snap i think we got a wrong Environment Variable :(")
        print("")

    # Call API Header
    try:
        head.update({'Host':host})
        temp=len(item['request']['header'])
        for x in range(temp):
            head.update({item['request']['header'][x]['key']:item['request']['header'][x]['value']})
    except:
        print("")
   

    # Call API Body
    try:
        payload=(item['request']['body']['raw'])
    except:
        print("Well, not every API have body Lakshman, FYI don't ask who is Lakshman :P")
        print("")

    # Push API
    method=item['request']['method']
    print("Method: "+method)
    if method=="GET":
       requests.get(url,data=payload,headers=head,proxies=proxy,verify=False)
    elif method=="POST":
        requests.post(url,data=payload,headers=head,proxies=proxy,verify=False)
    elif method=="PUT":
        requests.put(url,data=payload,headers=head,proxies=proxy,verify=False)
    elif method=="DELETE":
        requests.delete(url,data=payload,headers=head,proxies=proxy,verify=False)
    elif method=="PATCH":
        requests.patch(url,data=payload,headers=head,proxies=proxy,verify=False)
    elif method=="HEAD":
        requests.head(url,data=payload,headers=head,proxies=proxy,verify=False)
    else:
        requests.options(url,data=payload,headers=head,proxies=proxy,verify=False)
    print("")