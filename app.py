import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog
from tkinter import messagebox
import os
from dee.tasks import DEETask, DEETaskSetting
import crawler.run_crawler as clr
import subprocess
import sys
import json


def get_all_items(directory_path):
    try:
        # 获取指定路径下的所有文件和文件夹名，并返回完整路径
        all_items = [os.path.join(directory_path, item) for item in os.listdir(directory_path)]
        return all_items
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def extract(doc, dataset, mode):
    if mode == 'LSTM':
        bert_model_dir = r"G:/Pretrain_model/pytorch/bert-base-chinese"
        if dataset == 'Ch-Fin-Ann':
            task_dir = "Exps/PTPCG_R1_reproduction"
            resume = 62
        elif dataset == 'Duee-Fin':
            task_dir = "Exps/LSTM_dueefin"
            resume = 93
    elif mode == 'BERT':
        bert_model_dir = r"G:/Pretrain_model/pytorch/bert-base-chinese"
        if dataset == 'Ch-Fin-Ann':
            task_dir = "Exps/PTPCG_BERT"
            resume = 82
        elif dataset == 'Duee-Fin':
            task_dir = "Exps/BERT_dueefin"
            resume = 79
    elif mode == 'BERT-wwm':
        bert_model_dir = r"G:/Pretrain_model/pytorch/chinese-bert-wwm-ext"
        if dataset == 'Ch-Fin-Ann':
            task_dir = "Exps/PTPCG_BERT_wwm"
            resume = 35  # 测试用，待修改
        elif dataset == 'Duee-Fin':
            task_dir = "Exps/"
            resume = 0
    elif mode == 'RoBERTa':
        bert_model_dir = r"G:/Pretrain_model/pytorch/chinese-roberta-base"
        if dataset == 'Ch-Fin-Ann':
            task_dir = "Exps/PTPCG_RoBERTa"
            resume = 95
        elif dataset == 'Duee-Fin':
            task_dir = "Exps/RoBERTa_dueefin"
            resume = 65
    elif mode == 'RoBERTa-wwm':
        bert_model_dir = r"G:/Pretrain_model/pytorch/chinese-roberta-wwm-ext"
        if dataset == 'Ch-Fin-Ann':
            task_dir = "Exps/PTPCG_RoBERTa_wwm"
            resume = 51
        elif dataset == 'Duee-Fin':
            task_dir = "Exps/RoBERTa_wwm_dueefin"
            resume = 92
    elif mode == 'Fin-BERT':
        bert_model_dir = r"G:/Pretrain_model/pytorch/finbert-base-chinese"
        if dataset == 'Ch-Fin-Ann':
            task_dir = "Exps/PTPCG_FinBERT"
            resume = 88
        elif dataset == 'Duee-Fin':
            task_dir = "Exps/FinBERT_dueefin"
            resume = 100

    cpt_file_name = "TriggerAwarePrunedCompleteGraph"

    dee_setting = DEETaskSetting.from_pretrained(
        os.path.join(task_dir, f"{cpt_file_name}.task_setting.json")
    )
    dee_setting.local_rank = -1
    dee_setting.filtered_data_types = "o2o,o2m,m2m,unk"
    dee_setting.bert_model = bert_model_dir
    dee_task = DEETask(
        dee_setting,
        load_train=False,
        load_dev=False,
        load_test=False,
        load_inference=False,
        parallel_decorate=False,
    )
    dee_task.resume_cpt_at(resume)
    results = dee_task.predict_one(doc)
    return results


global dat
global items
global index
index = 0

root = ttk.Window(
        title="Fin-PTPCG事件抽取",        # 设置窗口的标题
        themename="litera",     # 设置主题
        size=(1080, 1200),        # 窗口的大小
        position=(100, 100),     # 窗口所在的位置
        minsize=(0, 0),          # 窗口的最小宽高
        maxsize=(3840, 2160),    # 窗口的最大宽高
        resizable=None,         # 设置窗口是否可以更改大小
        alpha=1.0,              # 设置窗口的透明度(0.0完全透明）
        )
crawler_window = ttk.Frame(root)
main_window = ttk.Frame(root)
auto_window = ttk.Frame(root)
train_window = ttk.Frame(root)
cur_frame = 0

