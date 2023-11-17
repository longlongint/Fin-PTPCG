import os
import torch
import torch.nn as nn
from transformers import BertModel, logging
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, AdamW
from args import set_args

logging.set_verbosity_error()  # 不显示模型加载的warning


args = set_args()


def get_name(filepath):
    file_name = list()
    for t in os.listdir(filepath):
        data_collect = ''.join(t)
        file_name.append(data_collect)
    return file_name


class Model(nn.Module):

    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(768, 3)
        self.encoder = torch.nn.TransformerEncoderLayer(d_model=768, nhead=8)
        self.bn = torch.nn.BatchNorm1d(num_features=500)
        self.relu = torch.nn.ReLU(inplace=False)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, input_ids, attention_mask, token_type_ids):
        with torch.no_grad():
            out = pretrained(input_ids=input_ids,
                             attention_mask=attention_mask,
                             token_type_ids=token_type_ids)
        out = self.encoder(out.last_hidden_state)
        out = self.fc(out[:, 0])
        out = out.softmax(dim=1)
        return out


class LargeModel(nn.Module):

    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(1024, 3)
        self.encoder = torch.nn.TransformerEncoderLayer(d_model=1024, nhead=8)
        self.bn = torch.nn.BatchNorm1d(num_features=500)
        self.relu = torch.nn.ReLU(inplace=False)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, input_ids, attention_mask, token_type_ids):
        with torch.no_grad():
            out = pretrained(input_ids=input_ids,
                             attention_mask=attention_mask,
                             token_type_ids=token_type_ids)
        out = self.encoder(out.last_hidden_state)
        out = self.fc(out[:, 0])
        # out = self.fc(out.last_hidden_state[:, 0])
        out = out.softmax(dim=1)
        return out


class LabeledDataset(Dataset):
    def __init__(self):
        xy = []
        x = []
        y = []
        path = lab_path
        name = get_name(path)
        use_text = False
        use_title = True
        for i, (n) in enumerate(name):
            tmp = n
            if use_text:
                it = []
                f = open(path+n, encoding='GB18030')
                text = f.read()
                f.close()
                it.append(text)
                x.append(text)
                y.append(tmp)
                it.append(tmp)
                xy.append(it)
            if use_title:
                it = []
                n = n[:-4]
                for t in range(len(n)):
                    if n[t].isdigit():
                        continue
                    elif n[t] == '-':
                        n = n[(t+1):]
                        break
                x.append(n)
                it.append(n)
                y.append(tmp)
                it.append(tmp)
                xy.append(it)

        self.x = x
        self.y = y
        self.dataset = xy

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        text = self.x[i]
        label = self.y[i]

        return text, label


def collate_fn1(data):
    sents = [i[0] for i in data]
    labels = [-1 for i in data]
    pre = [i[1] for i in data]
    # 编码
    data = token.batch_encode_plus(batch_text_or_text_pairs=sents,
                                   truncation=True,
                                   padding='max_length',
                                   max_length=500,
                                   return_tensors='pt',
                                   return_length=True)

    # input_ids:编码之后的数字
    # attention_mask:是补零的位置是0,其他位置是1
    input_ids = data['input_ids'].to(device)
    attention_mask = data['attention_mask'].to(device)
    token_type_ids = data['token_type_ids'].to(device)
    labels = torch.LongTensor(labels).to(device)

    # print(data['length'], data['length'].max())

    return input_ids, attention_mask, token_type_ids, sents, pre


def labeled():
    model = torch.load(args.model_save_path + 'cls_model_{}_EPOCH3.pth'.format(args.pretrain_model))
    model.eval()
    dataset = LabeledDataset()
    loader_test = torch.utils.data.DataLoader(dataset=dataset,
                                              batch_size=args.test_batch_size,
                                              collate_fn=collate_fn1,
                                              shuffle=True,
                                              drop_last=True)
    for i, (input_ids, attention_mask, token_type_ids, sents, pre) in enumerate(loader_test):
        with torch.no_grad():
            out = model(input_ids=input_ids,
                        attention_mask=attention_mask,
                        token_type_ids=token_type_ids)

        out = out.argmax(dim=1)
        for j in range(len(out)):
            tpth = lab_path
            tpth = tpth + pre[j]
            f = open(tpth, encoding='GB18030')
            text = f.read()
            f.close()
            if out[j] == 0:
                path = r'G:/Dataset/fn/中性/'
                path = path + sents[j] + '.txt'
            elif out[j] == 1:
                path = r'G:/Dataset/fn/利好/'
                path = path + sents[j] + '.txt'
            else:
                path = r'G:/Dataset/fn/利空/'
                path = path + sents[j] + '.txt'
            with open(path, 'w', encoding='GB18030') as fi:
                fi.write(text)


if __name__ == '__main__':

    device = torch.device('cuda:0' if (torch.cuda.is_available() and args.use_cuda) else 'cpu')
    if args.pretrain_model in ['RoBERTa-zh-Large-PyTorch', 'chinese-macbert-large', 'chinese-roberta-wwm-ext-large',
                               'bert-large-chinese']:
        modsize = 'large'
    else:
        modsize = 'base'
    # 加载预训练模型
    pre_path = args.pretrain_path + '/' + args.pretrain_model
    pretrained = BertModel.from_pretrained(pre_path)
    # 需要移动到cuda上
    pretrained.to(device)
    # 加载字典和分词工具
    token = BertTokenizer.from_pretrained(pre_path)

    # 不训练,不需要计算梯度
    for param in pretrained.parameters():
        param.requires_grad_(False)
    if modsize == 'base':
        model = Model()
    elif modsize == 'large':
        model = LargeModel()
    # 同样要移动到cuda
    model.to(device)

    lab_path = r'G:/Code/financialNLP/data/2022-08-24/公司/'

    labeled()
