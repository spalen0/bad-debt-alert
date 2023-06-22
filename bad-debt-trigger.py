import os, requests, datetime
import asyncio, telegram

url = os.environ['DATA_URL']
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    total = int(data['total']) * -1
    decimals = int(data['decimals'])
    updated = int(data['updated'])
    debt = round(total / 10 ** decimals, 2)
    date = datetime.datetime.fromtimestamp(updated)
    threshold = int(os.environ['DEBT_THRESHOLD'])

    if debt > threshold:
        bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])
        chat_id = os.environ['TELEGRAM_CHAT_ID']
        print(f'Sending message')
        protocol = os.environ['PROTOCOL']
        asyncio.run(bot.send_message(chat_id=chat_id, text=f'⚠️ {protocol} Bad Debt: ${debt} at {date} ⚠️'))

    print(f'Total: ${debt}')
    print(f'Updated: {date}')
else:
    print(f'Request failed with status code {response.status_code}')
