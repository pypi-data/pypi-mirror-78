# -*-coding: UTF-8 -*-
#
import time
import json
import hashlib
import string
import random
import requests
# 设置laiye配置参数
# 将通用的函数迁移到rdo中
from . import laiye_config
# comment the config file for netstore
# import laiye_config2
from . import rdo
#导入公共变量
from . import gl
#导入结构
from  .tree import kt

# 定义公共变量----------
var_user_name = laiye_config.user_name
var_user_id = laiye_config.user_id


# 定义函数
def GetChars(length):
    CHAR_LIST = []
    [[CHAR_LIST.append(e) for e in string.ascii_letters] for i in range(0, 2)]
    [[CHAR_LIST.append(e) for e in string.ascii_letters] for i in range(0, 2)]
    [[CHAR_LIST.append(e) for e in string.digits] for i in range(0, 2)]
    random.shuffle(CHAR_LIST)
    return "".join(CHAR_LIST[0:length])


# 定义头文件
def get_headers():
    # 读取配置文件laiye_config.py
    secret = laiye_config.secret
    pubkey = laiye_config.pubkey
    timestamp = str(int(time.time()))
    nonce = GetChars(32)
    upwd = nonce + timestamp + secret
    s1 = hashlib.sha1()
    s1.update(upwd.encode("utf-8"))
    sign = s1.hexdigest()
    #    sign = hashlib.sha1(nonce + timestamp + secret).hexdigest()
    data = {
        "pubkey": pubkey,
        "sign": sign,
        "nonce": nonce,
        "timestamp": timestamp
    }
    headers = {}
    for k, v in data.items():
        headers["Api-Auth-" + k] = v
    return headers


# 定义简化版的提交
def rd_post(api, data):
    return requests.post(url=api, json=data, headers=get_headers())


# ------------------1用户相关部分------------------------------------------
# ------------------1.1用户相关方法----------------------------------------
# 创建用户
def laiye_user_create(user_name="test", user_id="123-123"):
    headers = get_headers()
    usr_create = "https://openapi.wul.ai/v2/user/create"
    data = {"nickname": user_name,
            "avatar_url": "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=4090426978,2527772527&fm=15&gp=0.jpg",
            "user_id": user_id}
    r = requests.post(usr_create, headers=get_headers(), json=data)
    res = len(r.json())
    if res == 0:
        return user_id
    else:
        return "error"


def user_create(user_name="test", user_id="123-123"):
    return laiye_user_create(user_name, user_id)


# 查询用户
def user_query(user_id='123-123', format='list'):
    api = "https://openapi.wul.ai/v2/user/get"
    data = {
        "user_id": user_id
    }
    r = rd_post(api, data)
    if format == 'list':
        res = rdo.dict_values_list(r.json())
    else:
        res = r.json()
    return res


# ------------------1.2创建用户类-------------------------------
# 创建用户，使用类的方式
class user:
    def create(user_name="test", user_id="123-123"):
        res = laiye_user_create(user_name, user_id)
        return res

    def query(user_id='123-123', format='list'):
        res = user_query(user_id, format)
        return res


# ------------------1.3用户定义变量----------------------------
# 定义obj_user防止重复调用，使用配置文件
obj_user = user.create(var_user_name, var_user_id)


# -------------end for user definition-------------------------
# --------------------------2前端机器人交互---------------------
# --------------------------2.1定义方法---------------------------
# 处理来也编码
def laiye_decode(data, format='list'):
    # msg_id = data['msg_id']
    msg_body = data["suggested_response"]
    res = []
    if format == 'list':
        for i in range(len(msg_body)):
            item = []
            data_entry = msg_body[i]
            res_txt = data_entry['response'][0]["msg_body"]["text"]["content"]
            res_score = data_entry['score']
            res_send = data_entry['is_send']
            res_ques_std = data_entry['bot']['qa']['standard_question']
            res_ques_sys = data_entry['bot']['qa']['question']

            item.append(res_ques_std)
            item.append(res_score)
            item.append(res_ques_sys)
            item.append(res_txt)

            # item.append(res_send)
            # item.append(i+1)
            res.append(item)
    else:
        for i in range(len(msg_body)):
            item = {}
            data_entry = msg_body[i]
            res_txt = data_entry['response'][0]["msg_body"]["text"]["content"]
            res_score = data_entry['score']
            res_send = data_entry['is_send']
            res_ques_std = data_entry['bot']['qa']['standard_question']
            res_ques_sys = data_entry['bot']['qa']['question']

            item['ques_std'] = res_ques_std
            item['score'] = res_score
            item['ques_match'] = res_ques_sys
            item['answer'] = res_txt

            # item.append(res_send)
            # item.append(i+1)
            res.append(item)

    return res


