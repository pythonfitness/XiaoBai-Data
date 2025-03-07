import requests
import json
import time
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import warnings
from typing import Optional

# 禁用安全请求警告
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

def get_json_data(url: str, headers: dict) -> Optional[dict]:
    """
    发送带重试机制的HTTP请求获取JSON数据

    Args:
        url: 请求URL
        headers: 请求头字典

    Returns:
        dict: 解析后的JSON数据，失败返回None

    Raises:
        HTTPError: 当超过最大重试次数时抛出
    """
    retries = 3
    backoff_factor = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            response.raise_for_status()
            raw_data = response.text
            
            # 精确提取JSON部分
            json_start = raw_data.find('{')
            json_end = raw_data.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("Invalid JSON structure")
                
            return json.loads(raw_data[json_start:json_end])
        except (requests.exceptions.RequestException, json.JSONDecodeError, ValueError) as e:
            wait_time = backoff_factor * 2 ** attempt
            print(f"请求失败: {e}, {retries - attempt - 1}次重试中...")
            time.sleep(wait_time)
    print(f"请求失败: 超过最大重试次数{retries}")
    return None