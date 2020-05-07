

import tornado.web
import tornado.websocket
import tornado.template
import tornado.ioloop
import tornado.options
import json


def create_event(event, func):
    event = func


def send_command(command ):
    cmd = {"body": {"origin": {"type": "player"},"commandLine": command,"version": 1},"header": {"requestId": "00000000-0000-0000-0000-000000000000","messagePurpose": "commandRequest", "version": 1,"messageType": "commandRequest" }}
    WSHandler.mcws.write_message(cmd)


class event():
    def on_message(player, message):
        pass
    def on_blockbroken():
        pass

############ EVENT LIST ##############
eventlist = ["PlayerMessage","BlockBroken","BlockPlaced"]
######################################

############# Websocket Connect Event #########
class WSHandler(tornado.websocket.WebSocketHandler):
  mcws = None
  def open(self):
    print('Connect to a client.Now subscribe to all event...')
    for event in eventlist:
        event = "{\"body\": {\"eventName\": \"%s\"},\"header\": {\"requestId\": \"00000000-0000-0000-0000-000000000000\",\"messagePurpose\": \"subscribe\",\"version\": 1,\"messageType\": \"commandRequest\"}}" % event
        self.write_message(event)
        print(self)
        WSHandler.mcws = self


################################################



############ MINECRAFT CALLBACK EVENTS##############


  def on_message(self, message):
    try:
        package = json.loads(message)
    except:
        print("Make Sure You Connected To Minecraft Not Normal Websocket Client.")
    try:
        if package["body"]["eventName"] == "PlayerMessage":
            player = {"name":package["body"]["properties"]["Sender"],"language":package["body"]["properties"]["locale"],"edition":package["body"]["properties"]["editionType"]}
            sendmsg = {"message":package["body"]["properties"]["Message"],"type":package["body"]["properties"]["MessageType"]}
            event.on_message(player, sendmsg)
    except:
        pass
    try:
        if package["body"]["eventName"] == "BlockBroken":
            print(package)
    except:
        pass
    try:
        if package["body"]["eventName"] == "BlockPlaced":
            print(package)
    except:
        pass



###############################################



##########CLOSE EVENT + START SERVER ##########


  def on_close(self):
    print('connection closed...')
def startserver():
    print("use /connect 127.0.0.1:8765/mcbw ingame")
    application = tornado.web.Application([
        (r'/mcbw', WSHandler)
        ])
    application.listen(8765)
    tornado.ioloop.IOLoop.instance().start()
################################################