def laiye_bot(query_text, user_id=obj_user, format='list'):
    wd_input = {
        "msg_body": {
            "text": {
                "content": query_text
            }
        },
        "user_id": user_id,
        "extra": "string"
    }
    res_all = 'https://openapi.wul.ai/v2/msg/bot-response'
    res_get = requests.post(res_all, headers=get_headers(), json=wd_input)
    # print(res_get.json())
    return (laiye_decode(res_get.json(), format))


def aibot_query(query_text, user_id=obj_user, format='list'):
    return laiye_bot(query_text, user_id, format)


# --------------------2.2定义机器人类----------------------------------
# 定义机器人查询对象
class aibot:
    def query(query_text, user_id=obj_user, format='list'):
        res = aibot_query(query_text, user_id, format)
        return res


# -------------------3知识点分类-----------------------------------
# -------------------3.1知识点分类相关函数------------------------------
# 定义知识点查询辅助函数

def knowledge_list_aux(json, format='list'):
    data = json["knowledge_tags"]
    res = []
    if format == 'list':
        for i in range(len(data)):
            row = []
            id = data[i]["id"]
            parent_id = data[i]["parent_knowledge_tag_id"]
            name = data[i]["name"]
            row.append(name)
            row.append(id)
            row.append(parent_id)
            res.append(row)
    else:
        for i in range(len(data)):
            row = {}
            id = data[i]["id"]
            parent_id = data[i]["parent_knowledge_tag_id"]
            name = data[i]["name"]
            row['name'] = name
            row['id'] = id

            row['parent_id'] = parent_id
            #row['flag'] = 0
            res.append(row)

    return res

def knowledge_list_aux0(json, format='list'):
    data = json["knowledge_tags"]
    res = []
    if format == 'list':
        for i in range(len(data)):
            row = []
            id = data[i]["id"]
            parent_id = data[i]["parent_knowledge_tag_id"]
            name = data[i]["name"]
            row.append(name)
            row.append(id)
            row.append(parent_id)
            res.append(row)
    else:
        for i in range(len(data)):
            row = {}
            id = data[i]["id"]
            parent_id = data[i]["parent_knowledge_tag_id"]
            name = data[i]["name"]
            row['id'] = id
            row['name'] = name
            row['parent_id'] = parent_id
            row['flag'] = 0
            res.append(row)

    return res
# 查询知识点分类列表
def kcat_list(page=1, page_size=100, parent_id='407895', format='list'):
    api = "https://openapi.wul.ai/v2/qa/knowledge-tags/list"
    # '0' root
    # '71688'    网商test
    # '407895'  捷豹路虎
    data = {
        "page": page,
        "page_size": page_size,
        "parent_k_tag_id": parent_id
    }
    res_kl = requests.post(api, json=data, headers=get_headers())
    res = knowledge_list_aux(res_kl.json(), format)
    return res

def kcat_list0(page=1, page_size=100, parent_id='407895', format='list'):
    api = "https://openapi.wul.ai/v2/qa/knowledge-tags/list"
    # '0' root
    # '71688'    网商test
    # '407895'  捷豹路虎
    data = {
        "page": page,
        "page_size": page_size,
        "parent_k_tag_id": parent_id
    }
    res_kl = requests.post(api, json=data, headers=get_headers())
    res = knowledge_list_aux0(res_kl.json(), format)
    return res


# 查询所有结果

# def kcat_list_all(parent_id="0", format='list'):
#     res = kcat_list(parent_id=parent_id, format=format)
#     if res:
#         for i in range(len(res)):
#             if format == 'list':
#                 item = res[i][1]
#             else:
#                 item = res[i]['id']
#             return res + kcat_list_all(parent_id=item, format=format)
#     else:
#         return res