#  文本框
# f = ttk.Frame(main_window).grid(padx=10, pady=10, row=0, column=0, columnspan=7)
text_content = "证券代码：000605证券简称：渤海股份公告编号：2018-062\n\
        渤海水业股份有限公司关于持股5%以上股东股份补充质押的公告\n\
        本公司及董事会全体成员保证信息披露的内容真实、准确和完整，没有虚假记载、误导性陈述或重大遗漏。\n\
        近日，渤海水业股份有限公司（以下简称“公司”）收到公司持股5%以上股东李华青女士的《告知函》，获悉李华青女士将其所持有的部分公司股票进行补充质押，具体事项如下：\n\
        一、股份质押基本情况\n\
        1.基本情况\n\
        公司于2017年12月8日披露了《关于持股5%以上股东股份质押的公告》，李华青女士于2017年12月7日将其持有的公司12151000股股份质押。\n\
        2018年7月11日，公司完成资本公积转增股本，转增方案为每10股转增4股，本次资本公积转增股本完成后，李华青女士质押的股份由12151000股变更为17011400股。\n\
        由于质押股份的市值减少，根据李华青女士与海通证券股份有限公司（以下简称“海通证券”）的约定，李华青女士向海通证券补充质押公司股份1188600股，该笔补充质押已于2018年9月6日在中国证券登记结算有限责任公司办理了相关登记手续。\n\
        本次补充质押的1188600股占李华青女士所持有的公司股份总数的5.25%，占公司总股本的0.34%。\n\
        2.股份累计质押情况\n\
        截至本公告发布之日，李华青女士持有公司股份22619999股（均为限售流通股），占公司总股本的比例为6.41%。\n\
        本次质押完成后，李华青女士累计质押的股份数为18200000股，占公司总股本的5.16%，占其持有公司股份总数的80.46%。\n\
        3.本次股权质押行为、内容、程序符合国家法律法规和有关部门的规章制度要求，且李华青女士具备相应的资金偿还能力，不存在被强制平仓或强制过户等风险。\n\
        二、备查文件\n\
        1.李华青女士出具的《关于股份补充质押的告知函》；\n\
        2.中国证券登记结算有限责任公司股份冻结明细。\n\
        特此公告。\n\
        渤海水业股份有限公司董事会\n\
        2018年9月7日"
text_content = "本钢板材控股股东本钢公司解除质押2.18亿股 新增质押1.1亿股\n\
        挖贝网10月17日，本钢板材（000761）今日发布公告，公司控股股东本溪钢铁（集团）有限责任公司向中国工商银行股份有限公司本溪分行质押1.1亿股，用于融资。\n\
        公告显示，控股股东本钢公司向国泰君安证券股份有限公司解除质押2.18亿股，解除质押占其所持股份比例9.15%，质押开始日期2016年9月28日，质押解除日期2019年10月16日，质押解除事由换股完成。\n\
        据了解，本钢板材本次质押股数1.1亿股，占其所持股份比例为4.75%，质押日期自2019年10月16日至2024年6月20日，质权人为中国工商银行股份有限公司本溪分行。\n\
        截至公告披露日，本钢公司持有本公司股份数为2,381,105,094股，占公司总股份数的61.44%；其中累计质押的股份数为624,264,469股，占公司总股份数的16.11%。\n\
        公司披露2019年半年度报告显示，2019年上半年归属于上市公司股东的净利润4.53亿元，比上年同期减少40.13%。"
st = ScrolledText(main_window, padding=5, height=17, autohide=True)
st.grid(padx=90, row=0, column=0, columnspan=7, sticky=W)
st.insert(END, text_content)

dataset = ttk.StringVar()
lab1 = ttk.Label(main_window, text='数据集：').grid(row=1, column=1, padx=30, pady=5, sticky="nsew")
cbo1 = ttk.Combobox(
            master=main_window,
            textvariable=dataset,
            bootstyle=INFO,
            font=("Times New Roman", 12),
            values=["Ch-Fin-Ann", "Duee-Fin"]
        )
cbo1.current(1)
cbo1.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

lab2 = ttk.Label(main_window, text='模型：').grid(row=2, column=1, padx=30, pady=5, sticky="nsew")
mode = ttk.StringVar()
cbo2 = ttk.Combobox(
            master=main_window,
            textvariable=mode,
            bootstyle=INFO,
            font=("Times New Roman", 12),
            values=["LSTM", "BERT", "BERT-wwm", "RoBERTa", "RoBERTa-wwm", "Fin-BERT"]
        )
