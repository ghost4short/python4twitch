from time import sleep
import socket
import requests
from threading import Thread
import urllib.request, json

class GhostBot:

    def __init__(self):
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.nickname = 'your twitch channel name'
        self.TwitchToken = 'yout twitch chat token'
        self.channels = ['channel 1', 'channel 2'] #Comma separated channel names, without capitalization.
        self.keywords = ['keyword ', 'keyword 2'] #Comma separated list of keyword, case sensitive.
        self.TelegramToken = "your Telegram bot token"
        self.TelegramChat_id = "your Telegram bot chat id"
        
    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.server, self.port))
        self.sock.send((f"PASS {self.TwitchToken}\n\r").encode())
        self.sock.send((f"NICK {self.nickname}\n\r").encode())
        for ch in self.channels:
            self.sock.send((f"JOIN #{ch}\n\r").encode())

    def send_message(self, channel, text):
        print(f"From Telegram - Channel: {channel} / Message: {text}")
        self.sock.send((f"PRIVMSG #{channel} :{text}\r\n").encode())
  
    def check_role(self, ch, usr): #Completely unnecessary.
        with urllib.request.urlopen(f"https://tmi.twitch.tv/group/user/{ch}/chatters") as url:
            data = json.load(url)
        for role in data['chatters']:
            if usr in data['chatters'][role]:
                return(role)

    def handle_chat(self, irc_resp): #Reads all chat and sends the message to your telegram bot when the message contains any of the keywords anywhere in the message.
        if irc_resp.startswith('PING'):
            self.sock.send(('PONG :tmi.twitch.tv\r\n').encode())
        elif len(irc_resp) > 0:
            if irc_resp.find("PRIVMSG")>0:
                message = irc_resp.split(":")
                chat_user = message[1].split("!")
                channel = chat_user[1].split("#")
                u_role = self.check_role(channel[1].strip(), chat_user[0])
                for si in self.keywords:
                    if message[2].find(si)>-1:
                        print(f"From Twitch - Channel: {channel[1]} / User: {chat_user[0]} / Message: {message[2]}")
                        url = f"https://api.telegram.org/bot{self.TelegramToken}/sendMessage?chat_id={self.TelegramChat_id}&text=Channel:%20{channel[1]}%0AUser:%20{chat_user[0]}%20({u_role})%0AMessage:%20{message[2]}"
                        requests.get(url).json()
                        break
        else:
            next

# Hit a Reply to message in telegram and this function forwards the Reply to the Twitch chat in the channel the message came from. 
# Ignores non-replies. Start a reply with @ (empty space behind @) It will automatically @ (tag) the user you are replying to.
    def handle_telegram(self, t_recv): 
        up_id = t_recv['result'][0]['update_id']
        if "reply_to_message" in t_recv['result'][0]['message']:
            t_id_file = open("telegram_id.txt", "r")
            t_id = int(t_id_file.read())
            if up_id>t_id:
                r_message = t_recv['result'][0]['message']['text']
                r_chan_text = t_recv['result'][0]['message']['reply_to_message']['text'].split(" ")
                r_chan_id = r_chan_text[1]
                r_user_text = r_chan_text[3].split("\n")
                r_user_id = r_user_text[0]
                if r_message.startswith('@ '):
                    self.send_message(r_chan_id, f"@{r_user_id} {r_message}")
                else:
                    self.send_message(r_chan_id, r_message)                                     
                f = open("telegram_id.txt", "w")
                f.write(str(up_id))
                f.close()
        else:
            next

    def listen_chat(self):
        try:
            while True:
                try:
                    resp = self.sock.recv(2048).decode()
                    self.handle_chat(resp)
                except:
                    sleep(5)
                    print("Twitch chat connection error!")
                    gbi.connect()
                    pass
        except KeyboardInterrupt:
            self.sock.close()
            exit()

    def listen_telegram(self):
        try:
            while True:                
                try:
                    url = f"https://api.telegram.org/bot{self.TelegramToken}/getUpdates?limit=1&offset=-1&timeout=5"
                    recv = requests.get(url).json()
                    self.handle_telegram(recv)
                except:
                    print("Telegram timeout error!")
                    sleep(5)
                    pass
                sleep(5)
        except KeyboardInterrupt:
            exit()

if __name__ == '__main__':
    gbi = GhostBot()
    ircCon=False
    while not ircCon:
        try:
            gbi.connect()
            ircCon=True
        except ConnectionResetError:
            pass
    chatThread = Thread(target=gbi.listen_chat)
    telegramThread = Thread(target=gbi.listen_telegram)
    chatThread.start()
    telegramThread.start()