import argparse
from crawler.sina_news import sinanews


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', default=10, type=int, help='设置爬虫爬取新闻条数')
    parser.add_argument('--is_txt', default=True, type=bool, help='是否生成txt文件')

    parser.add_argument('--path', default='./data', type=str, help='数据文件存储路径')
    return parser.parse_args()


def crawler():import argparse
from crawler.sina_news import sinanews

global tp
global istxt
global pth
global flag
flag = 1


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', default=10000, type=int, help='设置爬虫爬取新闻条数')
    parser.add_argument('--is_txt', default=True, type=bool, help='是否生成txt文件')
    parser.add_argument('--path', default='./data', type=str, help='数据文件存储路径')
    if flag:
        parser.set_defaults(top=tp)
        parser.set_defaults(is_txt=istxt)
        parser.set_defaults(path=pth)

    return parser.parse_args()


def crawler():
    # 爬取新浪财经信息
    args = set_args()
    sinanews.get_rolling_news_csv(top=args.top, get_content=True, classify='财经',
                                  path=args.path, is_txt=args.is_txt)


if __name__ == '__main__':

    crawler()

    # 爬取新浪财经信息
    args = set_args()
    sinanews.get_rolling_news_csv(top=args.top, get_content=True, classify='财经',
                                  path=args.path, is_txt=args.is_txt)


if __name__ == '__main__':

    crawler()