cbo2.current(5)
cbo2.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")


#  按钮功能
def submit():
    if cur_frame == 0:
        # 获取输入框和下拉选项框中的值
        st2.delete("0.0", 'end')
        input_value = st.get(1.0, "end")
        input_value = input_value.replace("(以上内容每个颜色的标注代表一个事件的论元，这种颜色的标注代表多个事件的共享论元)", "")
        if len(input_value) <= 1:  # 输入为空
            messagebox.showinfo("输入为空", "请输入待处理的文本！")
        st.delete("0.0", 'end')
        dataset_value = dataset.get()
        mode_value = mode.get()

        # 在结果展示框中显示输入框和下拉选项框中的值
        res = extract(input_value, dataset_value, mode_value)
        # print(res)
        mspans = res["comments"]["mspans"]
        sentences = res["comments"]["sentences"]
        for s in sentences:
            st.insert(END, s)
            st.insert(END, '\n')
        st.insert(END, "\n(以上内容每个颜色的标注代表一个事件的论元，")
        st.insert(END, "这种颜色的标注", 'share')
        st.insert(END, "代表多个事件的共享论元)")
        if not len(res["event_list"]):
            st2.insert(END, 'No events in this text!\n')
        i = 1
        for events in res["event_list"]:
            if dataset_value == 'Ch-Fin-Ann':
                st2.insert(END, 'EVENT TYPE: ')
            else:
                st2.insert(END, '事件类型: ')
            st2.insert(END, events['event_type'])
            st2.insert(END, '\n')
            tag = "event" + str(i)
            for arg in events['arguments']:
                st2.insert(END, arg['role'])
                st2.insert(END, ': ')
                st2.insert(END, arg['argument'])
                st2.insert(END, '\n')

                for mspan in mspans:
                    if mspan["mspan"] == arg["argument"]:
                        index1 = str(mspan["drange"][0] + 1) + '.' + str(mspan["drange"][1])
                        index2 = str(mspan["drange"][0] + 1) + '.' + str(mspan["drange"][2])
                        flag = 0
                        for tmp in range(0, 13):
                            has_tag = st.tag_nextrange("event" + str(tmp), index1, index2)
                            if has_tag:
                                flag = 1
                        if not flag:
                            st.tag_add(tag, index1, index2)
                        else:
                            st.tag_add("share", index1, index2)
                        break
                    else:
                        continue
            st2.insert(END, '\n')
            i += 1
    elif cur_frame == 2:
        # 获取输入框和下拉选项框中的值
        auto_st2.delete("0.0", 'end')
        input_value = auto_st.get(1.0, "end")
        input_value = input_value.replace("(以上内容每个颜色的标注代表一个事件的论元，这种颜色的标注代表多个事件的共享论元)", "")
        if len(input_value) <= 1:  # 输入为空
            messagebox.showinfo("输入为空", "请输入待处理的文本！")
        auto_st.delete("0.0", 'end')
        dataset_value = auto_dataset.get()
        mode_value = auto_mode.get()

        # 在结果展示框中显示输入框和下拉选项框中的值
        res = extract(input_value, dataset_value, mode_value)
        global dat
        dat = res
        # print(res)
        mspans = res["comments"]["mspans"]
        sentences = res["comments"]["sentences"]
        for s in sentences:
            auto_st.insert(END, s)
            auto_st.insert(END, '\n')
        auto_st.insert(END, "\n(以上内容每个颜色的标注代表一个事件的论元，")
        auto_st.insert(END, "这种颜色的标注", 'share')
        auto_st.insert(END, "代表多个事件的共享论元)")
        if not len(res["event_list"]):
            auto_st2.insert(END, 'No events in this text!\n')
        i = 1
        for events in res["event_list"]:
            if dataset_value == 'Ch-Fin-Ann':
                auto_st2.insert(END, 'EVENT TYPE: ')
            else:
                auto_st2.insert(END, '事件类型: ')
            auto_st2.insert(END, events['event_type'])
            auto_st2.insert(END, '\n')
            tag = "event" + str(i)
            for arg in events['arguments']:
                auto_st2.insert(END, arg['role'])
                auto_st2.insert(END, ': ')
                auto_st2.insert(END, arg['argument'])
                auto_st2.insert(END, '\n')

                for mspan in mspans:
                    if mspan["mspan"] == arg["argument"]:
                        index1 = str(mspan["drange"][0] + 1) + '.' + str(mspan["drange"][1])
                        index2 = str(mspan["drange"][0] + 1) + '.' + str(mspan["drange"][2])
                        flag = 0
                        for tmp in range(0, 13):
                            has_tag = auto_st.tag_nextrange("event" + str(tmp), index1, index2)
                            if has_tag:
                                flag = 1
                        if not flag:
                            auto_st.tag_add(tag, index1, index2)
                        else:
                            auto_st.tag_add("share", index1, index2)
                        break
                    else:
                        continue
            auto_st2.insert(END, '\n')
            i += 1


