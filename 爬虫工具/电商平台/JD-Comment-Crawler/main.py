import csv
from fake_useragent import UserAgent
import os
from utils.request_utils import get_json_data
from config import HEADERS, FORMAT_URL, OUTPUT_DIR, TRAVERSE_SORTING, PRODUCT_URLS

def get_comment_data(format_url, proc, i, max_page, output_file):
    """
    获取商品评论数据
    :param format_url: 格式化的字符串架子，在循环中给它添上参数
    :param proc: 商品的productID，标识唯一的商品号
    :param i: 商品的排序方式，例如全部商品、晒图、追评、好评等
    :param max_page: 商品的评论最大页数
    :param output_file: 输出的 CSV 文件路径
    """
    ua = UserAgent()
    headers = HEADERS.copy()
    headers["User-Agent"] = ua.random

    # 检查文件是否存在，如果不存在则写入表头
    file_exists = os.path.isfile(output_file)
    with open(output_file, 'a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['userId', 'content', 'boughtTime', 'voteCount', 'replyCount', 'starStep', 'creationTime',
                      'referenceName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        cur_page = 0
        while cur_page < max_page:
            cur_page += 1
            url = format_url.format(proc, i, cur_page)
            json_data = get_json_data(url, headers)
            if json_data:
                page_len = len(json_data['comments'])
                print(f"当前第{cur_page}页")
                for j in range(0, page_len):
                    comment = json_data['comments'][j]
                    row = {
                        'userId': comment['id'],  # 用户ID
                        'content': comment['content'],  # 评论内容
                        'boughtTime': comment['referenceTime'],  # 购买时间
                        'voteCount': comment['usefulVoteCount'],  # 点赞数
                        'replyCount': comment['replyCount'],  # 回复数目
                        'starStep': comment['score'],  # 得分
                        'creationTime': comment['creationTime'],  # 评价时间
                        'referenceName': comment['referenceName']  # 手机型号
                    }
                    writer.writerow(row)
            else:
                cur_page -= 1
                print('网络故障或者是网页出现了问题，五秒后重新连接')

def main():
    for k, text in enumerate(PRODUCT_URLS, start=1):
        product_id = 'productId=' + text.replace("https://item.jd.com/", "").replace(".html", "")
        ua = UserAgent()
        headers = HEADERS.copy()
        headers["User-Agent"] = ua.random

        if TRAVERSE_SORTING:
            sortings = range(7)
        else:
            sortings = [0]  # 只按全部评论排序

        for i in sortings:
            if i == 6:
                continue
            print(f'正在爬取第{k}个商品,第{i + 1}个排序方式,{product_id}')

            # 先访问第0页获取最大页数，再进行循环遍历
            url = FORMAT_URL.format(product_id, i, 0)
            json_data = get_json_data(url, headers)
            if json_data:
                print("最大页数%s" % json_data['maxPage'])
                output_file = os.path.join(OUTPUT_DIR, f'jd_comment_{product_id.split("=")[1]}_{i}.csv')
                get_comment_data(FORMAT_URL, product_id, i, json_data['maxPage'], output_file)  # 遍历每一页
                if json_data['maxPage'] < 100:
                    print('评论数过少，无需遍历排序方式')
                    break
            else:
                print('网络故障或者是网页出现了问题，重新连接')
                continue

if __name__ == "__main__":
    main()