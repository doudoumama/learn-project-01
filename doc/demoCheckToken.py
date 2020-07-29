# -*- coding: utf-8 -*-
import datetime
import hashlib
import hmac
import base64
import json
import requests
import random

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def httpRequest(bodyMd5, nonce, secretId, secretKey, data):
    dateTime = datetime.datetime.utcnow().strftime(GMT_FORMAT)

    auth = "hmac id=\"" + secretId + "\", algorithm=\"hmac-sha1\", headers=\"x-date x-sr-authorization x-sr-nonce x-sr-secretid\", signature=\""

    signStr = "x-date: " + dateTime + "\n" + "x-sr-authorization: " + bodyMd5 + "\n" + "x-sr-nonce: " + nonce + "\n" + "x-sr-secretid: " + secretId
    signature = hmac.new(secretKey, signStr, hashlib.sha1).digest()
    signature = base64.b64encode(signature)
    sign = auth + signature + "\""

    print(sign)

    url = 'https://service-7lf0ujt4-1258801057.gz.apigw.tencentcs.com/release/api/uma/v1/verifyToken'
    headers = {
        "X-NameSpace-Code": "uma-dev",
        "X-MicroService-Name": "uma-shop-api-web",
        "Content-Type": "application/json",
        "X-Date": dateTime,
        "x-sr-authorization": bodyMd5,
        "x-sr-nonce": nonce,
        "x-sr-secretid": secretId,
        "Authorization": sign
    }
    response = requests.post(url=url, headers=headers, data=data)

    ret = response.text.encode('UTF-8')
    print(ret)

data = {
    "token": "xxx",
}
secretId = 'AKIDJ5WivaiE4g18gfUbuBMheea9nRsI1807orvD'
secretKey = '1m5Jsk2aj86R3Mw5S8ork8h3wzsv3y9mtk5y8yM1'
bodyMd5 = hashlib.md5(json.dumps(data)).hexdigest()
nonce = 'tgshdy987uyjh765'

httpRequest(bodyMd5, nonce, secretId, secretKey, json.dumps(data))

