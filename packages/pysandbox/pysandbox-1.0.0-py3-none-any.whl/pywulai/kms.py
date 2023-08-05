import time
import json
import hashlib
import string
import random
import requests
import pyrda.sqlserver as sqlserver
import pyrdo.list as rdlist
import pyrdb.wulai as rdb
# 定义函数
def GetChars(length):
    CHAR_LIST = []
    [[CHAR_LIST.append(e) for e in string.ascii_letters] for i in range(0, 2)]
    [[CHAR_LIST.append(e) for e in string.ascii_letters] for i in range(0, 2)]
    [[CHAR_LIST.append(e) for e in string.digits] for i in range(0, 2)]
    random.shuffle(CHAR_LIST)
    return "".join(CHAR_LIST[0:length])
#  添加头部认证文件
#  同时有相应的写入文件
def get_headers(pubkey:dict(type=str,help="the pubKey for wulai app"), secret:dict(type=str,help="the secret for wulai app")):
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
def get_headers_km(conn,app_id):
    sql = "select Fpubkey,Fsecret from t_km_app where Fapp_id='%s' and Fstatus = 1" % app_id
    data = sqlserver.sql_select(conn,sql)
    pubkey = data[0][0]
    secret = data[0][1]
    return get_headers(pubkey,secret)
# 定义简化版的提交
# headers get from get_headers()
def rd_post(headers, api, data):
    return requests.post(url=api, json=data, headers=headers)
###################################################################
# 知识点处理
#
#
#####################################################################
# 定义知识点查询辅助函数
def knowledge_list_aux(json,app_id, format='list'):
    data = json["knowledge_tags"]
    res = []
    if format == 'list':
        for i in range(len(data)):
            row = []
            id = data[i]["id"]
            parent_id = data[i]["parent_knowledge_tag_id"]
            name = data[i]["name"]
            row.append(app_id)
            row.append(id)
            row.append(name)
            row.append(parent_id)
            row.append(0)
            res.append(row)
    else:
        for i in range(len(data)):
            row = {}
            id = data[i]["id"]
            parent_id = data[i]["parent_knowledge_tag_id"]
            name = data[i]["name"]
            row['Fapp_id'] = app_id
            row['Fid'] = id
            row['Fname'] = name
            row['FparentId'] = parent_id
            row['Fflag'] = 0
            res.append(row)

    return res
# 查询知识点分类列表
def kcat_list(conn,app_id='caas', page=1, page_size=100, parent_id='0', format='list'):
    headers = get_headers_km(conn,app_id)
    api = "https://openapi.wul.ai/v2/qa/knowledge-tags/list"
    # '0' root
    data = {
        "page": page,
        "page_size": page_size,
        "parent_k_tag_id": parent_id
    }
    res_kl = rd_post(headers,api,data)
    res = knowledge_list_aux(res_kl.json(),app_id=app_id, format=format)
    return res
# 查询根节点
def root_knowledge_list(conn,app_id):
    # headers = get_headers_km(conn,app_id)
    return kcat_list(conn=conn,app_id=app_id,parent_id='0')
# 根据parentID查询知识点列表
def knowledge_list_by_parentId(conn,app_id,parent_id):
    # headers = get_headers_km(conn,app_id)
    return kcat_list(conn=conn,app_id=app_id,parent_id=parent_id)
#初始化知识库
def kc_initial_setUp(conn,app_id):
    if rdb.db_is_new_aibot(conn,app_id):
        rdb.initial_kc(conn=conn, app_id=app_id)
# 查询所有知识点
def kc_updateAll(conn,app_id):
    # headers = get_headers_km(conn,app_id)
    data = rdb.kc_unSearched(conn,app_id)
    # print(data)
    ncount = len(data)
    # print(ncount)
    while ncount > 0 :
        for i in range(len(data)):
            parent_id = data[i]
            res_kc = knowledge_list_by_parentId(conn,app_id,parent_id)
            rdb.upload_kc(conn,app_id,res_kc,1)
            rdb.kc_updated(conn,app_id,parent_id)
        data = rdb.kc_unSearched(conn,app_id)
        ncount = len(data)
