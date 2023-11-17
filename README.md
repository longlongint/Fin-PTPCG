# Fin-PTPCG
论文[《基于Fin-BERT的中文金融领域事件抽取方法》](https://link.cnki.net/urlid/11.2127.TP.20231012.1517.002)的代码。
- [**Fin-PTPCG**](https://link.cnki.net/urlid/11.2127.TP.20231012.1517.002) 模型在[PTPCG](https://arxiv.org/abs/2112.06013)的基础上增加了Fin-BERT编码器，充分利用Fin-BERT预训练模型的表达能力，在编码阶段融入领域内的先验知识，并且在事件检测模块采用多个二元分类器叠加的方式，保证模型可以有效识别一篇文档内存在多事件的情况并筛除掉负面样例，抽取实体之后将实体连接成完全图并通过计算相似度矩阵进行剪枝，通过选择伪触发器解决无标注触发词的问题，最后接入事件分类器实现事件抽取。该方法在ChFinAnn和Duee-fin数据集上事件抽取任务的F1值相比于基线方法分别取得了0.7%和3.7%的提升。

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

