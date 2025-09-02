import time
import typing
import websocket_server
import os
import vgamepad

HOST = "0.0.0.0"
PORT = 12121

def clamp(value, minLimit = -1.0, maxLimit = 1.0):
    value = float(value)
    value = max(value, minLimit)
    value = min(value, maxLimit)
    return value

class Player:
    def __init__(self) -> None:
        self.gamepad = vgamepad.VX360Gamepad()
    def interpret(self, message:str):
        xyab_mapping = {
            'a': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,
            'b': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,
            'x': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,
            'y': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            'lt': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
            'ls': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            'rt': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
            'rs': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            'dl': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            'dd': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            'dr': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
            'du': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            'start': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START,
            'back': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            'guide': vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
        }

        args = message.split(' ')
        # self.gamepad.left_trigger_float
        if args[0] == "pressed":
            twostep = args[1].split('-')
            if len(twostep) == 2:
                self.gamepad.press_button(xyab_mapping[twostep[0]])
            else:
                self.gamepad.press_button(xyab_mapping[args[1]])
        elif args[0] == 'released':
            twostep = args[1].split('-')
            if len(twostep) == 2:
                self.gamepad.press_button(xyab_mapping[twostep[1]])
                self.gamepad.update()
                time.sleep(0.1)
                self.gamepad.release_button(xyab_mapping[twostep[1]])
                self.gamepad.release_button(xyab_mapping[twostep[0]])
            else:
                self.gamepad.release_button(xyab_mapping[args[1]])
        elif args[0] == 'moveljoy':
            self.gamepad.left_joystick_float(clamp(args[1]), -clamp(args[2]))
        elif args[0] == 'moverjoy':
            self.gamepad.right_joystick_float(clamp(args[1]), -clamp(args[2]))
        elif args[0] == 'clicked':
            pass
            if args[1] == 'lj':
                self.gamepad.left(1.0)
                self.gamepad.update()
                time.sleep(0.1)
                self.gamepad.left_trigger_float(0.0)
            elif args[1] == 'rj':
                self.gamepad.left_trigger_float(1.0)
                self.gamepad.update()
                time.sleep(0.1)
                self.gamepad.left_trigger_float(0.0)
            else:
                self.gamepad.press_button(xyab_mapping[args[1]])
                self.gamepad.update()
                time.sleep(0.1)
                self.gamepad.release_button(xyab_mapping[args[1]])
        self.gamepad.update()
    def leave(self):
        pass

players: typing.Dict[int, Player] = {}

def playerJoined(client, server):
    print(f"System] Player {client['id']} joined.")
    players[client['id']] = Player()

def playerMessage(client, server, message):
    print(f"Player {client['id']}: {message}")
    players[client['id']].interpret(message)

def playerLeft(client, server):
    print(f"System] Player {client['id']} left.")
    players[client['id']].leave()
    del players[client['id']]

# server = WebSocketServer(host=HOST, port=PORT)
server = websocket_server.WebsocketServer(host=HOST, port=PORT)
server.set_fn_new_client(playerJoined)
server.set_fn_message_received(playerMessage)
server.set_fn_client_left(playerLeft)

try:
    print(f"System] Start WebSocket server on {HOST}:{PORT}")
    os.system("adb reverse tcp:12121 tcp:60000")
    # server.run_forever()
    server.serve_forever()
except KeyboardInterrupt:
    print("System] Close server...")
    os.system("adb reverse --remove tcp:12121")
    server.server_close()