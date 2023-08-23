import asyncio
from asyncua import Server, ua
import sqlite3 as sql


async def main():
    server = Server()
    await server.init()
    # 设置服务器地址
    url = 'opc.tcp://localhost:6000/freeopcua/server'
    server.set_endpoint(url)
    server.set_server_name('MyServer')
    uri = 'http://example1.com'
    idx = await server.register_namespace(uri)
    # 注册对象和变量
    await server.nodes.objects.add_folder(idx, 'obj')

    # 添加测试用对象
    await server.nodes.objects.add_folder(idx, 'obj1')
    node = await server.nodes.objects.get_child([f'{idx}:obj1'])
    count = 0
    for i in range(10):
        count += 1
        await create_obj(idx, node, count)
    # 启动服务器
    await server.start()
    print(f'server start at{server.endpoint}')
    try:
        while True:
            await asyncio.sleep(5)
    finally:
        await server.stop()


# 测试用法
async def create_obj(idx, node, count):
    obj = await node.add_object(idx, f'test{count}')
    va0 = await obj.add_variable(idx, 'time', ua.Variant(ua.DateTime.now(), ua.VariantType.DateTime))
    va1 = await obj.add_variable(idx, 'temperature', ua.Variant(0.0, ua.VariantType.Double))
    va2 = await obj.add_variable(idx, 'water_usage', ua.Variant(0.0, ua.VariantType.Double))
    await va0.set_writable()
    await va1.set_writable()
    await va2.set_writable()


def run_server():
    asyncio.run(main())


if __name__ == '__main__':
    run_server()
