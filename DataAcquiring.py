import random as r
import time as t
import asyncio
from asyncua import Client


async def types_gen(node):
    name = await node.read_display_name()
    name = name.Text
    a = await node.read_data_value()
    print(a)


async def main():
    url = 'opc.tcp://localhost:6000/freeopcua/server'
    while True:
        start = t.time()
        async with Client(url=url) as client:
            uri = 'http://example1.com'
            idx = await client.get_namespace_index(uri)
            folder = client.get_node('ns=2;i=1')
            nodes = await folder.get_children()
            count = 0
            for node in nodes:
                attributes = await node.get_children()
                for attribute in attributes:
                    await types_gen(attribute)
                    count += 1
            t.sleep(5)
        end = t.time()
        print(end-start, count)


if __name__ == '__main__':
    asyncio.run(main())