#查询知识库的id
# 知识分类id
def kc_getId(conn,app_id,kc_name):
    return rdb.db_kc_getId(conn,app_id,kc_name)
# 知识占名称
def kc_getName(conn,app_id,kc_id):
    return rdb.db_kc_getName(conn,app_id,kc_id)
# 上级知识分类Id
def kc_getParentId(conn,app_id,kc_name):
    return rdb.db_kc_getParentId(conn,app_id,kc_name)
# 上级知识分类名称
def kc_getParentName(conn,app_id,kc_name):
    return rdb.db_kc_getParentName(conn,app_id,kc_name)
def wulai_kc_create(conn,app_id,kc_parentName,kc_name='123'):
    kc_parentId = kc_getId(conn,app_id,kc_parentName)
    headers = get_headers_km(conn,app_id)
    api = 'https://openapi.wul.ai/v2/qa/knowledge-tag/create'
    data = {
            "knowledge_tag": {
                "parent_knowledge_tag_id": kc_parentId,
                "id": '123',
                "name": kc_name}
            }
    r = rd_post(headers,api,data)
    res1 = r.json()
    keys = rdlist.dict_keys_list(res1)
    if 'knowledge_tag' in keys:
        res_ret = True
        Fapp_id = app_id
        Fid = res1['knowledge_tag']['id']
        Fname = res1['knowledge_tag']['name']
        FparentId = res1['knowledge_tag']['parent_knowledge_tag_id']
        Fflag = 1
        res = [[Fapp_id, Fid, Fname, FparentId, Fflag]]
        # 上传数据
        rdb.upload_kc(conn, app_id, res, 1)
    else:
        res_ret = False
    return res_ret
    print(res1)
#知识点创建规范
def kc_create(conn,app_id:dict(type=str,help="程序ID"),kc_parentName:dict(type=str,help="上级知识分类名称"),kc_name:dict(type=str,help="知识分类名称，全局唯一")='123'):
    return wulai_kc_create(conn=conn,app_id=app_id,kc_parentName=kc_parentName,kc_name=kc_name)

def wulai_kc_delete(conn,app_id,kc_name):
    headers = get_headers_km(conn,app_id)
    kc_id = kc_getId(conn,app_id,kc_name)
    api = 'https://openapi.wul.ai/v2/qa/knowledge-tag/delete'
    data = {
            "id": kc_id
            }
    r = rd_post(headers,api,data)
    #同步上传数据库,完善相关功能
    rdb.kc_del_byName(conn=conn,app_id=app_id,kc_name=kc_name)
    # return value
    res = r.json()
    return res
#知识分类删除
def kc_delete(conn,app_id,kc_name):
    return wulai_kc_delete(conn,app_id,kc_name)
def wulai_kc_update(conn,app_id,old_kc_name,new_kc_name):
    headers = get_headers_km(conn,app_id)
    kc_id = kc_getId(conn,app_id,old_kc_name)
    api = 'https://openapi.wul.ai/v2/qa/knowledge-tag/update'
    data = {
        "knowledge_tag": {
            "id": kc_id,
            "name": new_kc_name
        }
    }
    r = rd_post(headers,api,data)
    res = r.json()
    #更新数据库并写入日志
    rdb.db_kc_update(conn,app_id,old_kc_name,new_kc_name)
    return(res)
# 知识分类更新
def kc_update(conn,app_id,old_kc_name,new_kc_name):
    return wulai_kc_update(conn=conn,app_id=app_id,old_kc_name=old_kc_name,new_kc_name=new_kc_name)

