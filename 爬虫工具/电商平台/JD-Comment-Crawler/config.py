import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据目录
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

# 请求头
HEADERS = {
    'Accept': '*/*',
    'Host': "club.jd.com",
    'sec-ch-ua': "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
}

# 格式化的URL
FORMAT_URL = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={0}&score={1}&sortType=5&page={2}&pageSize=10&isShadowSku=0&fold=1'

# 配置项：是否遍历评论排序方式
TRAVERSE_SORTING = False

# 配置项：是否去重
DEDUPLICATION = True

# 配置项：爬取间隔区间
MIN_SLEEP_INTERVAL = 0.5
MAX_SLEEP_INTERVAL = 1.5

# 商品URL列表
PRODUCT_IDS = [
    "100144482372",  # 替换为实际的商品URL
    # 可以添加更多的商品URL
]