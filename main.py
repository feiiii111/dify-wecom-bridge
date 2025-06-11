from flask import Flask, request, jsonify
import hashlib
import xml.etree.ElementTree as ET
import base64
import requests
from Crypto.Cipher import AES
import time

# 你的配置信息
corp_id = "wweed97ce2866dcef7"
agent_id = "1000002"
secret = "YZIYmi6KUe-ZLeYkRMCoJg4Hac-m1LZezzma0Hnym4w"
token = "sIUrTFHqLxgPL4Y8y024ll"
encoding_aes_key = "lDyPMkYXdFdMkRHLLZrhTbL58C6rJzMzMAu3hUqdg32"
dify_base_url = "http://localhost:8088/v1"
dify_api_key = "app-kGw98rIUrP1YgQBr9HZ4l7Xq"

app = Flask(__name__)

@app.route('/wecom', methods=['POST'])
def wecom_callback():
    xml_data = request.data.decode('utf-8')
    xml_tree = ET.fromstring(xml_data)
    content = xml_tree.find('Content').text
    from_user = xml_tree.find('FromUserName').text

    # 传给 Dify Agent
    dify_headers = {
        "Authorization": f"Bearer {dify_api_key}",
        "Content-Type": "application/json"
    }
    dify_payload = {
        "inputs": {"query": content},
        "response_mode": "blocking"
    }
    response = requests.post(f"{dify_base_url}/chat-messages", json=dify_payload, headers=dify_headers)
    answer = response.json()['answer']

    # 发回企业微信
    send_wecom_message(from_user, answer)

    return "success"

def get_wecom_access_token():
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
    res = requests.get(url).json()
    return res['access_token']

def send_wecom_message(userid, content):
    access_token = get_wecom_access_token()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": userid,
        "msgtype": "text",
        "agentid": agent_id,
        "text": {"content": content},
        "safe": 0
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