def kcat_list_all(parent_id="0", format='list'):
    if gl.kc_initial :
        task = kt.rest_id()
        ncount = len(task)
        while (ncount > 0):
            for i in range(ncount):
                id = task[i]
                item = kcat_list0(parent_id=id, format='json')
                kt.attach(item)
                kt.update(id)
            task = kt.rest_id()
            ncount = len(task)
        print('from initial')
        gl.kc_initial = False
    else:
        print('from gobal vars')
    res = kt.formatter(gl.forest,format=format)
    return (res)


# 查询根节点
def root0_knowledge_list():
    return kcat_list(parent_id='0')


# 查询网商test
def root1_knowledge_list():
    parent_id = root0_knowledge_list()[0][1]
    return kcat_list(parent_id=parent_id)


# 查询捷豹路虎
def jblh_knowledge_list():
    return kcat_list(parent_id='407895')


# 根据parentID查询知识点列表
def knowledge_list_by_parentId(parent_id):
    return kcat_list(parent_id=parent_id)


# 创建与来也一致的接口名称
def qa_knowledge_tags_list(parent_id="0"):
    return knowledge_list_by_parentId(parent_id)

def qa_knowledge_tag_create(kc_parentId='0',kc_name='123'):
    api = 'https://openapi.wul.ai/v2/qa/knowledge-tag/create'
    data = {
            "knowledge_tag": {
                "parent_knowledge_tag_id": kc_parentId,
                "id": '123',
                "name": kc_name}
            }
    r = rd_post(api,data)
    res1 = r.json()
    res = res1['knowledge_tag']['id']
    return res




# -----------------------3.2知识点分类class----------------
# 知识分类的类
class knowledgeTag:
    def query(parent_id="0"):
        res = kcat_list(parent_id=parent_id)
        return res

    def query_all(parent_id):
        res = kcat_list_all(parent_id=parent_id)
        return res

    def getId(knowledge_tag_name):
        arrayData = kcat_list_all('0')
        res = rdo.arrayLookup(arrayData, knowledge_tag_name, 0, 1)
        if res == False:
            return '-1'
        else:
            return res

    def getName(knowledge_tagId):
        arrayData = kcat_list_all('0')
        res = rdo.arrayLookup(arrayData, knowledge_tagId, 1, 0)
        if res == False:
            return '-1'
        else:
            return res

    def getParentId(knowledge_tag_name):
        arrayData = kcat_list_all('0')
        res = rdo.arrayLookup(arrayData, knowledge_tag_name, 0, 2)
        if res == False:
            return '-1'
        else:
            return res


def qa_knowledge_tag_delete(kc_id):
    api = 'https://openapi.wul.ai/v2/qa/knowledge-tag/delete'
    data = {
            "id": kc_id
            }
    r = rd_post(api,data)
    res = r.json()
    return res

# 针对概念进行统一处理
def kc_root(format='list'):
    return kcat_list(parent_id='0', format=format)


def kc_expand(parent_id, format='list'):
    return kcat_list(parent_id=parent_id, format=format)


def kc_expandAll(parent_id='0', format='list'):
    return kcat_list_all(parent_id=parent_id, format=format)


def kc_id(kc_name, parent_id='0'):
    arrayData = kc_expandAll(parent_id)
    res = rdo.arrayLookup(arrayData, kc_name, 0, 1)
    if res == False:
        return '-1'
    else:
        return res


def kc_name(kc_id, parent_id='0'):
    arrayData = kc_expandAll(parent_id)
    res = rdo.arrayLookup(arrayData, kc_id, 1, 0)
    if res == False:
        return '-1'
    else:
        return res

def kc_create(kc_parentName,kc_name):
    var_parent_id = kc.id(kc_parentName)
    return qa_knowledge_tag_create(var_parent_id,kc_name)

def kc_delete(kc_name, parent_id='0'):
    var_kc_id = kc_id(kc_name,parent_id)
    return qa_knowledge_tag_delete(var_kc_id)

def kc_parentId(kc_name, parent_id='0'):
    arrayData = kc_expandAll(parent_id)
    res = rdo.arrayLookup(arrayData, kc_name, 0, 2)
    if res == False:
        return '-1'
    else:
        return res

def qa_knowledge_tag_update(kc_id,new_kc_name):
    api = 'https://openapi.wul.ai/v2/qa/knowledge-tag/update'
    data = {
        "knowledge_tag": {
            "id": kc_id,
            "name": new_kc_name
        }
    }
    r = rd_post(api,data)
    res = r.json()
    return(res)
