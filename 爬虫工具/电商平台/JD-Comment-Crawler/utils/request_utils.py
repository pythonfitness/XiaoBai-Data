import requests
import json
import time
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import warnings

# 禁用安全请求警告
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

def get_json_data(url, headers):
    """
    发送请求并获取JSON数据
    :param url: 请求的URL
    :param headers: 请求头
    :return: JSON数据
    """
    try:
        response = requests.get(url=url, headers=headers, verify=False)
        time.sleep(random.uniform(0.5, 2))
        json_data = response.text
        start_loc = json_data.find('{')
        json_data = json_data[start_loc:-2]
        return json.loads(json_data)
    except Exception as e:
        print(f"请求出错: {e}")
        time.sleep(3)
        return None