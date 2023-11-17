import os

from dee.tasks import DEETask, DEETaskSetting

if __name__ == "__main__":
    # init
    # task_dir = "Exps/sct-Tp1CG-with_left_trigger-OtherType-comp_ents-bs64_8"
    task_dir = "Exps/PTPCG_finBERT"
    cpt_file_name = "TriggerAwarePrunedCompleteGraph"
    # bert_model_dir is for tokenization use, `vocab.txt` must be included in this dir
    # change this to `bert-base-chinese` to use the huggingface online cache
    # bert_model_dir = "/path/to/bert-base-chinese"
    bert_model_dir = r"G:/Pretrain_model/pytorch/finbert-base-chinese"
    # load settings
    dee_setting = DEETaskSetting.from_pretrained(
        os.path.join(task_dir, f"{cpt_file_name}.task_setting.json")
    )
    dee_setting.local_rank = -1
    dee_setting.filtered_data_types = "o2o,o2m,m2m,unk"
    dee_setting.bert_model = bert_model_dir

    # build task
    dee_task = DEETask(
        dee_setting,
        load_train=False,
        load_dev=False,
        load_test=False,
        load_inference=False,
        parallel_decorate=False,
    )

    # load PTPCG parameters
    # 括号里的数字是加载第几个epoch的参数
    dee_task.resume_cpt_at(88)

    # predict
    '''
    doc = (
        "证券简称：中联电气证券代码：002323公告编号：2015-036"
        "江苏中联电气股份有限公司关于股权解除质押及再质押的公告"
        "公司及董事会全体成员保证公告内容的真实、准确和完整，没有虚假记载、误导性陈述或者重大遗漏。"
        "江苏中联电气股份有限公司（以下简称“公司”）2015年4月15日接到股东霍尔果斯苏兴股权投资管理合伙企业（有限合伙）（以下简称“霍尔果斯苏兴”）通知，霍尔果斯苏兴将其持有的原质押给江苏银行股份有限公司盐城文峰支行的8000000股无限售流通股（占公司目前股份总数的7.43%，该质押事项详见公司2014年6月11日刊登在《证券时报》、巨潮资讯网http://www.cninfo.com.cn上的第2014-031号公告）于2015年4月14日全部解除了质押，并在中国证券登记结算有限责任公司深圳分公司办理了解除质押登记手续。"
        "霍尔果斯苏兴将其持有的本公司5000000股无限售流通股（占公司目前股份总数的4.64%）又重新质押给江苏银行股份有限公司盐城文峰支行。"
        "霍尔果斯苏兴已于2015年4月15日在中国证券登记结算有限责任公司深圳分公司办理完毕质押登记手续，质押期限从2015年4月15日至质权人申请解冻为止。"
        "目前，霍尔果斯苏兴共持有本公司无限售条件流通股16057600股，占公司股份总数的14.93%。"
        "截止本公告披露日，霍尔果斯苏兴共质押其持有的公司股份5000000股，占公司股份总数的4.64%。"
        "特此公告。"
        "江苏中联电气股份有限公司董事会"
        "2015年4月16日"
    )
    '''
    doc = (
        "证券代码：000605证券简称：渤海股份公告编号：2018-062\
        渤海水业股份有限公司关于持股5%以上股东股份补充质押的公告\
        本公司及董事会全体成员保证信息披露的内容真实、准确和完整，没有\
        虚假记载、误导性陈述或重大遗漏。\
        近日，渤海水业股份有限公司（以下简称“公司”）收到公司持股5%以上股东李华青女士的《告知函》，获悉李华青女士将其所持有的部分公司股票进行补充质押，具体事项如下：\
        一、股份质押基本情况\
        1.基本情况\
        公司于2017年12月8日披露了《关于持股5%以上股东股份质押的公告》，李华青女士于2017年12月7日将其持有的公司12151000股股份质押。\
        2018年7月11日，公司完成资本公积转增股本，转增方案为每10股转增4股，本次资本公积转增股本完成后，李华青女士质押的股份由12151000股变更为17011400股。\
        由于质押股份的市值减少，根据李华青女士与海通证券股份有限公司（以下简称“海通证券”）的约定，李华青女士向海通证券补充质押公司股份1188600股，该笔补充质押已于2018年9月6日在中国证券登记结算有限责任公司办理了相关登记手续。\
        本次补充质押的1188600股占李华青女士所持有的公司股份总数的5.25%，占公司总股本的0.34%。\
        2.股份累计质押情况\
        截至本公告发布之日，李华青女士持有公司股份22619999股（均为限售流通股），占公司总股本的比例为6.41%。\
        本次质押完成后，李华青女士累计质押的股份数为18200000股，占公司总股本的5.16%，占其持有公司股份总数的80.46%。\
        3.本次股权质押行为、内容、程序符合国家法律法规和有关部门的规章制度要求，且李华青女士具备相应的资金偿还能力，不存在被强制平仓或强制过户等风险。\
        二、备查文件\
        1.李华青女士出具的《关于股份补充质押的告知函》；\
        2.中国证券登记结算有限责任公司股份冻结明细。\
        特此公告。\
        渤海水业股份有限公司董事会\
        2018年9月7日"

    )
    results = dee_task.predict_one(doc)  # dict数据类型
    print(results)
    # for events in results["event_list"]:
    #     print(events)