def kc_update(old_kc_name,new_kc_name):
    var_kc_id = kc_id(old_kc_name)
    res = qa_knowledge_tag_update(var_kc_id,new_kc_name)
    return res



def kc_query(parent_id='0', format='list', show_all=False):
    if show_all:
        res = kc_expandAll(parent_id, format)
        return res
    else:
        res = kc_expand(parent_id, format)
        return res


class kc:
    def root(format='list'):
        return kc_root(format)

    def expand(parent_id="0", format='list'):
        res = kc_expand(parent_id, format)
        return res

    def expandAll(parent_id='0', format='list'):
        res = kc_expandAll(parent_id, format)
        return res
    def create(kc_parentName,kc_name):
        return kc_create(kc_parentName,kc_name)
    def delete(kc_name,parent_id='0'):
        return kc_delete(kc_name,parent_id)
    def update(old_kc_name,new_kc_name):
        return kc_update(old_kc_name,new_kc_name)

    def query(parent_id='0', format='list', show_all=False):
        return kc_query(parent_id, format, show_all)

    def id(kc_name, parent_id='0'):
        return kc_id(kc_name, parent_id=parent_id)

    def name(kc_id, parent_id='0'):
        return kc_name(kc_id, parent_id)

    def parentId(kc_name, parent_id='0'):
        return kc_parentId(kc_name, parent_id)


# ----------------------------4知识点相关内容-----------------------------
# ----------------------------4.1知识点相关函数------------------------------
# 创建知识点
def qa_knowledge_tag_knowledge_create_formatter(json):
    res = json['knowledge_tag_knowledge']['knowledge']['id']
    return res


# 创建知识点并返回知识点ID string
def qa_knowledge_tag_knowledge_create(ques_txt="test1_test2_test3", knowledge_tagId='441190'):
    api = "https://openapi.wul.ai/v2/qa/knowledge-tag-knowledge/create"
    data = {
        "knowledge_tag_knowledge": {
            "knowledge":
                {
                    "status": True,
                    "standard_question": ques_txt,
                    "respond_all": True,
                    "id": "121212",
                    "maintained_by_user_attribute_group": True
                },
            "knowledge_tag_id": knowledge_tagId}
    }
    res_raw = requests.post(api, json=data, headers=get_headers())
    res = qa_knowledge_tag_knowledge_create_formatter(res_raw.json())
    return res


# 查询知识点规格化内容
def knowledge_items_list_fomatter(json,format='list'):
    data = json['knowledge_items']
    res = []
    if  format == 'list':
        for i in range(len(data)):
            item = []
            row = data[i]
            k_id = row["knowledge"]["id"]
            k_txt = row["knowledge"]['standard_question']
            k_tag_id = row['knowledge_tag']['id']
            k_tag_name = row['knowledge_tag']['name']
            item.append(k_txt)
            item.append(k_id)
            item.append(k_tag_name)
            item.append(k_tag_id)
            res.append(item)
    else:
        for i in range(len(data)):
            item = {}
            row = data[i]
            k_id = row["knowledge"]["id"]
            k_txt = row["knowledge"]['standard_question']
            k_tag_id = row['knowledge_tag']['id']
            k_tag_name = row['knowledge_tag']['name']
            item['kn_name'] = k_txt
            item['kn_id'] = k_id
            item['kc_name'] = k_tag_name
            item['kc_id'] = k_tag_id
            res.append(item)
    return res


# 查询某个分类下的所有知识点列表
def qa_knowledge_items_list(knowledge_tagId='441190', page=1, page_size=50,format='list'):
    api = "https://openapi.wul.ai/v2/qa/knowledge-items/list"
    data = {
        "filter": {
            # "knowledge_id": "string",
            "knowledge_tag_id": knowledge_tagId
        },
        "page": page,
        "page_size": page_size
    }
    res_raw = rd_post(api, data)
    return knowledge_items_list_fomatter(res_raw.json(),format=format)


# 定义查询相似问格式函数
def qa_similar_question_list_formatter(json,format='list'):
    data = json["similar_questions"]
    res = []
    if format == 'list':
        for i in range(len(data)):
            item = data[i]
            row = rdo.dict_values_list(item)
            res.append(row)
    else:
        for i in range(len(data)):
            item = data[i]
            row_value = rdo.dict_values_list(item)
            row_key = ['kl_id','kl_name','kn_id']
            row = rdo.list_as_dict(row_key,row_value)
            res.append(row)

    return res


