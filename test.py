import json
import asyncio
import pathlib
import ssl
import websockets

ssl_context_c = ssl.SSLContext()
ssl_context_c.check_hostname = False
ssl_context_c.verify_mode = ssl.CERT_NONE

import decode2


userdict = {}

async def hello():
    uri = "wss://192.168.178.48:443/WebSocket"
    async with websockets.connect(
            uri, ssl=ssl_context_c
    ) as websocket:

        counter = 0
        login = {"command": "login",
                 "user": "Admin",
                 "password": "****",
                 "long_life": False,
                 "id": counter}

        counter+=1

        getUserIDs = {"command": "getUserIds",
                   "id": counter}

        counter+=1

        json_object = json.dumps(login)
        await websocket.send(json_object)
        answer = await websocket.recv()

        json_object = json.dumps(getUserIDs)
        await websocket.send(json_object)
        answer = await websocket.recv()
        userids = (json.loads(answer)["data"]["userids"])

        for id in userids :
            getUserID = {"command": "getUser", "params": {"userid": id}, "id": counter}
            counter += 1
            json_object = json.dumps(getUserID)
            await websocket.send(json_object)
            answer = await websocket.recv()
            data = json.loads(answer)["data"]
            name = data["userdetails"]["username"]
            userdict[id] = name

        getProtocol = {"command":"getProtocolData","params":{"deviceid":9,"protocoltype":1},"id":counter}
        counter += 1
        json_object = json.dumps(getProtocol)
        await websocket.send(json_object)
        answer = await websocket.recv()
        data = json.loads(answer)["data"]
        protocoldata = data["protocoldata"]

        decoder = decode2.ProtocollDecode1(userdict)
        decoder.decode(protocoldata)
        #print(protocoldata)



asyncio.get_event_loop().run_until_complete(hello())