def clear():
    if cur_frame == 0:
        st.delete("0.0", 'end')
        st2.delete("0.0", 'end')
    elif cur_frame == 2:
        auto_st.delete("0.0", 'end')
        auto_st2.delete("0.0", 'end')


def train_again():
    sh_file_path = r'G:\graduate\DocEE-main\scripts\run_main.sh'
    subprocess.run(['bash', sh_file_path])


def add_training():
    # 指定要追加数据的JSON文件路径
    json_file_path = r"G:\graduate\DocEE-main\Data\new\new_data.json"

    # 使用with语句打开文件，确保文件操作完成后正确关闭文件
    with open(json_file_path, 'a', encoding='utf-8') as json_file:
        # 使用json.dump将数据写入文件
        global dat
        json.dump(dat, json_file, ensure_ascii=False)
        # 写入一个换行，以确保下一个JSON对象在新行开始
        json_file.write('\n')

    auto_st.delete("0.0", 'end')
    auto_st2.delete("0.0", 'end')
    global index
    if index < len(items):
        index = index + 1
        f = open(items[index], encoding="GB18030")
        auto_st.insert(END, f.read())


def ignore_add():
    auto_st.delete("0.0", 'end')
    auto_st2.delete("0.0", 'end')
    global index
    if index < len(items):
        index = index + 1
        f = open(items[index], encoding="GB18030")
        auto_st.insert(END, f.read())


ttk.Button(master=main_window,
           text="清空信息",
           bootstyle=(INFO, OUTLINE),
           command=clear).grid(row=3, column=2, padx=0, pady=5, sticky=W)
ttk.Button(master=main_window,
           text="开始抽取",
           bootstyle=(INFO, OUTLINE),
           command=submit).grid(row=3, column=3, padx=0, pady=5, sticky=W)

text_content = ""

st2 = ScrolledText(main_window, padding=5, height=15, autohide=True)
st2.grid(padx=90, row=5, column=0, columnspan=8)

st2.insert(END, text_content)


