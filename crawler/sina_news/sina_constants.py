# -*- coding: gbk -*-

template_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num={}&page={}&r={}'

lid2classification = {
    "2509": "ȫ��",
    "2510": "����",
    "2511": "����",
    "2669": "���",
    "2512": "����",
    "2513": "����",
    "2514": "����",
    "2515": "�Ƽ�",
    "2516": "�ƾ�",
    "2517": "����",
    "2518": "����",
    "2968": "����_����",
    "2970": "����_���",
    "2972": "����_���",
    "2974": "���ڹ������"
}
classification2lid = dict((v, k) for k, v in lid2classification.items())
classifications = list(lid2classification.values())  # �������
max_num_per_page = 50

columns = ['title', 'time', 'url', 'wapurl', 'media_name', 'keywords', 'content']
