import requests
botToken = "Your TelegramBotToken"
url = f"https://api.telegram.org/bot{botToken}/getUpdates"
print(requests.get(url).json())