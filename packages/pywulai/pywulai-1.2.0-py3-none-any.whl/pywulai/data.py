import pyrda.sqlserver as sqlserver
# test for function notation
def helloworld(txt: dict(type=str, help='input text')):
    print(txt)
# initial knowledge category in database
def initial_kc(conn, app_id: dict(type=str, help="the name of km app")='caas'):
    data = (app_id,'0','root','-1',0)
    sql = "insert into t_km_kc values('%s','%s','%s','%s',%s)" % data
    sqlserver.sql_insert(conn, sql)
if __name__ == '__main__':
    helloworld('hawken')
    print(helloworld.__annotations__)
    #初始化数据知识分类数据
    conn = sqlserver.conn_create("115.159.201.178", "sa", "Hoolilay889@", "rdbe")
    app_id = "nslog"
    initial_kc(conn,app_id)
    sqlserver.conn_close(conn)