# 查询相似问列表
def qa_similar_question_list(knowledge_id='2536831', page=1, page_size=50,format='list'):
    api = "https://openapi.wul.ai/v2/qa/similar-question/list"
    data = {
        "knowledge_id": knowledge_id,
        "page": page,
        "page_size": page_size
        # "similar_question_id": "string"
    }
    res_raw = rd_post(api, data)
    #print(res_raw.json())
    return qa_similar_question_list_formatter(res_raw.json(),format=format)


# 基于现有知识点，创建相似问
# 如果没有知识点，请先通过qa_knowledge_tag_knowledge_create('test1234')创建
def qa_similar_question_create(knowledge_id='2536831', ques_txt="test1212"):
    api = "https://openapi.wul.ai/v2/qa/similar-question/create"
    data = {
        "similar_question": {
            "knowledge_id": knowledge_id,
            "question": ques_txt,
            "id": "1212"}
    }
    res = rd_post(api, data)
    return res.json()


# 查询属性组答案列表格式化函数
def qa_user_attribute_group_answers_list_formatter(json,format='list'):
    data = json["user_attribute_group_answers"]
    res = []
    if format =='list':
        for i in range(len(data)):
            item = data[i]
            row = []
            answ_id = item['answer']['id']
            answ_txt = item['answer']['msg_body']['text']['content']
            k_id = item['answer']['knowledge_id']
            row.append(answ_id)
            row.append(answ_txt)
            row.append(k_id)
            res.append(row)
    else:
        for i in range(len(data)):
            item = data[i]
            row = {}
            answ_id = item['answer']['id']
            answ_txt = item['answer']['msg_body']['text']['content']
            k_id = item['answer']['knowledge_id']
            row['kk_id'] = answ_id
            row['kk_name'] = answ_txt
            row['kn_id'] = k_id
            res.append(row)

    return res


# 查询属性组答案列表
def qa_user_attribute_group_answers_list(knowledge_id="2536831", uag_id="0", page=1, page_size=50,format='list'):
    api = "https://openapi.wul.ai/v2/qa/user-attribute-group-answers/list"
    data = {"filter": {
        "knowledge_id": knowledge_id,
        "user_attribute_group_id": uag_id},
        "page": page,
        "page_size": page_size
    }
    res_raw = rd_post(api, data)
    return qa_user_attribute_group_answers_list_formatter(res_raw.json(),format=format)


# 创建属性组回复即标准答案
def qa_user_attribute_group_answer_create(knowledge_id='2536831', answ_txt="answer3", answ_id="1212", uag_id='0'):
    api = "https://openapi.wul.ai/v2/qa/user-attribute-group-answer/create"
    data = {"user_attribute_group_answer": {
        "answer": {
            "knowledge_id": knowledge_id,
            "msg_body": {
                "text": {
                    "content": answ_txt
                }
            },
            "id": answ_id
        },
        "user_attribute_group_id": uag_id}
    }
    r = rd_post(api, data)
    #print(res.json())
    res2 = r.json()
    res = res2['user_attribute_group_answer']['answer']['id']
    return res


# 删除属性组回复
def qa_user_attribute_group_answer_delete(id='4591534'):
    api = "https://openapi.wul.ai/v2/qa/user-attribute-group-answer/delete"
    data = {
        "id": id
    }
    res = rd_post(api, data)
    return res.json()


# ----------------4.2知识点class-------------
def func_ques_std_query(knowledgeTag_name,format='list'):
    ktag_id = knowledgeTag.getId(knowledgeTag_name)
    if ktag_id != False:
        res = qa_knowledge_items_list(ktag_id,format=format)
    else:
        res = False
    return res


def func_ques_std_getId(ques_txt, knowledgeTag_name):
    arrayData = func_ques_std_query(knowledgeTag_name)
    res = rdo.arrayLookup(arrayData, ques_txt, 0, 1)
    return res


def func_ques_std_getName(ques_id, knowledgeTag_name):
    arrayData = func_ques_std_query(knowledgeTag_name)
    res = rdo.arrayLookup(arrayData, ques_id, 1, 0)
    return res


def func_ques_like_query(ques_std_txt, knowledgeTag_name,format='list'):
    kn_id = func_ques_std_getId(ques_std_txt, knowledgeTag_name)
    res = qa_similar_question_list(kn_id,format=format)
    return res


