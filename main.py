import asyncio
import websockets
import threading
import signal

import websocket

import nest_asyncio
nest_asyncio.apply()

connections = set()
connections_lock = threading.Lock()

async def playerConnection(websocket, path):
    global connections_lock
    global connections

    with connections_lock:
        connections.add(websocket)
        playerId = len(connections)
    
    print(f"System] Player {playerId} join.")
    
    try:
        while True:
            message = await websocket.recv()
            print(f"Player {playerId}: {message}")
    except websockets.exceptions.ConnectionClosed:
        with connections_lock:
            connections.remove(websocket)
            playersCount = len(connections)
            print(f"System] Player {playerId} leave. Now remain {playersCount} players.")

            if playersCount == 0:
                print("System] All players left. Server exited.")
                asyncio.get_event_loop().stop()

start_server = websockets.serve(playerConnection, "0.0.0.0", 60000)
asyncio_main_loop = asyncio.get_event_loop()
# asyncio.get_event_loop().add_signal_handler(signal.SIGINT, lambda: asyncio.ensure_future(handle_signal(signal.SIGINT)))
print("System] Server started.")

def signal_handler(sig, frame):
    print('Exiting...')
    loop = asyncio.get_event_loop()
    loop.stop()

# signal.signal(signal.SIGINT, signal_handler)
asyncio_main_loop.run_until_complete(start_server)
asyncio_main_loop.run_forever()
# try:
    # while asyncio.get_event_loop().is_running():
        # pass
    
    # asyncio_main_loop.run_until_complete(asyncio_main_loop.shutdown_asyncgens())
# except KeyboardInterrupt:
    # print("System] KeyboardInterrupt. Server exited.")
    # asyncio_main_loop.stop()