'''
tag 属性
background color——背景色
bgstipple bitmap——背景位图
borderwidth pixels——边框宽度
elide boolean——指定是否应该删除数据。已删除的数据（字符、图像、嵌入的窗口等）不显示并且在屏幕上不占用空间，但进一步的行为与普通数据一样
fgstipple bitmap——前景位图
font fontName——字体
foreground color——前景色
justify justify——对齐方式 left, right, or center.
lmargin1 pixels——第一行左边边距
lmargin2 pixels——当一行内容过多而换行，换行的那些行的左边边距
lmargincolor color
offset pixels——指定文本基线应垂直偏移整行基线的量
overstrike boolean——删除线
overstrikefg color——删除线颜色
relief relief
rmargin pixels——右边距
rmargincolor color——右边距颜色
selectbackground color
selectforeground color
spacing1 pixels
spacing2 pixels
spacing3 pixels
tabs tabList
tabstyle style
underline boolean——是否设置下划线
underlinefg color——指定显示下划线时使用的颜色
wrap mode ——  none, char, or word

tag函数：
tag_add(tagName, index1, index2...)
为 index1 到 index2 之间的内容添加一个 Tag（tagName 参数指定）
如果 index2 参数忽略，则单独为 index1 指定的内容添加 Tag

tag_bind(tagName, sequence, func, add=None)
给tag绑定事件（sequence）
如 Enter, Leave, ButtonPress, Motion, and KeyPress 等事件

import tkinter as tk
import tkinter.messagebox
root = tk.Tk()
root.geometry('600x400')
tx = tk.Text(root)
tx.pack()
tx.tag_config('tg1',background='red',foreground='white',underline=True)
tx.insert('end','xxxxxxxxxx','tg1')
def show(event):
    tkinter.messagebox.showinfo(message='hello')
tx.tag_bind('tg1','<Enter>',show)
root.mainloop()
tag_unbind(tagName, sequence, funcid=None)


tag_cget(tagName, option)
返回 tagName 指定的 option 选项的值

tag_config(tagName, cnf=None, **kw)
配置一些属性：背景颜色，前景色，字体等等，可设置的属性在上面有提到
和tag_configure 一样

tag_delete(tagNames)
删除tags

tag_lower(tagName, belowThis=None)
降低 Tag 的优先级
如果 belowThis 参数不为空，则表示 tagName 需要比 belowThis 指定的 Tag 优先级更低

tag_raise(tagName, aboveThis=None)
提升Tag的优先级
如果 aboveThis 参数不为空，则表示 tagName 需要比 aboveThis 指定的 Tag 优先级更高

tag_names(index=None)
返回所有标签名称的列表

tag_nextrange(tagName, index1, index2=None)
在 index1 到 index2 的范围内第一个 tagName 的位置
如果没有则返回空字符串

tag_prevrange(tagName, index1, index2=None)
ag_nextrange() 的反向查找，也就是查找范围是 index2 到 index1
tag_ranges(tagName)
返回所有 tagName 指定的文本，并将它们的范围以列表的形式返回
tag_remove(tagName, index1, index2=None)
删除 index1 到 index2 之间所有的 tagName
如果忽略 index2 参数，那么只删除 index1 指定的那个字符的 tagName
'''
st.tag_configure("event1", foreground="#060500", background="#FB9B69")
st.tag_configure("event2", foreground="#FFFF00", background="#8080C0")
st.tag_configure("event3", foreground="#EDEBE4", background="#417CA9")
st.tag_configure("event4", foreground="#F2EBE7", background="#AE9AAB")
st.tag_configure("event5", foreground="#D5D360", background="#6671C0")
st.tag_configure("event6", foreground="#A73A50", background="#9FEFE2")
st.tag_configure("event7", foreground="#C6EDEC", background="#7379B0")
st.tag_configure("event8", foreground="#FFFFFF", background="#336699")
st.tag_configure("event9", foreground="#FFFFFF", background="#479AC7")
st.tag_configure("event10", foreground="#FFFFFF", background="#00B271")
st.tag_configure("event11", foreground="#000000", background="#D7FFF0")
st.tag_configure("event12", foreground="#F9ECDF", background="#825855")
st.tag_configure("share", foreground="#000000", background="#F0DAD2")


def start_crawler():
    clr.tp = crawler_entry1.get()
    if crawler_cbo2.get() == "True":
        clr.istxt = True
    else:
        clr.istxt = False
    clr.pth = crawler_entry3.get()
    clr.crawler()


def app_extraction():
    crawler_window.grid_remove()
    auto_window.grid_remove()
    train_window.grid_remove()
    main_window.grid()
    global cur_frame
    cur_frame = 0


def app_crawler():
    main_window.grid_remove()
    auto_window.grid_remove()
    train_window.grid_remove()
    crawler_window.grid()
    global cur_frame
    cur_frame = 1


def auto_extraction():
    crawler_window.grid_remove()
    main_window.grid_remove()
    train_window.grid_remove()
    auto_window.grid()
    global cur_frame
    cur_frame = 2
    directory_path = r"G:\金融竞赛\dataset\利空\\"
    global items
    items = get_all_items(directory_path)


def train_model():
    crawler_window.grid_remove()
    main_window.grid_remove()
    auto_window.grid_remove()
    train_window.grid()
    global cur_frame
    cur_frame = 3


#  顶部菜单拦
def open_file():   # 导入文件函数
    filename = filedialog.askopenfilename()
    f = open(filename, encoding="GB18030")
    if cur_frame == 0:
        st.delete("0.0", 'end')
        st.insert(END, f.read())
    elif cur_frame == 2:
        auto_st.delete("0.0", 'end')
        auto_st.insert(END, f.read())


