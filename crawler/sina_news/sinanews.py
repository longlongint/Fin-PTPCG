# -*- coding: gbk -*-
"""
新浪新闻数据接口
"""

import re
import os
import json
import random
import sys

import lxml.html
import lxml.etree
import pandas as pd
from datetime import datetime

from crawler.sina_news import sina_constants as cts
from crawler.sina_news.utils.downloader import Downloader
from crawler.sina_news.utils.disk_cache import DiskCache

no_cache_downloader = Downloader(cache=None)
disk_cache_downloader = Downloader(cache=DiskCache())


def get_date():
    # 获取当前日期，格式YYYY-MM-DD
    cur_date = datetime.now().strftime('%Y-%m-%d')
    return cur_date


def data_cleaning():

    return


def get_rolling_news_csv(top=50, get_content=True, classify=None, path='../data', is_txt=False):
    """
    获取新浪滚动新闻并保存成csv文件
    :param top: int, 获取的滚动新闻条数，默认为50
    :param get_content: bool, 是否获取新闻内容，默认为True
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :param path: str, 文件保存路径
    """
    df = get_rolling_news(top=top, get_content=get_content, classify=classify, savepath=path, is_txt=is_txt)

    df_path = path + '/全部.csv'
    df.to_csv(df_path, index=False, encoding='gb18030')


def savetxt(path, filename, contents):
    """
    :param path: str, txt文件存储路径
    :param filename: str, txt文件命名
    :param contents: str, txt文件内容
    :return:
    """
    if not os.path.exists(path):
        # 如果路径不存在则创建
        os.makedirs(path)
    pth = path + '/' + filename + '.txt'

    file = open(pth, mode = 'w', encoding='gb18030')
    file.write(contents)
    file.close()
    return