def func_ques_like_getId(ques_like_txt, ques_std_txt, knowledgeTag_name):
    arrayData = func_ques_like_query(ques_std_txt, knowledgeTag_name)
    res = rdo.arrayLookup(arrayData, ques_like_txt, 1, 0)
    return res


def func_ques_like_getName(ques_like_id, ques_std_txt, knowledgeTag_name):
    arrayData = func_ques_like_query(ques_std_txt, knowledgeTag_name)
    res = rdo.arrayLookup(arrayData, ques_like_id, 0, 1)
    return res


class knowledgeNode:
    def ques_std_create(ques_txt, knowledgeTag_name):
        ktag_id = knowledgeTag.getId(knowledgeTag_name)
        if ktag_id != False:
            res = qa_knowledge_tag_knowledge_create(ques_txt, ktag_id)
        else:
            res = False
        return res

    def ques_std_query(knowledgeTag_name,format='list'):
        res = func_ques_std_query(knowledgeTag_name,format=format)
        return res

    def ques_std_getId(ques_txt, knowledgeTag_name):
        res = func_ques_std_getId(ques_txt, knowledgeTag_name)
        return res

    def ques_std_getName(ques_id, knowledgeTag_name):
        res = func_ques_std_getName(ques_id, knowledgeTag_name)
        return res

    def ques_like_create(ques_like_txt, ques_std_txt, knowledgeTag_name):
        kn_id = func_ques_std_getId(ques_std_txt, knowledgeTag_name)
        res = qa_similar_question_create(kn_id, ques_like_txt)
        return res

    def ques_like_query(ques_std_txt, knowledgeTag_name):
        res = func_ques_like_query(ques_std_txt, knowledgeTag_name)
        return res

    def ques_like_getId(ques_like_txt, ques_std_txt, knowledgeTag_name):
        res = func_ques_like_getId(ques_like_txt, ques_std_txt, knowledgeTag_name)
        return res

    def ques_like_getName(ques_like_id, ques_std_txt, knowledgeTag_name):
        res = func_ques_like_getName(ques_like_id, ques_std_txt, knowledgeTag_name)
        return res


def kn_create(txt, kc_name):
    ktag_id = kc_id(kc_name)
    if ktag_id != False:
        res = qa_knowledge_tag_knowledge_create(txt, ktag_id)
    else:
        res = False
    return res


def kn_query(kc_name,format='list'):
    res = func_ques_std_query(kc_name,format=format)
    return res



def kn_id(kn_name, kc_name):
    res = func_ques_std_getId(kn_name, kc_name)
    return res

def func_qa_knowledge_delete(kn_name,kc_name):
    var_kn_id = func_ques_std_getId(kn_name, kc_name)
    api = 'https://openapi.wul.ai/v2/qa/knowledge/delete'
    data = {
        "id": var_kn_id
    }
    r = rd_post(api, data)
    res = r.json()
    return (res)

def kn_delete(kn_name,kc_name):
    return func_qa_knowledge_delete(kn_name,kc_name)



def func_qa_knowledge_update(kc_name,old_kn_name,new_kn_name):
    var_kn_id = func_ques_std_getId(old_kn_name, kc_name)
    api ='https://openapi.wul.ai/v2/qa/knowledge/update'
    data ={
            "knowledge": {
            "status": True,
            "standard_question": new_kn_name,
            "respond_all": True,
            "id": var_kn_id,
            "maintained_by_user_attribute_group": True
                        }
            }
    r= rd_post(api,data)
    res = r.json()
    return(res)

def kn_update(kc_name,old_kn_name,new_kn_name):
    return(func_qa_knowledge_update(kc_name,old_kn_name,new_kn_name))




def kn_name(kn_id, kc_name):
    res = func_ques_std_getName(kn_id, kc_name)
    return res


class kn:
    def create(txt, kc_name):
        return kn_create(txt, kc_name)
    def delete(kn_name,kc_name):
        return kn_delete(kn_name,kc_name)
    def update(kc_name,old_kn_name,new_kn_name):
        return kn_update(kc_name,old_kn_name,new_kn_name)

    def query(kc_name,format='list'):
        return kn_query(kc_name,format)


    def id(kn_name, kc_name):
        return kn_id(kn_name, kc_name)

    def name(kn_id, kc_name):
        return kn_name(kn_id, kc_name)