############################################################################
#  处理知识点 kn
#
#
#
#
##############################################################################
# 创建知识点
def qa_knowledge_tag_knowledge_create_formatter(json,app_id,kc_name):
    #res = json['knowledge_tag_knowledge']['knowledge']['id']
    kc_id = json['knowledge_tag_knowledge']['knowledge_tag_id']
    kn_id = json['knowledge_tag_knowledge']['knowledge']['id']
    kn_name = json['knowledge_tag_knowledge']['knowledge']['standard_question']
    res = (app_id,kc_id,kc_name,kn_id,kn_name)
    return res


# 创建知识点并返回知识点ID string
def wulai_kn_create(conn,app_id,kn_name="test1_test2_test3", kc_name='rdstest2'):
    headers = get_headers_km(conn,app_id)
    #获取知识点的ID
    knowledge_tagId = kc_getId(conn,app_id,kc_name)
    print(knowledge_tagId)
    api = "https://openapi.wul.ai/v2/qa/knowledge-tag-knowledge/create"
    data = {
        "knowledge_tag_knowledge": {
            "knowledge":
                {
                    "status": True,
                    "standard_question": kn_name,
                    "respond_all": True,
                    "id": "121212",
                    "maintained_by_user_attribute_group": True
                },
            "knowledge_tag_id": knowledge_tagId}
    }
    print(rdb.db_is_kn_new(conn,app_id,kn_name))
    if rdb.db_is_kn_new(conn,app_id,kn_name):
        res_raw = rd_post(headers, api, data)
        # print(res_raw.json())
        res = qa_knowledge_tag_knowledge_create_formatter(res_raw.json(), app_id=app_id,kc_name=kc_name)
        #写入数据库
        rdb.db_kn_insert(conn,app_id,res)
        #写入日志
        info = "知识点" + kn_name +"已创建"
        rdb.db_add_log(conn=conn,app_id=app_id,obj_id='t_km_kn',desc_txt=info)
    else:
        res = rdb.db_kn_select(conn,app_id,kn_name)
        # 写入日志
        info = "知识点" + kn_name + "已存在"
        rdb.db_add_log(conn=conn, app_id=app_id, obj_id='t_km_kn', desc_txt=info)
    return res
#知识点查询ID
def kn_getId(conn,app_id,kn_name):
    res = rdb.db_kn_getId(conn,app_id,kn_name)
    return res
#知识点查询名称
def kn_getName(conn,app_id,kn_id):
    res = rdb.db_kn_getName(conn,app_id,kn_id)
    return res

#删除知识点
def wulai_kn_delete(conn,app_id,kn_name):
    headers = get_headers_km(conn,app_id)
    var_kn_id = kn_getId(conn,app_id,kn_name)
    api = 'https://openapi.wul.ai/v2/qa/knowledge/delete'
    data = {
        "id": var_kn_id
    }
    r = rd_post(headers,api,data)
    res = r.json()
    ncount = len(res)
    if ncount >0:
        info = "知识点" + kn_name + "删除失败"
    else:
        info = "知识点" + kn_name + "删除成功"
        #同步更新数据库及日志
        rdb.db_kn_delete(conn,app_id,kn_name)
    return (info)
#更新知识点
def wulai_kn_update(conn,app_id,old_kn_name,new_kn_name):
    var_kn_id = kn_getId(conn,app_id,old_kn_name)
    headers = get_headers_km(conn,app_id)
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
    r= rd_post(headers,api,data)
    #同步数据库及写入日志
    rdb.db_kn_update(conn=conn,app_id=app_id,old_kn_name=old_kn_name,new_kn_name=new_kn_name)
    res = r.json()
    # print(res)
    #通过判断键是否存在来确认是否已经成功
    keys = rdlist.dict_keys_list(res)
    if 'knowledge' in keys:
        res_ret = True
    else:
        res_ret = False
    return res_ret
