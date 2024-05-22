# Fin-PTPCG
论文[《基于Fin-BERT的中文金融领域事件抽取方法》](https://link.cnki.net/urlid/11.2127.TP.20231012.1517.002)的代码。
- [**Fin-PTPCG**](https://link.cnki.net/urlid/11.2127.TP.20231012.1517.002) 模型在[PTPCG](https://arxiv.org/abs/2112.06013)的基础上增加了Fin-BERT编码器，充分利用Fin-BERT预训练模型的表达能力，在编码阶段融入领域内的先验知识，并且在事件检测模块采用多个二元分类器叠加的方式，保证模型可以有效识别一篇文档内存在多事件的情况并筛除掉负面样例，抽取实体之后将实体连接成完全图并通过计算相似度矩阵进行剪枝，通过选择伪触发器解决无标注触发词的问题，最后接入事件分类器实现事件抽取。该方法在ChFinAnn和Duee-fin数据集上事件抽取任务的F1值相比于基线方法分别取得了0.7%和3.7%的提升。
- 本项目还提供了可视化交互页面和从互联网上下载金融新闻的功能 (本项目从互联网上下载的数据仅作为科研测试数据使用) ，后续版本会继续对此完善开发

## 复现实验
### 运行环境
- python 3.7
  - dgl==0.9.1
  - dgl_cu113==0.9.1
  - gpu_watchmen==0.3.8
  - Jinja2==3.1.2
  - loguru==0.5.3
  - lxml==4.9.3
  - matplotlib==3.5.3
  - networkx==2.6.3
  - numpy==1.21.6
  - pandas==1.1.5
  - pytest==7.4.3
  - pytorch_mcrf==0.0.3
  - scikit_learn==1.0.2
  - scipy==1.7.3
  - setuptools==63.4.1
  - tensorboardX==2.5.1
  - torch==1.12.1
  - tqdm==4.64.1
  - transformers==4.22.2
  - ttkbootstrap==1.10.1 
``` bash
# 安装指令：
pip install -r requirement.txt
```

### 数据处理
```bash
# ChFinAnn
## 数据集下载: https://github.com/dolphin-zs/Doc2EDAG
$ unzip Data.zip
$ cd Data
# 生成文档的类型 (o2o, o2m, m2m) 以便更好的验证和测试
$ python stat.py

# DuEE-fin
## 数据集下载:  https://aistudio.baidu.com/aistudio/competition/detail/65
$ cd Data/DuEEData  # 将 train.json 和 dev.json 粘贴至 Data/DuEEData 文件夹下并且运行:
$ python build_data.py
```


### 预训练模型的下载
- [**Fin-BERT**](https://github.com/valuesimplex/FinBERT) : 熵简科技 AI Lab 在 BERT 架构上使用 30 亿 tokens 训练的预训练模型。
- [**Bert-base-Chinese**](https://huggingface.co/bert-base-chinese) : 谷歌在 2018 年提出的预训练模型的中文训练版本。
- [**Bert-wwm**](https://huggingface.co/hfl/chinese-bert-wwm) : 哈工大讯飞联合实验室（HFL）在 BERT 基础训练任务中将掩码修改为全词掩码 whole word mask 的预训练模型。
- [**RoBerta-base-Chinese**](https://github.com/dbiir/UER-py/wiki/Modelzoo) : UER-py 在 [这篇论文](https://arxiv.org/abs/1909.05658) 的基础上训练的中文 RoBERTa 预训练模型。
- [**RoBerta-wwm-ext**](https://huggingface.co/hfl/chinese-roberta-wwm-ext) : 哈工大讯飞联合实验室（HFL）在 RoBERTa 基础训练任务中将掩码修改为全词掩码 whole word mask 的预训练模型。


### 快速运行
- 完成数据预处理和预训练模型的下载之后可以下载我们已经训练完成的模型进行快速复现。【 [下载地址](https://pan.baidu.com/s/1MS1lLPiE6kTMw-CIzbi8bg?pwd=XATU)】 将下载的模型放入 Exps/ 文件夹下，并修改配置 json 文件中的预训练模型路径和模型路径
- 批量的运行在 scripts/ 文件夹下，修改 run_Fin-PTPCG.sh 和 run_Fin-PTPCG_dueefin.sh 脚本文件中的预训练模型路径和任务名称(TASK_NAME，应和模型 json 配置文件中保持一致)，将skip_train参数设置为True，然后分别运行对应的脚本。
- 对单文件的抽取运行应修改 app.py 中 extract() 函数中的预训练模型和模型路径后运行 app.py ``` python app.py ```


### 模型训练
- [Fin-PTPCG](https://link.cnki.net/urlid/11.2127.TP.20231012.1517.002)

  修改 run_Fin-PTPCG.sh 和 run_Fin-PTPCG_dueefin.sh 脚本文件中的预训练模型路径和任务名称，修改参数至合适值(如只需复现可以按照论文中的参数进行设置)，论文中使用的编码器是 Fin_BERT 编码器，可以尝试其他 BERT 架构的编码器进行训练。  

``` bash
# ChFinAnn 数据集
$ nohup bash scripts/run_Fin-PTPCG.sh 1>Logs/Fin-PTPCG_ChFinAnn.log 2>&1 &
$ tail -f Logs/Fin-PTPCG_ChFinAnn.log

# Duee-fin数据集
$ nohup bash scripts/run_Fin-PTPCG_dueefin.sh 1>Logs/Fin-PTPCG_Dueefin.log 2>&1 &
$ tail -f Logs/Fin-PTPCG_Dueefin.log
```


## 历史更新
- **2023年11月17日** v0.1
  - 1.上传本项目代码，当前版本**尚未**实现下载新闻的可视化界面，app 的后续正在开发中。
- **2024年5月22日** v0.2
  - 1.实现下载新闻可视化界面，修改自动抽取逻辑
