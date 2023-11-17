# -*- coding: gbk -*-
"""
�����������ݽӿ�
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
    # ��ȡ��ǰ���ڣ���ʽYYYY-MM-DD
    cur_date = datetime.now().strftime('%Y-%m-%d')
    return cur_date


def data_cleaning():

    return


def get_rolling_news_csv(top=50, get_content=True, classify=None, path='../data', is_txt=False):
    """
    ��ȡ���˹������Ų������csv�ļ�
    :param top: int, ��ȡ�Ĺ�������������Ĭ��Ϊ50
    :param get_content: bool, �Ƿ��ȡ�������ݣ�Ĭ��ΪTrue
    :param classify: str, ��ȡ�Ĺ������ŵ����Ĭ��ΪNone����"2509:ȫ��"
    :param path: str, �ļ�����·��
    """
    df = get_rolling_news(top=top, get_content=get_content, classify=classify, savepath=path, is_txt=is_txt)

    df_path = path + '/ȫ��.csv'
    df.to_csv(df_path, index=False, encoding='gb18030')


def savetxt(path, filename, contents):
    """
    :param path: str, txt�ļ��洢·��
    :param filename: str, txt�ļ�����
    :param contents: str, txt�ļ�����
    :return:
    """
    if not os.path.exists(path):
        # ���·���������򴴽�
        os.makedirs(path)
    pth = path + '/' + filename + '.txt'

    file = open(pth, mode = 'w', encoding='gb18030')
    file.write(contents)
    file.close()
    return


def get_rolling_news(top=50, get_content=True, classify=None, savepath='../data', is_txt = False):
    """
    ��ȡ���˹�������
    :param top: int, ��ȡ�Ĺ�������������Ĭ��Ϊ50
    :param get_content: bool, �Ƿ��ȡ�������ݣ�Ĭ��ΪTrue
    :param classify: str, ��ȡ�Ĺ������ŵ����Ĭ��ΪNone����"2509:ȫ��"
    :return: pd.DataFrame, ������Ϣ���ݿ�
    """
    if classify:
        assert classify in cts.classifications, (
            '������ classify Ϊ {}�е�һ��'.format(cts.classifications)
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
                com_path = path + '/��˾'
                trade_path = path + '/��ҵ'
                other_path = path + '/����'
                title = data['title']  # ���±���
                title = re.sub(r'[*,/|?:<>"\\\']', '', title)
                title = '%d-' % cnt + title
                cont = row[6] # ��������
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
                # ��һ��
                com = pd.DataFrame(com_data, columns=cts.columns if get_content else cts.columns[:-1])
                trade = pd.DataFrame(trade_data, columns=cts.columns if get_content else cts.columns[:-1])
                other = pd.DataFrame(other_data, columns=cts.columns if get_content else cts.columns[:-1])
                all = pd.DataFrame(all_data, columns=cts.columns if get_content else cts.columns[:-1])
                all_path = savepath + '/' + last_ct + '/%s-ȫ��.csv'%last_ct
                com_path = savepath + '/' + last_ct + '/%s-��˾.csv'%last_ct
                trade_path = savepath + '/' + last_ct + '/%s-��ҵ.csv'%last_ct
                other_path = savepath + '/' + last_ct + '/%s-����.csv'%last_ct
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
    ��ȡ���˹�������url
    :param top: int, ��ȡ�Ĺ�������������Ĭ��Ϊ50
    :param classify: str, ��ȡ�Ĺ������ŵ����Ĭ��ΪNone����"2509:ȫ��"
    :return: pd.DataFrame, ������Ϣ���ݿ�
    """
    if classify:
        assert classify in cts.classifications, (
            '������ classify Ϊ {}�е�һ��'.format(cts.classifications)
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
    ��ȡ��������
    :param url: str, ��������
    :return: str, ��������
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
        # ����δ֪�ַ��Ϳհ��ַ�
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', '', content)
        content = re.sub(r'\s*\n\s*', '', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = re.sub(r'\n', '', content)
        content = re.sub(r'\r', '', content)
        content = content.lstrip(r'���ɾͿ����������ʦ�б���Ȩ����רҵ����ʱ��ȫ�棬�����ھ�Ǳ��������ᣡ')
        content = content.lstrip(r'�������˲ƾ�APP���鿴������Ѷ�ʹ�V�۵�')

        content = content.strip()
    except Exception as e:
        print('get_news_content(%s) error:' % url, e)
    return content


if __name__ == '__main__':
    get_rolling_news_csv(top=5, get_content=True, classify='�ƾ�',path='../data',is_txt=True)