def get_rolling_news(top=50, get_content=True, classify=None, savepath='../data', is_txt = False):
    """
    获取新浪滚动新闻
    :param top: int, 获取的滚动新闻条数，默认为50
    :param get_content: bool, 是否获取新闻内容，默认为True
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :return: pd.DataFrame, 新闻信息数据框
    """
    if classify:
        assert classify in cts.classifications, (
            '请设置 classify 为 {}中的一个'.format(cts.classifications)
        )

    lid = cts.classification2lid.get(classify, '2509')
    classify = cts.lid2classification[lid]
    num_list = [cts.max_num_per_page] * (top // cts.max_num_per_page)
    last_page_num = top % cts.max_num_per_page
    if last_page_num:
        num_list += [last_page_num]

    df_data = []
    com_data = []
    trade_data = []
    other_data = []
    all_data = []
    cnt = 1
    stock_list_path = savepath + '/stock_list.csv'
    stock_inf = pd.read_csv(stock_list_path, encoding='gb18030')
    stock_name = stock_inf.iloc[:,1]
    stock_trade = stock_inf.iloc[:,2]
    _lst = stock_trade.tolist()
    _set = set(_lst)
    stock_trade = list(_set)
    last_ct = datetime.now().strftime('%Y-%m-%d')
    for page, num in enumerate(num_list, start=1):
        r = random.random()
        url = cts.template_url.format(lid, num, page, r)
        response = no_cache_downloader(url)
        response_dict = json.loads(response)
        data_list = response_dict['result']['data']

        for data in data_list:
            ctime = datetime.fromtimestamp(int(data['ctime']))
            ct = datetime.strftime(ctime, '%Y-%m-%d')
            ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')

            url = data['url']
            row = [data['title'], ctime,
                   url, data['wapurl'], data['media_name'], data['keywords']]
            if get_content:
                row.append(get_news_content(url))
                path = savepath + '/' + ct
                com_path = path + '/公司'
                trade_path = path + '/行业'
                other_path = path + '/其他'
                title = data['title']  # 文章标题
                title = re.sub(r'[*,/|?:<>"\\\']', '', title)
                title = '%d-' % cnt + title
                cont = row[6] # 文章内容
                csvw = [data['title'], ctime, url, data['wapurl'], data['media_name'], data['keywords']]
                csvw.append(cont)
                flag = 1
                for i in range(len(stock_name)):
                    if stock_name[i] in cont:
                        if is_txt:
                            savetxt(com_path, title, cont)
                        com_data.append(csvw)
                        all_data.append(csvw)
                        flag = 0
                        break
                if flag:
                    for i in range(len(stock_trade)):
                        if stock_trade[i] in cont:
                            if is_txt:
                                savetxt(trade_path, title, cont)
                            trade_data.append(csvw)
                            all_data.append(csvw)
                            flag = 0
                            break
                if flag:
                    if is_txt:
                        savetxt(other_path, title, cont)
                    other_data.append(csvw)
                    all_data.append(csvw)
                cnt += 1
            if last_ct != ct or cnt == (top+1):
                # 下一天
                com = pd.DataFrame(com_data, columns=cts.columns if get_content else cts.columns[:-1])
                trade = pd.DataFrame(trade_data, columns=cts.columns if get_content else cts.columns[:-1])
                other = pd.DataFrame(other_data, columns=cts.columns if get_content else cts.columns[:-1])
                all = pd.DataFrame(all_data, columns=cts.columns if get_content else cts.columns[:-1])
                all_path = savepath + '/' + last_ct + '/%s-全部.csv'%last_ct
                com_path = savepath + '/' + last_ct + '/%s-公司.csv'%last_ct
                trade_path = savepath + '/' + last_ct + '/%s-行业.csv'%last_ct
                other_path = savepath + '/' + last_ct + '/%s-其他.csv'%last_ct
                com.to_csv(com_path, index=False, encoding='gb18030')
                trade.to_csv(trade_path, index=False, encoding='gb18030')
                other.to_csv(other_path, index=False, encoding='gb18030')
                all.to_csv(all_path, index=False, encoding='gb18030')
                sys.exit()
            df_data.append(row)

    df = pd.DataFrame(df_data, columns=cts.columns if get_content else cts.columns[:-1])

    return df


def get_rolling_news_url(top=50, classify=None):
    """
    获取新浪滚动新闻url
    :param top: int, 获取的滚动新闻条数，默认为50
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :return: pd.DataFrame, 新闻信息数据框
    """
    if classify:
        assert classify in cts.classifications, (
            '请设置 classify 为 {}中的一个'.format(cts.classifications)
        )

    lid = cts.classification2lid.get(classify, '2509')
    num_list = [cts.max_num_per_page] * (top // cts.max_num_per_page)
    last_page_num = top % cts.max_num_per_page
    if last_page_num:
        num_list += [last_page_num]

    urls = []
    for page, num in enumerate(num_list, start=1):
        r = random.random()
        url = cts.template_url.format(lid, num, page, r)
        response = no_cache_downloader(url)
        response_dict = json.loads(response)
        data_list = response_dict['result']['data']
        for data in data_list:
            url = data['url']
            urls.append(url)
    return urls


def get_news_content(url):
    """
    获取新闻内容
    :param url: str, 新闻链接
    :return: str, 新闻内容
    """
    content = ''
    try:
        text = disk_cache_downloader(url)
        html = lxml.etree.HTML(text)
        res = html.xpath('//*[@id="artibody" or @id="article"]//p')
        p_str_list = [lxml.etree.tostring(node).decode('gbk') for node in res]
        p_str = ''.join(p_str_list)
        html_content = lxml.html.fromstring(p_str)
        content = html_content.text_content()
        # 清理未知字符和空白字符
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', '', content)
        content = re.sub(r'\s*\n\s*', '', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = re.sub(r'\n', '', content)
        content = re.sub(r'\r', '', content)
        content = content.lstrip(r'炒股就看金麒麟分析师研报，权威，专业，及时，全面，助您挖掘潜力主题机会！')
        content = content.lstrip(r'下载新浪财经APP，查看更多资讯和大V观点')

        content = content.strip()
    except Exception as e:
        print('get_news_content(%s) error:' % url, e)
    return content


if __name__ == '__main__':
    get_rolling_news_csv(top=5, get_content=True, classify='财经',path='../data',is_txt=True)