def kl_create(txt, kn_name, kc_name):
    kn_id = func_ques_std_getId(kn_name, kc_name)
    res = qa_similar_question_create(kn_id, txt)
    return res


def kl_query(kn_name, kc_name,format='list'):
    res = func_ques_like_query(kn_name, kc_name,format=format)
    return res


def kl_id(txt, kn_name, kc_name):
    res = func_ques_like_getId(txt, kn_name, kc_name)
    return res


def kl_name(kl_id, kn_name, kc_name):
    res = func_ques_like_getName(kl_id, kn_name, kc_name)
    return res

def func_qa_similar_question_delete(kl_name, kn_name, kc_name):
    var_kl_id = kl_id(kl_name, kn_name, kc_name)
    api = 'https://openapi.wul.ai/v2/qa/similar-question/delete'
    data = {
            "id": var_kl_id
            }
    r = rd_post(api,data)
    res = r.json()
    return(res)

def kl_delete(kl_name, kn_name, kc_name):
    return func_qa_similar_question_delete(kl_name, kn_name, kc_name)

def func_qa_similar_question_update(new_kl_name,old_kl_name, kn_name, kc_name):
    var_kl_id = kl_id(old_kl_name, kn_name, kc_name)
    var_kn_id = kn_id(kn_name,kc_name)
    api = 'https://openapi.wul.ai/v2/qa/similar-question/update'
    data = {
            "similar_question": {
            "knowledge_id": var_kn_id,
            "question": new_kl_name,
            "id": var_kl_id}
            }
    r = rd_post(api,data)
    res = r.json
    return(res)

def kl_update(new_kl_name,old_kl_name, kn_name, kc_name):
    return(func_qa_similar_question_update(new_kl_name,old_kl_name, kn_name, kc_name))


# 知识叶
class kl:
    def create(txt, kn_name, kc_name):
        return kl_create(txt, kn_name, kc_name)
    def delete(kl_name, kn_name, kc_name):
        return(kl_delete(kl_name, kn_name, kc_name))
    def update(new_kl_name,old_kl_name, kn_name, kc_name):
        return(kl_update(new_kl_name,old_kl_name, kn_name, kc_name))

    def query(kn_name, kc_name,format='list'):
        return kl_query(kn_name, kc_name,format=format)

    def id(txt, kn_name, kc_name):
        return kl_id(txt, kn_name, kc_name)

    def name(kl_id, kn_name, kc_name):
        return kl_name(kl_id, kn_name, kc_name)


# 知识核相关内容

def kk_create(txt, kn_name, kc_name):
    kn_id2 = kn_id(kn_name, kc_name)
    return qa_user_attribute_group_answer_create(knowledge_id=kn_id2, answ_txt=txt, answ_id="1212", uag_id='0')
def kk_delete(kk_id):
    return qa_user_attribute_group_answer_delete(id=kk_id)
def kk_query(kn_name,kc_name,format='list'):
    var_kn_id = kn_id(kn_name,kc_name)
    return qa_user_attribute_group_answers_list(knowledge_id=var_kn_id,format=format)
def kk_id(kk_name,kn_name,kc_name):
    arrayData = kk_query(kn_name,kc_name)
    res = rdo.arrayLookup(arrayData,kk_name,1,0)
    return(res)
def kk_name(kk_id,kn_name,kc_name):
    arrayData = kk_query(kn_name,kc_name)
    res = rdo.arrayLookup(arrayData,kk_id,0,1)
    return(res)

def func_qa_user_attribute_group_answer_update(new_kk_name,old_kk_name,kn_name,kc_name):
    var_kn_id = kn_id(kn_name,kc_name)
    var_kk_id = kk_id(old_kk_name,kn_name,kc_name)
    api='https://openapi.wul.ai/v2/qa/user-attribute-group-answer/update'
    data= {"user_attribute_group_answer":
            {
                "answer":
                    {
                        "knowledge_id": var_kn_id,
                        "msg_body": {
                            "text": {
                                "content": new_kk_name
                                    }
                                    },
                        "id": var_kk_id
                            },
                        "user_attribute_group_id": "0"}
         }
    r = rd_post(api,data)
    res = r.json()
    return(res)
def kk_update(new_kk_name,old_kk_name,kn_name,kc_name):
    return(func_qa_user_attribute_group_answer_update(new_kk_name,old_kk_name,kn_name,kc_name))

