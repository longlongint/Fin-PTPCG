# 金融资讯舆情分析 #

## 项目介绍 ##
&emsp;&emsp;本项目为第一届中国研究生金融科技创新大赛的算法挑战赛选题方向一的参赛项目，包含新闻爬取模块、预测模型模块

## 环境依赖 ##
```
python==3.7
lxml==4.8.0
pandas==1.3.5
pytorch==1.10.0
tqdm==4.64.0
transformers==4.16.2
tensorboardX==2.2
sklearn
```
安装依赖包：pip install -r requirements.txt   

## 目录结构 ##
```
│  run_crawler.py           // 爬虫程序入口
│  run_model.py             // 训练模型程序入口
│  predict.py               // 预测分类
│  args.py                  // 训练模型的参数
│  README.md
│  requirements.txt
│
├─cache                     // 缓存文件夹，爬取的网页缓存在此，若再次爬取到重复内容可直接读取缓存
├─data                      // 爬取的新闻文件存储路径
├─datasets                  // 训练/测试用数据集位置
├─logs                      // 训练模型产生的log文档，可用tensorboard打开
├─model                     // 训练所得的模型文件
├─sina_news
│  │  sinanews.py           // 爬虫主要程序
│  │  sina_constants.py
│  │  __init__.py
│  │  __version__.py
│  │
│  ├─utils                  // 工具文件夹
│  │  │  disk_cache.py
│  │  │  downloader.py
│  │  │  __init__.py
│  │  │

```
## 使用说明 ##
##### 新闻爬取:
```
python run_crawler.py [--top] [--is_txt] [--path]

方括号内数据为可选参数:   
    --top：爬取新浪滚动新闻最新的top条新闻，最大值为2500   
    --is_txt：是否生成txt类型数据，默认为True   
    --path: 数据文件存储路径，默认为程序根目录下./path文件夹，若不存在则新建   

爬取运行示例：python run_crawler.py --top 2500 --is_txt True --path ./data

程序会在path参数设定的目录下生成一个当前日期的文件夹，格式为YYYY-MM-DD，文件夹中有
三个子文件夹，是按照关键字将新闻内容进行了分类，分别是公司、行业、其他，txt格式的数据
存入其中。csv格式的数据存在日期文件夹目录下，每日生成公司、行业、其他、全部四个csv文件。
```
##### 模型训练:
```
1.下载预训练模型，如BERT-Base-Chinese
2.args.py文件是参数设置，修改默认参数或者在运行时修改
3.使用以下命令运行文件: 
  python run_model.py [--func] [--pretrain_model]
  方括号内数据为可选参数: 
      --func: 训练/验证/测试的选择
      --pretrain_model: 预训练模型的选择
```
##### 分类预测:
```
1.更改predict.py文件中的lab_path(输入路径)和path(输出路径)
2.python predict.py
```
## 版本更新 ##
##### 2022/07/11:
&emsp;&emsp;1.在参考 [此代码](https://github.com/Jacen789/rolling-news) 基础上，完成了爬取新闻的基础功能，仅保存参赛所需财经新闻   
&emsp;&emsp;2.添加了将新闻内容根据关键字分类的功能   
&emsp;&emsp;3.添加了可以生成txt格式数据的选项
##### 2022/07/16:
&emsp;&emsp;1.添加了可以限制爬取新闻的时间范围的功能(限制在程序运行当日)，超出限制则自动停止程序，避免重复获取信息存入不同路径造成冗余   
##### 2022/07/20:
&emsp;&emsp;1.修复了由于在爬虫程序运行中日期改变导致的程序运行异常的BUG   
&emsp;&emsp;2.修复了未到达当日0点就已经爬取结束的情况下不生成csv格式数据的BUG   
##### 2022/08/01:
&emsp;&emsp;1.添加了基于BERT的三分类预测模型，测试准确率约为72%
##### 2022/08/03:
&emsp;&emsp;1.使用基于标题的训练方式，提升测试准确率至82%
##### 2022/08/15:
&emsp;&emsp;1.在训练中使用10折交叉验证，提升测试准确率至86%    
&emsp;&emsp;2.添加了根据训练好的模型进行预测的功能    