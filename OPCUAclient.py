from asyncua import Client, ua
from tkinter.messagebox import showerror, showinfo
import numpy as np
import time as t
from datetime import datetime


# 根据初始值框所输入内容（统一为StringVar)
# 和DataType转换得出真实初始值
def type_trans(value, string):
    if string == 'Boolean':
        return eval(value)
    elif string == 'Int64':
        return np.int(value)
    elif string == 'Float':
        return np.float(value)
    elif string == 'Double':
        return np.double(value)
    elif string == 'String':
        return value
    elif string == 'DateTime':
        return datetime.fromtimestamp(t.time())


class MyClient:
    def __init__(self, idx, client, folder_node):
        self.idx = idx
        self.client = client
        self.folder_node = folder_node

    # @staticmethod
    # async def run_client():
    #     url = 'opc.tcp://localhost:6000/freeopcua/server'
    #     async with Client(url=url) as client:
    #         uri = 'http://example1.com'
    #         idx = await client.get_namespace_index(uri)
    #         # nod = await client.nodes.objects.get_children()
    #         # node = await client.check_connection()
    #         # print(nod)
    #         # print(node)
    #         folder_node = client.get_node("ns=2;i=1")
    #         # b = await folder_node.get_child(['2:test1', '2:time'])

    # 1. 最初的设计（淘汰）
    # name为添加变量的列表, 其中name[0]是点位名, name[1:]是变量名
    #    for i in range(1, len(name)):
    #         va = await obj.add_variable(idx, name[i], ua.Variant(var_value[name[1]][0], eval(var_value[name[1]][1])))
    #         await va.set_writable()
    # val_value是字典，以变量名检索，[0]为变量初始值， [1]为变量数据类型
    #
    # 2. signal_name为点位名， entry_list为三个三个一组的列表
    async def add_node(self, signal_name, entry_list):
        obj = await self.folder_node.add_object(self.idx, signal_name)
        for i in range(0, len(entry_list), 3):
            await obj.add_variable(self.idx, entry_list[i+2].get(),
                                   ua.Variant(type_trans(entry_list[i].get(), entry_list[i + 1].get()),
                                              eval(f'ua.VariantType.{entry_list[i + 1].get()}')))

    # 待debug
    async def add_node1(self, signal_name1, data_list):
        print(data_list)
        obj = await self.folder_node.add_object(self.idx, signal_name1)
        for i in range(0, len(data_list), 3):
            await obj.add_variable(self.idx, data_list[i+2],
                                   ua.Variant(type_trans(data_list[i], data_list[i + 1]),
                                              eval(f'ua.VariantType.{data_list[i + 1]}')))

    async def get_node_(self, identifier):
        print(identifier)
        try:
            # b = client.get_node('ns=2;i=4')
            b = self.client.get_node(identifier)
            value = await b.read_value()
            h = await b.read_display_name()
            h = h.Text
            showinfo(title='查询结果', message=f'您查询的点位名：{h}\n您查询的点位：{identifier}\n您查询的点位值：{value}')
        except:
            showerror(title='错误', message='查询错误!')

    # 点位写入数据库（数据持久化）
    async def write(self):
        pass

    # 点位读取（数据持久化）
    async def read(self):
        pass

    # def data_inter(name, value):
    #     connection = sql.connect(
    #         host="localhost",
    #         user="root",
    #         password="2Weiayou!",
    #         database="firstproject"
    #     )
    #     with connection.cursor() as cursor:
    #         query = 'UPDATE opcua.signal_variable SET value=%s WHERE name=%s'
    #         a = cursor.execute(query, (value, name))
    #         return a > 0
