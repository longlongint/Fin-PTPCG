import argparse


def set_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--use_cuda', default=True, type=bool, help='是否使用gpu')
    parser.add_argument('--epochs', default=5, type=int, help='训练的epoch数')
    parser.add_argument('--train_batch_size', default=128, type=int, help='训练的batch size')
    parser.add_argument('--test_batch_size', default=128, type=int, help='测试的batch size')
    parser.add_argument('--use_title', default=True, type=bool, help='是否使用标题进行训练')
    parser.add_argument('--use_text', default=False, type=bool, help='是否使用文本进行训练')
    parser.add_argument('--func', default='train', type=str, choices=['train', 'val', 'test'],
                        help='train是不使用交叉验证，val是使用交叉验证进行训练，test是测试')

    parser.add_argument('--path', default='./datasets', type=str, help='数据文件存储路径')
    parser.add_argument('--pretrain_path', default=r'G:/Pretrain_model/pytorch',
                        type=str, help='预训练模型路径')
    parser.add_argument('--pretrain_model', default='bert-base-chinese', type=str,
                        choices=['bert-base-chinese', 'chinese-pert-base', 'chinese-roberta-wwm-ext',
                                 'chinese-roberta-base', 'chinese-bert-wwm-ext', 'chinese-macbert-base',
                                 'RoBERTa-zh-Large-PyTorch', 'chinese-macbert-large', 'chinese-roberta-wwm-ext-large',
                                 'bert-large-chinese'],
                        help='预训练的模型')
    parser.add_argument('--model_save_path', default='./model/', type=str,
                        help='模型参数保存和读取的地址')
    parser.add_argument('--log_path', default='./logs', type=str, help='logs保存地址')

    return parser.parse_args()