#查询知识点
# 查询知识点规格化内容
def knowledge_items_list_fomatter(json,app_id,format='list'):
    data = json['knowledge_items']
    res = []
    if  format == 'list':
        for i in range(len(data)):
            item = []
            row = data[i]
            kn_id = row["knowledge"]["id"]
            kn_name = row["knowledge"]['standard_question']
            kc_id = row['knowledge_tag']['id']
            kc_name = row['knowledge_tag']['name']
            item.append(app_id)
            item.append(kc_id)
            item.append(kc_name)
            item.append(kn_id)
            item.append(kn_name)
            res.append(item)
    else:
        for i in range(len(data)):
            item = {}
            row = data[i]
            k_id = row["knowledge"]["id"]
            k_txt = row["knowledge"]['standard_question']
            k_tag_id = row['knowledge_tag']['id']
            k_tag_name = row['knowledge_tag']['name']
            item['app_id'] = app_id
            item['kn_name'] = k_txt
            item['kn_id'] = k_id
            item['kc_name'] = k_tag_name
            item['kc_id'] = k_tag_id
            res.append(item)
    return res


# 查询某个分类下的所有知识点列表并且同步给数据库
def wulai_kn_query(conn,app_id,kc_name, page=1, page_size=200,format='list'):
    knowledge_tagId = kc_getId(conn,app_id,kc_name)
    # print(knowledge_tagId)
    # page_size range from 0 to 200
    # here is the bug is pagesize more than 200
    # to be fixed
    headers = get_headers_km(conn,app_id)
    api = "https://openapi.wul.ai/v2/qa/knowledge-items/list"
    data = {
        "filter": {
            # "knowledge_id": "string",
            "knowledge_tag_id": knowledge_tagId
        },
        "page": page,
        "page_size": page_size
    }
    res_raw = rd_post(headers,api,data)
    # print(res_raw.json())
    arrayData =  knowledge_items_list_fomatter(res_raw.json(),app_id=app_id,format=format)
    ncount = len(arrayData)
    if ncount >0:
        #存在数据，同步数据库
        rdb.db_kn_insertBatchUnique(conn=conn,app_id=app_id,arrayData=arrayData)
        res = True
    else:
        res = False
    return res
def wulai_kn_query_pageCount(conn,app_id,kc_name, page=1,page_size=200):
    knowledge_tagId = kc_getId(conn,app_id,kc_name)
    # print(knowledge_tagId)
    # page_size range from 0 to 200
    # here is the bug is pagesize more than 200
    # to be fixed
    headers = get_headers_km(conn,app_id)
    api = "https://openapi.wul.ai/v2/qa/knowledge-items/list"
    data = {
        "filter": {
            # "knowledge_id": "string",
            "knowledge_tag_id": knowledge_tagId
        },
        "page": page,
        "page_size": page_size
    }
    res_raw = rd_post(headers,api,data)
    data = res_raw.json()
    res = data["page_count"]
    return(res)
# 针对分页进行处理
def wulai_kn_query2(conn,app_id,kc_name):
    page_count= wulai_kn_query_pageCount(conn,app_id,kc_name)
    #希望从1开始处理页码，进行分页处理
    page_count2 = page_count + 1
    # 针对每一页进行处理
    for page in range(1,page_count2):
        wulai_kn_query(conn,app_id,kc_name,page)
    res = True
    return res



########################################################################
# 创建相似问 kl
# 也称为knowledge leaf
#
#########################################################################
#创建相似问
def wulai_kl_create(conn,app_id,kn_name, kl_name="test1212"):
    kn_id = kn_getId(conn,app_id,kn_name)
    headers = get_headers_km(conn,app_id)
    api = "https://openapi.wul.ai/v2/qa/similar-question/create"
    data = {
        "similar_question": {
            "knowledge_id": kn_id,
            "question": kl_name,
            "id": "1212"}
    }
    #判断是否为新的相似问
    if rdb.db_is_kl_new(conn=conn,app_id=app_id,kn_name=kn_name,kl_name=kl_name):
        r = rd_post(headers, api, data)
        res = r.json()
        #写入数据库,需要进一步处理
        kl_id = res['similar_question']['id']
        item=(app_id,kn_id,kn_name,kl_id,kl_name)
        rdb.db_kl_insert(conn=conn,app_id=app_id,data=item)
        info = True
    else:
        #res = "知识点" + kn_name +"中对应的相似问" +kl_name +"已存在！"
        info = False
    return info
