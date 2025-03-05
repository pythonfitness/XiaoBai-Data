import csv
from fake_useragent import UserAgent
import os
from utils.request_utils import get_json_data
from config import HEADERS, FORMAT_URL, OUTPUT_DIR, TRAVERSE_SORTING, PRODUCT_IDS, DEDUPLICATION
import time

def remove_duplicates(input_file, output_file):
    # 用于存储已经出现过的行
    unique_rows = set()
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        # 创建 CSV 读取器和写入器对象
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        # 读取并写入表头
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            # 将行转换为元组，因为集合只能存储可哈希的对象
            row_tuple = tuple(row)
            if row_tuple not in unique_rows:
                # 如果行未出现过，则添加到集合中并写入新文件
                unique_rows.add(row_tuple)
                writer.writerow(row)
def get_comment_data(format_url, product_id, i, max_page, output_file):
    """
    获取商品评论数据
    :param format_url: 格式化的字符串架子，在循环中给它添上参数
    :param product_id: 商品标识唯一的商品号
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
            url = format_url.format(product_id, i, cur_page)
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
                        'referenceName': comment['referenceName']  # 型号
                    }
                    writer.writerow(row)
            else:
                cur_page -= 1
                print('网络故障或者是网页出现了问题，五秒后重新连接')
                time.sleep(5)

def main():
    for k, product_id in enumerate(PRODUCT_IDS, start=1):
        ua = UserAgent()
        headers = HEADERS.copy()
        headers["User-Agent"] = ua.random

        if TRAVERSE_SORTING:
            print('设置遍历全部排序方式')
            sortings = range(7)
        else:
            print('设置只爬取全部评论')
            sortings = [0]  # 只按全部评论排序

        for i in sortings:
            if i == 6:
                continue
            print(f'正在爬取第{k}个商品,第{i + 1}种排序方式,{product_id}')
            # 先访问第0页获取最大页数，再进行循环遍历
            url = FORMAT_URL.format(product_id, i, 0)
            json_data = get_json_data(url, headers)
            if json_data:
                print("最大页数%s" % json_data['maxPage'])
                output_file = os.path.join(OUTPUT_DIR, f'jd_comment_{product_id}.csv')
                get_comment_data(FORMAT_URL, product_id, i, json_data['maxPage'], output_file)  # 遍历每一页
            else:
                print('网络故障或者是网页出现了问题，重新连接')
                continue
        if DEDUPLICATION:
            print(f'正在去重第{k}个商品')
            remove_duplicates(os.path.join(OUTPUT_DIR, f'jd_comment_{product_id}.csv'),
                              os.path.join(OUTPUT_DIR, f'jd_comment_{product_id}_deduplication.csv'))

if __name__ == "__main__":
    main()