class kk:
    def create(txt, kn_name, kc_name):
        return kk_create(txt, kn_name, kc_name)
    def delete(kk_id):
        return kk_delete(kk_id)
    def update(new_kk_name,old_kk_name,kn_name,kc_name):
        return(kk_update(new_kk_name,old_kk_name,kn_name,kc_name))
    def query(kn_name,kc_name,format='list'):
        return kk_query(kn_name,kc_name,format=format)
    def id(kk_name,kn_name,kc_name):
        return(kk_id(kk_name,kn_name,kc_name))
    def name(kk_id,kn_name,kc_name):
        return(kk_name(kk_id,kn_name,kc_name))
# ----------------5个性化回复-----------------------------
# 用户属性元数据解析
def user_attr_metadata(json):
    data = json["user_attribute_user_attribute_values"]
    res = []
    for i in range(len(data)):
        item = data[i]['user_attribute']
        row = []
        name = item["name"]
        id = item["id"]
        type = item["type"]
        value_type = item["value_type"]
        used = item["use_in_user_attribute_group"]
        row.append(name)
        row.append(id)
        row.append(type)
        row.append(value_type)
        row.append(used)
        res.append(row)
    return res


# 查询用户属性列表
def user_attribute_list(page=1, page_size=50):
    api = "https://openapi.wul.ai/v2/user-attribute/list"
    data = {
        "page": page,
        "page_size": page_size
    }
    res_raw = requests.post(api, json=data, headers=get_headers())
    res = user_attr_metadata(res_raw.json())
    return res


# 创建属性组
def qa_user_attribute_group_items_create(id="123", name="ua1", group_name="uag1"):
    api = "https://openapi.wul.ai/v2/qa/user-attribute-group-items/create"
    data = {
        "user_attribute_group_item": {
            "user_attribute_user_attribute_value":
                [
                    {
                        "user_attribute": {
                            "id": id
                        },
                        "user_attribute_value": {
                            "name": name
                        }
                    }
                ],
            "user_attribute_group": {
                "name": group_name}
        }
    }
    res = requests.post(api, json=data, headers=get_headers())
    return res


# 查询已有的属性组
def qa_user_attribute_group_items_list(page=1, page_size=50):
    api = "https://openapi.wul.ai/v2/qa/user-attribute-group-items/list"
    data = {
        "page": page,
        "page_size": page_size
    }
    res = rd_post(api, data)
    return (res.json())


# ---------------------------------------------------------------


if __name__ == "__main__":
    # print(kcat_list_all("0"))
    # print(knowledgeTag.query_all("407895"))
    # print(kcat_list(parent_id='3') == True)
    # a =[[1]]
    # b = [[2],[3],[3]]
    # print(unique(a + b))
    # uid = laiye_user_create('tom','json1')
    # 第2种方式
    # uid = user.create("test3","13-13-13")
    # print(uid)
    # keyword ='发现神行多少钱'
    # res_bot = aibot.query(keyword)
    # print(res_bot)
    # res = laiye_bot(keyword,uid)
    # print(res)
    # keyword2 = '发现运动发动机什么型号2'
    # res2 = laiye_bot(keyword2, uid)
    # print(res2)
    # 进行根节点查询
    # print(knowledgeTag.getId('RDS_TEST'))
    # print(knowledgeTag.getParentId('RDS_TEST'))
    # print(knowledgeTag.getName('407898'))
    # 测试创建知识点

    print(knowledgeNode.ques_like_create('q1', 'hello world!', 'RDS_TEST'))
    print(knowledgeNode.ques_like_query('test1234', 'RDS_TEST'))
    # res_kt = knowledgeTag.query_all(laiye_config.ktag_ns_id)
    # print(res_kt)
    print(jblh_knowledge_list())
    # print(root0_knowledge_list())
    # print(root1_knowledge_list())
    print(knowledge_list_by_parentId('71688'))
    print(qa_knowledge_tags_list())

    # 查询用户属性列表
    print(user_attribute_list())
    # 创建属性组
    # print(qa_user_attribute_group_items_create())
    # 查询属性组及属性列表
    print(qa_user_attribute_group_items_list())

    # 打印相关的参数
    # print(laiye_config.pubkey)
    # print(laiye_config.secret)
    # rdo.testPrint()