# 删除相似问
def wulai_kl_delete(conn,app_id,kn_name,kl_name):
    kl_id = rdb.db_kl_getId(conn,app_id,kn_name,kl_name)
    headers = get_headers_km(conn,app_id)
    api = 'https://openapi.wul.ai/v2/qa/similar-question/delete'
    data = {
        "id": kl_id
    }
    r = rd_post(headers,api,data)
    res = r.json()
    ncount =len(res)
    if ncount >0:
        info = False
    else:
        rdb.db_kl_delete(conn,app_id,kn_name,kl_name)
        info = True
    #print('delete:')
    #print(res)
    return (info)
#获取id
def kl_getId(conn,app_id,kn_name,kl_name):
    res = rdb.db_kl_getId(conn,app_id,kn_name,kl_name)
    return res
#获取名称
def kl_getName(conn,app_id,kl_id):
    res = rdb.db_kl_getName(conn,app_id,kl_id)
    return res
#修改相似问
def wulai_kl_update(conn,app_id,kn_name,old_kl_name,new_kl_name):
    headers = get_headers_km(conn,app_id)
    kn_id = kn_getId(conn,app_id,kn_name)
    kl_id = kl_getId(conn,app_id,kn_name,old_kl_name)
    api = 'https://openapi.wul.ai/v2/qa/similar-question/update'
    data = {
            "similar_question": {
            "knowledge_id": kn_id,
            "question": new_kl_name,
            "id": kl_id}
            }
    r = rd_post(headers,api,data)
    res = r.json()
    keys = rdlist.dict_keys_list(res)
    if 'similar_question' in keys:
        res_ret = True
        #更新数据库
        rdb.db_kl_update(conn,app_id,kn_name,old_kl_name,new_kl_name)
    else:
        res_ret = False
    return res_ret
#查询相似问
def qa_similar_question_list_formatter(json,app_id,kn_name,format='list'):
    data = json["similar_questions"]
    res = []
    if format == 'list':
        for i in range(len(data)):
            item = data[i]
            #针对字典数据进行处理
            item2 = rdlist.dict_values_list(item)
            kl_id = item2[0]
            kl_name = item2[1]
            kn_id = item2[2]
            row = [app_id,kn_id,kn_name,kl_id,kl_name]

            res.append(row)
    else:
        for i in range(len(data)):
            item = data[i]
            row_value = rdlist.dict_values_list(item)
            row_key = ['kl_id','kl_name','kn_id']
            row = rdlist.list_as_dict(row_key,row_value)
            res.append(row)

    return res


# 查询相似问列表
def wulai_kl_query(conn,app_id,kn_name, page=1, page_size=50,format='list'):
    kn_id = kn_getId(conn,app_id,kn_name)
    headers = get_headers_km(conn,app_id)
    api = "https://openapi.wul.ai/v2/qa/similar-question/list"
    data = {
        "knowledge_id": kn_id,
        "page": page,
        "page_size": page_size
        # "similar_question_id": "string"
    }
    res_raw = rd_post(headers,api,data)
    # print(res_raw.json())
    #处理数据
    arrayData =  qa_similar_question_list_formatter(res_raw.json(),app_id,kn_name,format=format)
    rdb.db_kl_insertBatchUnique(conn,app_id,arrayData)
    ncount = len(arrayData)
    if ncount > 0:
        info = True
    else:
        info = False
    return info
