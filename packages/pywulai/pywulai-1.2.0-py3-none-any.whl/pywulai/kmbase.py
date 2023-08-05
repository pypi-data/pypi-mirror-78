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
    print(data)
    ncount = len(data)
    print(ncount)
    while ncount > 0 :
        for i in range(len(data)):
            parent_id = data[i]
            res_kc = knowledge_list_by_parentId(conn,app_id,parent_id)
            rdb.upload_kc(conn,app_id,res_kc,1)
            rdb.kc_updated(conn,app_id,parent_id)
        data = rdb.kc_unSearched(conn,app_id)
        ncount = len(data)
#查询知识库的id

def wulai_kc_create(conn,app_id,kc_parentName,kc_name='123'):
    kc_parentId = rdb.db_kc_getId(conn,app_id,kc_parentName)
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
    # print(res1)
    Fapp_id = app_id
    Fid = res1['knowledge_tag']['id']
    Fname = res1['knowledge_tag']['name']
    FparentId = res1['knowledge_tag']['parent_knowledge_tag_id']
    Fflag = 1
    res = [[Fapp_id,Fid,Fname,FparentId,Fflag]]
    #上传数据
    rdb.upload_kc(conn,app_id,res,1)
    return res
def wulai_kc_delete(conn,app_id,kc_name):
    headers = get_headers_km(conn,app_id)
    kc_id = rdb.db_kc_getId(conn,app_id,kc_name)
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
def wulai_kc_update(conn,app_id,old_kc_name,new_kc_name):
    headers = get_headers_km(conn,app_id)
    kc_id = rdb.db_kc_getId(conn,app_id,old_kc_name)
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
############################################################################
#  处理知识点
#
#
#
#
##############################################################################

if __name__ == "__main__":
    conn = sqlserver.conn_create('115.159.201.178', 'sa', 'Hoolilay889@', 'rdbe')
    app_id = 'caasb'
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
    #wulai_kc_create(conn,app_id,'RDS','bbc3')
    #wulai_kc_delete(conn,app_id,'bbc3')
    #wulai_kc_update(conn,app_id,'bbc','rdtest3')