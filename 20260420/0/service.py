import asyncio
import prog2
import socket

async def echo(reader, writer):
    while data := await reader.readline():
        res = data.strip().decode()
        try:
            res_sq=prog2.sqroots(res)
            writer.write(f"{res_sq}\n".encode())
        except Exception:
            writer.write(f"\n".encode())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())