############################################################################################
# 标准案相关内容 kk = knowledge kernel
#
#
#
#
#
############################################################################################
# 创建标准答
def wulai_kk_create(conn,app_id,kn_name,kk_name):
    kn_id = kn_getId(conn,app_id,kn_name)
    headers = get_headers_km(conn,app_id)
    kk_id = '1212'
    uag_id = '0'
    api = "https://openapi.wul.ai/v2/qa/user-attribute-group-answer/create"
    data = {"user_attribute_group_answer": {
        "answer": {
            "knowledge_id": kn_id,
            "msg_body": {
                "text": {
                    "content": kk_name
                }
            },
            "id": kk_id
        },
        "user_attribute_group_id": uag_id}
    }
    if rdb.db_is_kk_new(conn,app_id,kn_name,kk_name):
        r = rd_post(headers,api,data)
        res2 = r.json()
        kk_id2 = res2['user_attribute_group_answer']['answer']['id']
        item = (app_id,kn_id,kn_name,kk_id2,kk_name)
        #写入数据库
        rdb.db_kk_insert(conn,app_id,item)
        #info = True
    else:
        item = rdb.db_kk_select(conn,app_id,kn_name,kk_name)
        #info Fal

    return item
#获取标签答ID
def kk_getId(conn,app_id,kn_name,kk_name):
    res = rdb.db_kk_getId(conn,app_id,kn_name,kk_name)
    return res
#获取名称
def kk_getName(conn,app_id,kk_id):
    res = rdb.db_kk_getName(conn,app_id,kk_id)
    return res
#删除标准答
def wulai_kk_delete(conn,app_id,kn_name,kk_name):
    headers = get_headers_km(conn,app_id)
    kk_id = kk_getId(conn,app_id,kn_name,kk_name)
    print(kk_id)
    api = "https://openapi.wul.ai/v2/qa/user-attribute-group-answer/delete"
    data = {
        "id": kk_id
    }
    r = rd_post(headers,api,data)
    res = r.json()
    ncount = len(res)
    if ncount >0:
        info = False
    else:
        info = True
        #写入数据库
        rdb.db_kk_delete(conn,app_id,kn_name,kk_name)
    #print(res)
    return info
# 更新标准答
def wuali_kk_update(conn,app_id,kn_name,old_kk_name,new_kk_name):
    headers = get_headers_km(conn,app_id)
    kn_id = kn_getId(conn,app_id,kn_name)
    kk_id = kk_getId(conn,app_id,kn_name,old_kk_name)
    api='https://openapi.wul.ai/v2/qa/user-attribute-group-answer/update'
    data= {"user_attribute_group_answer":
            {
                "answer":
                    {
                        "knowledge_id": kn_id,
                        "msg_body": {
                            "text": {
                                "content": new_kk_name
                                    }
                                    },
                        "id": kk_id
                            },
                        "user_attribute_group_id": "0"}
         }
    r = rd_post(headers,api,data)
    res = r.json()
    keys = rdlist.dict_keys_list(res)
    if 'user_attribute_group_answer' in keys:
        #更新成功
        rdb.db_kk_update(conn,app_id,kn_name,old_kk_name,new_kk_name)
        res_ret = True

    else:
        res_ret = False
    return res_ret
# 查询标准答列表
# 查询属性组答案列表格式化函数
def qa_user_attribute_group_answers_list_formatter(json,app_id,kn_name,format='list'):
    data = json["user_attribute_group_answers"]
    res = []
    if format =='list':
        for i in range(len(data)):
            item = data[i]
            row = []
            kk_id = item['answer']['id']
            #针对内容处理进行处理
            kk_name_rawType = item['answer']['msg_body']
            kk_name_rawKey  = rdlist.dict_keys_list(kk_name_rawType)
            if 'text' in kk_name_rawKey:
                kk_name = kk_name_rawType['text']['content']
            if 'image' in kk_name_rawKey:
                kk_name = kk_name_rawType['image']['resource_url']

            kn_id = item['answer']['knowledge_id']
            row.append(app_id)
            row.append(kn_id)
            row.append(kn_name)
            row.append(kk_id)
            row.append(kk_name)
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
    print(res)

    return res