crawler_lab0 = ttk.Label(crawler_window, text='爬虫参数设置：')
crawler_lab0.grid(row=0, column=0, padx=30, pady=5, sticky="nsew")
crawler_lab1 = ttk.Label(crawler_window, text='爬取新闻条数：')
crawler_lab1.grid(row=1, column=0, padx=30, pady=5, sticky="nsew")
crawler_entry1 = ttk.Entry(crawler_window, width=50, bootstyle=PRIMARY)
crawler_entry1.grid(row=1, column=1, padx=30, pady=5, sticky="nsew")
crawler_lab2 = ttk.Label(crawler_window, text='是否生成txt文件：')
crawler_lab2.grid(row=2, column=0, padx=30, pady=5, sticky="nsew")
# crawler_entry2 = ttk.Entry(crawler_window, width=50, bootstyle=PRIMARY)
# crawler_entry2.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")
crawler_cbo2 = ttk.Combobox(
            master=crawler_window,
            textvariable="True",
            bootstyle=PRIMARY,
            # font=("Times New Roman", 12),
            values=["True", "False"]
        )
crawler_cbo2.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")
crawler_lab3 = ttk.Label(crawler_window, text='默认路径：')
crawler_lab3.grid(row=3, column=0, padx=30, pady=5, sticky="nsew")
crawler_entry3 = ttk.Entry(crawler_window, width=50, bootstyle=PRIMARY)
crawler_entry3.grid(row=3, column=1, padx=30, pady=5, sticky="nsew")
crawler_entry3.insert('0', r'G://graduate//DocEE-main//crawler//data')
# crawler_text = ttk.ScrolledText(crawler_window, wrap=tk.WORD)
ttk.Button(master=crawler_window,
           text="开始爬取",
           bootstyle=(INFO, OUTLINE),
           command=start_crawler).grid(row=4, column=0, padx=5, pady=5, sticky=W)
# crawler_text.grid(row=5, column=0, columnspan=3, padx=30, pady=5, sticky="nsew")

train_lab0 = ttk.Label(train_window, text='训练参数设置：')
train_lab0.grid(row=0, column=0, padx=30, pady=5, sticky="nsew")
'''
train_lab1 = ttk.Label(train_window, text='训练事件类型数：')
train_lab1.grid(row=1, column=0, padx=30, pady=5, sticky="nsew")
train_cbo1 = ttk.Combobox(
            master=train_window,
            textvariable=dataset,
            bootstyle=PRIMARY,
            # font=("Times New Roman", 12),
            values=["5类事件", "13类事件"]
        )
train_cbo1.current(1)
train_cbo1.grid(row=1, column=1, padx=30, pady=5, sticky="nsew")
'''
train_lab2 = ttk.Label(train_window, text='Epoch数：')
train_lab2.grid(row=2, column=0, padx=30, pady=5, sticky="nsew")
train_entry2 = ttk.Entry(train_window, width=50, bootstyle=PRIMARY)
train_entry2.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")

train_lab3 = ttk.Label(train_window, text='batch size：')
train_lab3.grid(row=3, column=0, padx=30, pady=5, sticky="nsew")
train_entry3 = ttk.Entry(train_window, width=50, bootstyle=PRIMARY)
train_entry3.grid(row=3, column=1, padx=30, pady=5, sticky="nsew")

train_lab4 = ttk.Label(train_window, text='learning rate：')
train_lab4.grid(row=4, column=0, padx=30, pady=5, sticky="nsew")
train_entry4 = ttk.Entry(train_window, width=50, bootstyle=PRIMARY)
train_entry4.grid(row=4, column=1, padx=30, pady=5, sticky="nsew")

train_lab5 = ttk.Label(train_window, text='dropout：')
train_lab5.grid(row=5, column=0, padx=30, pady=5, sticky="nsew")
train_entry5 = ttk.Entry(train_window, width=50, bootstyle=PRIMARY)
train_entry5.grid(row=5, column=1, padx=30, pady=5, sticky="nsew")

train_lab6 = ttk.Label(train_window, text='模型triggers个数：')
train_lab6.grid(row=6, column=0, padx=30, pady=5, sticky="nsew")
train_entry6 = ttk.Entry(train_window, width=50, bootstyle=PRIMARY)
train_entry6.grid(row=6, column=1, padx=30, pady=5, sticky="nsew")

ttk.Button(master=train_window,
           text="开始训练",
           bootstyle=(INFO, OUTLINE),
           command=train_again).grid(row=9, column=1, padx=0, pady=5, sticky=W)


