import asyncio

async def echo(reader, writer):
    host, port = writer.get_extra_info('peername')
    while data := await reader.readline():
        d1 = data.decode('utf-8').split()
        if d1[0] == 'print':
            writer.write((' '.join(d1[1:]) + '\n').encode().swapcase())
        elif d1[0] == 'info' and d1[1] == 'port':
            writer.write((str(port) + '\n').encode())
        elif d1[0] == 'info' and d1[1] == 'host':
            writer.write((host + '\n').encode())
            
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())