# 查询属性组答案列表
def wulai_kk_query(conn,app_id,kn_name, uag_id="0", page=1, page_size=50,format='list'):
    kn_id = kn_getId(conn,app_id,kn_name)
    # print(kn_id)
    headers = get_headers_km(conn,app_id)
    api = "https://openapi.wul.ai/v2/qa/user-attribute-group-answers/list"
    data = {"filter": {
        "knowledge_id": kn_id,
        "user_attribute_group_id": uag_id},
        "page": page,
        "page_size": page_size
    }
    r = rd_post(headers,api, data)
    # print(r)
    res = r.json()
    # print(res)
    arrayData =  qa_user_attribute_group_answers_list_formatter(res,app_id,kn_name,format=format)
    ncount = len(arrayData)
    if ncount >0:
        rdb.db_kk_insertBatchUnique(conn,app_id,arrayData)
        info = True
    else:
        info = False
    return info





if __name__ == "__main__":
    conn = sqlserver.conn_create('115.159.201.178', 'sa', 'Hoolilay889@', 'rdbe')
    app_id = 'caas'
    #print(wulai_kn_query(conn,app_id,'发现运动版_固定内容'))
    #print(wulai_kn_query_pageCount(conn, app_id, '发现运动版_固定内容')+1)
    #print(wulai_kn_query2(conn,app_id,'捷豹路虎_精品'))



    # kc_initial_setUp(conn,app_id)
    #kc_updateAll(conn,app_id)
    # headers = get_headers_km(conn, 'caas')
    # kc1 =kcat_list(headers=headers,app_id='caas',parent_id='0',format='json')
    # print(kc1)
    # kc2 =kcat_list(headers=get_headers_km(conn, 'caas'),app_id='caas',parent_id='0',format='list')
    # print(kc2)
    # res3 = rdb.kc_unSearched(conn,'caas')
    # print(res3)
    # kcat_list_all(app_id='caas',conn=conn)
    # kc create
    # qa_knowledge_tag_create(conn=conn,app_id='caas',kc_parentId='71688',kc_name='test123458')
    # kc delete
    # qa_knowledge_tag_delete(conn=conn,app_id='caas',kc_id='707150')
    #print(wulai_kc_create(conn,app_id,'RDS','bbc7'))
    #wulai_kc_delete(conn,app_id,'bbc3')
    #wulai_kc_update(conn,app_id,'bbc','rdtest3')
    # 创建知识点
    # print(rdb.db_kc_getId(conn,app_id,'rdtest2'))
    #print(wulai_kn_create(conn=conn,app_id=app_id,kn_name='sample4',kc_name='rdtest2'))
    #print(wulai_kn_delete(conn,app_id,'sample3'))
    #update kn
    #print(wulai_kn_update(conn,app_id,'sample6','sample7'))
    #print(wulai_kn_query(conn,app_id,'l112'))
    #相似问创建
    # print(wulai_kl_create(conn,app_id,'sample7','sample73'))
    #print(wulai_kl_delete(conn,app_id,'sample7','sample72'))
    #print(wulai_kl_update(conn,app_id,7','sample712','gotest3'))
    #查看相似问'sample
    #print(wulai_kl_query(conn,app_id,'sample1'))
    #print(wulai_kl_query(conn, app_id, 'sample'))
    #创建标准答
    #print(wulai_kk_create(conn,app_id,'sample7','a3'))
    #删除标准答
    #print(wulai_kk_delete(conn,app_id,'sample7','a2'))
    #更新数据
    #print(wuali_kk_update(conn,app_id,'sample7','a3','a9'))
    #查询标准答列表
    print(wulai_kl_query(conn,app_id,'发现运动版和奔驰GLB对比'))
