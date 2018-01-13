#-*- coding：utf-8 -*-
import requests

import hmac
import base64
import hashlib 
import requests
import binascii

import time
import random
import json
import re

from config import appid
from config import bucket
from config import secret_id
from config import secret_key
from config import wx_url as url

#从万象优图 图片转字符串
def img_to_str(num):
    files = {
      "appid": appid,
      "bucket": bucket#,
      #'url':'http://demo1-1253660247.cossh.myqcloud.com/split.png'
    }

    files['image'] = base64.b64encode(open("split"+num+".png",'rb').read()).decode()
    headers = {
    "Referer":"https://cloud.tencent.com/act/event/ci_demo.html",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
    ,'Host': 'recognition.image.myqcloud.com',
           "Content-Type":"application/json",
           "Authorization": get_sign(bucket)
           }
    #files = {"image":open("split.png", "rb").read()}
    r = requests.post(url,data=json.dumps(files),headers = headers)
    r_index = r'"itemstring":"(.*?)"'
    result = re.findall(r_index,r.content.decode("utf-8"))
    return result

def get_sign(bucket, howlong=30):
        """ GET REUSABLE SIGN
        :param bucket: 图片处理所使用的 bucket
        :param howlong: 签名的有效时长，单位 秒
        :return: 签名字符串
        """
        
        if howlong <= 0:
            raise Exception('Param howlong must be great than 0')

        now = int(time.time())
        rdm = random.randint(0, 999999999)

        text = 'a='+appid + '&b='+bucket + '&k='+secret_id + '&e='+str(now+howlong) + '&t='+str(now) + '&r='+str(rdm) + '&f='
        hexstring = hmac.new(secret_key.encode('utf-8'), text.encode('utf-8'), hashlib.sha1).hexdigest()
        binstring = binascii.unhexlify(hexstring)
        return base64.b64encode(binstring+text.encode('utf-8')).rstrip()

