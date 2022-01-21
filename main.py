# from zeroconf import ServiceBrowser, Zeroconf
#
#
# class MyListener:
#
#     def remove_service(self, zeroconf, type, name):
#         print("Service %s removed" % (name,))
#
#     def add_service(self, zeroconf, type, name):
#         info = zeroconf.get_service_info(type, name)
#         print("Service %s added, service info: %s" % (name, info))
#
#
# zeroconf = Zeroconf()
# listener = MyListener()
# browser = ServiceBrowser(zeroconf, "_siegenia._tcp.local.", listener)

#
# try:
#     input("Press enter to exit...\n\n")
# finally:
#     zeroconf.close()
import asyncio
import pathlib
import ssl
import websockets
import json
import asyncio
import pathlib
import ssl
import websockets

client_socket = None

uri = "wss://192.168.178.48:443/WebSocket"

ssl_context_c = ssl.SSLContext()
ssl_context_c.check_hostname = False
ssl_context_c.verify_mode = ssl.CERT_NONE


# client_socket = websockets.connect(uri, ssl=ssl_context)

# print(dir(client_socket))

# print("connected")


async def server(websocket, path):
    async with websockets.connect(uri, ssl=ssl_context_c) as client_socket:
        while True:
            data = await websocket.recv()
            print("Server RECIVE___________________________START")
            print(data)
            print("Server RECIVE___________________________ENDE")

            await client_socket.send(data)

            answer = await client_socket.recv()

            res = json.loads(answer)
            if "data" in res:
                if "serialnr" in res["data"]:
                    tmp = res["data"]["serialnr"]
                    s = tmp[:5] + str(6) + tmp[5 + 1:]
                    res["data"]["serialnr"] = s

            answer = json.dumps(res)

            print("Server Answer___________________________START")
            print(answer)
            print("Server Answer___________________________END")

            await websocket.send(answer)


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("mycert.pem")
ssl_context.load_cert_chain(localhost_pem)

start_server = websockets.serve( server, "0.0.0.0", 443, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
#
#
# async def hello():
#     uri = "wss://192.168.178.48:443/WebSocket"
#     async with websockets.connect(
#             uri, ssl=ssl_context
#     ) as websocket:
#         dict2 = {"openclose": "OPEN"}
#         dictionary = {
#             "command": "setDeviceParams",
#             "params": dict2,
#             "id": 184
#
#         }
#
#         dictionary2 = {
#             "command": "getDeviceParams"
#         }
#
#         login = {"command": "login",
#                  "user": "test",
#                  "password": "1234",
#                  "long_life": False,
#                  "id": 184}
#
#         request = {"command": "getDevice",
#                    "id": 184}
#
#         json_object = json.dumps(login)
#         print(json_object)
#
#         await websocket.send(json_object)
#
#         greeting = await websocket.recv()
#         print(greeting)
#
#         json_object = json.dumps(dictionary)
#         print(json_object)
#
#         await websocket.send(json_object)
#
#         greeting = await websocket.recv()
#         print(greeting)
#
#
# asyncio.get_event_loop().run_until_complete(hello())
