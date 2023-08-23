import tkinter as tk
import asyncio
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
import pandas as pd
from asyncua import Client, ua
from OPCUAclient import MyClient
import time as t


# 主窗口UI
def tk_window():
    # frame1
    frame1 = ttk.LabelFrame(window, text="简介", borderwidth=1, relief="solid")
    Label1 = ttk.Label(frame1, text="本OPCUA服务器endpoint为 'opc.tcp://localhost:6000/freeopcua/server'"
                                    "\n服务器名'MyServer', 点位存储在ns=2;i=1的folder\n可以使用文件自动导入点位，或手动录入点位")
    Label1.grid(row=0, column=0, padx=5, pady=5)
    frame1.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

    # frame2
    frame2 = ttk.LabelFrame(window, text='服务器配置', borderwidth=1, relief="solid")
    Label2 = ttk.Label(frame2, text='请输入点位名：')
    entry1 = ttk.Entry(frame2, textvariable=e1)
    button1 = ttk.Button(frame2, text='加入点位')
    button2 = ttk.Button(frame2, text='选择配置文件', command=signal_set)
    Label3 = ttk.Label(frame2, text='请输入属性数量：')
    button3 = ttk.Button(frame2, text='开始', command=tk_window1)
    Label4 = ttk.Label(frame2, text='可参考:  示例文件.xlsx')
    Label4.grid(row=3, column=0, columnspan=2)
    entry4 = ttk.Entry(frame2, textvariable=e7)
    entry4.grid(row=1, column=1, padx=5, pady=5)
    Label3.grid(row=1, column=0, padx=5, pady=5)
    entry1.grid(row=0, column=1, padx=5, pady=5)
    Label2.grid(row=0, column=0, padx=5, pady=5)
    button3.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    button1.grid(row=4, column=1, padx=5, pady=5)
    button2.grid(row=4, column=0, padx=5, pady=5)
    frame2.grid(row=1, column=0, padx=5, pady=5)

    # frame3
    frame3 = ttk.LabelFrame(window, text='特定值查询', borderwidth=1, relief="solid")
    Label3 = ttk.Label(frame3, text='请输入要查询的ns=')
    Label4 = ttk.Label(frame3, text='请输入要查询的i=')
    entry2 = ttk.Entry(frame3, textvariable=e2)
    entry3 = ttk.Entry(frame3, textvariable=e3)

    button3 = ttk.Button(frame3, text='查询点位', command=get_)
    Label3.grid(row=0, column=0, padx=5, pady=5)
    entry2.grid(row=0, column=1, padx=5, pady=5)
    Label4.grid(row=1, column=0, padx=5, pady=5)
    entry3.grid(row=1, column=1, padx=5, pady=5)
    button3.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    frame3.grid(row=1, column=1, padx=5, pady=5)


# 副窗口UI
def tk_window1():
    window1 = tk.Tk()
    window1.title('点位配置')
    frame = ttk.LabelFrame(window1, text="点位配置", borderwidth=1, relief="solid")
    frame.grid(row=0, column=0, padx=5, pady=5)
    create_variable(frame)
    button = ttk.Button(frame, text='加入点位', command=add_)
    button.grid(row=3, column=0, padx=5, pady=5, columnspan=2)


# 副窗口生成特定数量属性表
def create_variable(frame):
    num = e7.get()
    count = 0
    for i in range(3 * num):
        var = tk.StringVar(value='null')
        var_list.append(var)
    for i in range(0, 3 * num, 3):
        if count == 0:
            Label5 = ttk.Label(frame, text='属性名：')
            Label6 = ttk.Label(frame, text='数据类型：')
            Label7 = ttk.Label(frame, text='初始值(若为DateTime类型则不用填)：')
            Label5.grid(row=0, column=0 + count, padx=5, pady=5)
            Label6.grid(row=1, column=0 + count, padx=5, pady=5)
            Label7.grid(row=2, column=0 + count, padx=5, pady=5)
        #     for h in var_list:
        #         print(id(h))
        # print('这是', id(var_list[i]), id(var_list[i+1]), id(var_list[i+2]))
        entry5 = ttk.Entry(frame, textvariable=var_list[i])
        combobox = ttk.Combobox(frame, values=['Boolean', 'Int64', 'Float', 'Double', 'String', 'DateTime'],
                                textvariable=var_list[i + 1])
        entry4 = ttk.Entry(frame, textvariable=var_list[i + 2])
        entry_list.append(entry5)
        entry_list.append(combobox)
        entry_list.append(entry4)
        entry4.grid(row=0, column=1 + count, padx=5, pady=5)
        entry5.grid(row=2, column=1 + count, padx=5, pady=5)
        combobox.grid(row=1, column=1 + count, padx=5, pady=5)
        count += 1


# 文件式处理方法，待完善
async def signal_set_():
    url = 'opc.tcp://admin@localhost:6000/freeopcua/server'
    lst = []
    async with Client(url=url) as client:
        uri = 'http://example1.com'
        idx = await client.get_namespace_index(uri)
        folder_node = client.get_node("ns=2;i=1")
        my_client = MyClient(idx, client, folder_node)
    path = askopenfilename(title='请选择点位文件',
                           filetypes=(('表格文件', '*.xlsx'), ('表格文件', '*.xls'), ('CSV文件', '*.csv')))
    if path[-1] == 'x' or path[-1] == 's':
        df = pd.read_excel(path)
    elif path[-1] == 'v':
        df = pd.read_csv(path)
    for i in df.iterrows():
        signal_name1 = i[1]['点位名']
        count = 0
        for h in i[1]:
            if count != 0:
                lst.append(h)
            count += 1
        await my_client.add_node1(signal_name1, lst)
    showinfo(title='成功', message='点位添加成功!')

    # 具体处理过程


def signal_set():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(signal_set_())


#
# 调用客户端
#
async def add():
    url = 'opc.tcp://admin@localhost:6000/freeopcua/server'
    async with Client(url=url) as client:
        uri = 'http://example1.com'
        idx = await client.get_namespace_index(uri)
        folder_node = client.get_node("ns=2;i=1")
        my_client = MyClient(idx, client, folder_node)
        # 点位配置框变量
        signal_name = e1.get()
        await my_client.add_node(signal_name, entry_list)
        b = await client.nodes.root.get_child(['0:Objects', '2:obj', f'2:{signal_name}'])
        nodes = await b.get_children()
        for node in nodes:
            name = await node.read_display_name()
            name = name.Text
            ns = node.nodeid.NamespaceIndex
            ni = node.nodeid.Identifier
            showinfo(title='成功', message=f'点位 {name} 添加成功!\n ns={ns};i={ni}')


def add_():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add())


async def get__():
    url = 'opc.tcp://localhost:6000/freeopcua/server'
    async with Client(url=url) as client:
        uri = 'http://example1.com'
        idx = await client.get_namespace_index(uri)
        folder_node = client.get_node("ns=2;i=1")
        my_client = MyClient(idx, client, folder_node)
        namespace_to_get = e2.get()
        signal_id_to_get = e3.get()
        identifier = f'ns={namespace_to_get};i={signal_id_to_get}'
        await my_client.get_node_(identifier)


def get_():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get__())


if __name__ == '__main__':
    var_list = []
    entry_list = []
    # 窗口1
    window = tk.Tk()
    window.title('OPC UA客户端')
    e1, e2, e3 = tk.StringVar(), tk.IntVar(), tk.IntVar()
    e1.set('null')
    e2.set(2)
    e3.set(0)
    e7 = tk.IntVar()
    e7.set(1)
    tk_window()

    tk.mainloop()

    # init_value = type_trans(inter_value, variable_datatype)
