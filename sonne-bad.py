import os, requests, datetime
import asyncio, telegram

url = 'https://raw.githubusercontent.com/Risk-DAO/simulation-results/main/bad-debt/latest/optimism_sonne.json'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    total = int(data['total']) * -1
    decimals = int(data['decimals'])
    updated = int(data['updated'])
    debt = round(total / 10 ** decimals, 2)
    date = datetime.datetime.fromtimestamp(updated)

    if total > int(os.environ['DEBT_TRIGGER']):
        bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])
        chat_id = os.environ['TELEGRAM_CHAT_ID']
        print(f'Sending message to {chat_id}')
        asyncio.run(bot.send_message(chat_id=chat_id, text=f'⚠️ Sonne Bad debt trigger reached: ${debt} at {date} ⚠️'))

    print(f':red_circle: Total: ${debt}')
    print(f'Updated: {date}')
else:
    print(f'Request failed with status code {response.status_code}')
