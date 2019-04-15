import asyncio
import time

import websockets
import json

from python.LeapFrame import LeapFrame


def read_file(name='pinch-57fps.json'): return open(name, "r").read()


def read_json(data=read_file()): return json.loads(data)


def write_file(data, name='pinch-57fps-copy.json'):
    with open(name, 'w') as outfile:
        outfile.write(data)
        outfile.close()


leap_data = read_json()

# first frame
metadata = leap_data['metadata']
print('loaded meta: ' + str(metadata))

frames = leap_data['frames']
# frame descriptor
print('loaded frames: ' + str(frames[0]))


class Server:

    def __init__(self):
        self.connected = False
        self.i_frame = 0
        start_server = websockets.serve(self.hello, 'localhost', 6437)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def get_next_grame(self):
        if self.i_frame < len(frames) - 1:
            self.i_frame += 1
        else:
            self.i_frame = 1
            print("loop")
        return LeapFrame(json_data=frames[self.i_frame]).to_json()

    async def hello(self, websocket, path):
        print("connecting")

        async def disconnect():
            self.i_frame = 0
            self.connected = False
            websocket.close()
            print("disconnected")

        try:
            self.i_frame = 0
            await websocket.send('{"serviceVersion":"2.3.1+33747", "version":6}')
            await websocket.send('{"event": {"state": { "attached": true, "id": "NNNNNNNNNNN", "streaming": true,'
                                 '"type": "peripheral" },"type": "deviceEvent"}}')

            self.connected = True
            while self.connected:
                payload = self.get_next_grame()
                await websocket.send(payload)
                time.sleep(0.01)
                # print(payload)
        except:
            await disconnect()


Server()