menubar = ttk.Menu(root)  # 创建顶层菜单
filemenu1 = ttk.Menu(menubar)  # 创建子菜单
menubar.add_cascade(label='文件', menu=filemenu1)  # 关联级联菜单
filemenu1.add_command(label='导入文件', command=open_file)  # 子菜单中添加菜单项
filemenu1.add_separator()  # 分割线
filemenu2 = ttk.Menu(menubar)  # 创建子菜单
menubar.add_cascade(label='模式选择', menu=filemenu2)  # 关联级联菜单
filemenu2.add_command(label='单篇抽取模式', command=app_extraction)  # 子菜单中添加菜单项
filemenu2.add_command(label='爬虫模式', command=app_crawler)  # 子菜单中添加菜单项
filemenu2.add_command(label='自动抽取模式', command=auto_extraction)  # 子菜单中添加菜单项
filemenu2.add_command(label='模型训练', command=train_model)  # 子菜单中添加菜单项
root.config(menu=menubar)  # 关联窗口

main_window.grid()

auto_dataset = ttk.StringVar()
auto_st = ScrolledText(auto_window, padding=5, height=17, autohide=True)
auto_st.grid(padx=90, row=0, column=0, columnspan=7, sticky=W)
auto_st.insert(END, text_content)

auto_st.tag_configure("event1", foreground="#060500", background="#FB9B69")
auto_st.tag_configure("event2", foreground="#FFFF00", background="#8080C0")
auto_st.tag_configure("event3", foreground="#EDEBE4", background="#417CA9")
auto_st.tag_configure("event4", foreground="#F2EBE7", background="#AE9AAB")
auto_st.tag_configure("event5", foreground="#D5D360", background="#6671C0")
auto_st.tag_configure("event6", foreground="#A73A50", background="#9FEFE2")
auto_st.tag_configure("event7", foreground="#C6EDEC", background="#7379B0")
auto_st.tag_configure("event8", foreground="#FFFFFF", background="#336699")
auto_st.tag_configure("event9", foreground="#FFFFFF", background="#479AC7")
auto_st.tag_configure("event10", foreground="#FFFFFF", background="#00B271")
auto_st.tag_configure("event11", foreground="#000000", background="#D7FFF0")
auto_st.tag_configure("event12", foreground="#F9ECDF", background="#825855")
auto_st.tag_configure("share", foreground="#000000", background="#F0DAD2")

auto_lab1 = ttk.Label(master=auto_window, text='数据集：').grid(row=1, column=1, padx=30, pady=5, sticky="nsew")
auto_cbo1 = ttk.Combobox(
            master=auto_window,
            textvariable=auto_dataset,
            bootstyle=INFO,
            font=("Times New Roman", 12),
            values=["Ch-Fin-Ann", "Duee-Fin"]
        )
auto_cbo1.current(1)
auto_cbo1.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
auto_lab2 = ttk.Label(auto_window, text='模型：').grid(row=2, column=1, padx=30, pady=5, sticky="nsew")
auto_mode = ttk.StringVar()
auto_cbo2 = ttk.Combobox(
            master=auto_window,
            textvariable=auto_mode,
            bootstyle=INFO,
            font=("Times New Roman", 12),
            values=["LSTM", "BERT", "BERT-wwm", "RoBERTa", "RoBERTa-wwm", "Fin-BERT"]
        )
auto_cbo2.current(5)
auto_cbo2.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")


ttk.Button(master=auto_window,
           text="清空信息",
           bootstyle=(INFO, OUTLINE),
           command=clear).grid(row=3, column=2, padx=0, pady=5, sticky=W)
ttk.Button(master=auto_window,
           text="开始抽取",
           bootstyle=(INFO, OUTLINE),
           command=submit).grid(row=3, column=3, padx=0, pady=5, sticky=W)
text_content = ""

auto_st2 = ScrolledText(auto_window, padding=5, height=15, autohide=True)
auto_st2.grid(padx=90, row=5, column=0, columnspan=8)

auto_st2.insert(END, text_content)

ttk.Button(master=auto_window,
           text="赞同",
           bootstyle=(SUCCESS, OUTLINE),
           command=add_training).grid(row=6, column=2, padx=0, pady=5, sticky=W)
ttk.Button(master=auto_window,
           text="不赞同",
           bootstyle=(DANGER, OUTLINE),
           command=ignore_add).grid(row=6, column=3, padx=0, pady=5, sticky=W)

root.mainloop()
