# python4twitch

1. Get Twitch chat token here: https://twitchapps.com/tmi/

2. Create A Telegram Bot Using Telegram’s BotFather
    Open your telegram app and search for BotFather.
    Type /newbot to create a new bot. After completing the setup you'll get the Telegram bot’s token.

3. In Telegram bot chat send a random message to your bot. 
    Run get_chat_id.py script.
    In the result look for 'chat': {'id': 
    The number behind it is the Chat Id.

4. Create telegram_id.txt in Notepad. Type 0 in it and save in the same folder as the script.

5. Put channels and keywords in self.channels and self.keywords respectively.
