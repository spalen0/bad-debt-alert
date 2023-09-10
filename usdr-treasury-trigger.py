import os, requests, datetime, locale
import asyncio, telegram


def get_dai_in_treasury():
    dai_address = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
    url = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={dai_address}&address={treasury_address}&tag=latest&apikey={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        balance = int(response.json()["result"]) / 10**18
        print(f"The balance of Treasury in DAI is {balance}")
        return balance
    else:
        print(f"Request failed with status code {response.status_code}")
        return 0


def get_usdr_total_supply():
    token_address = "0x40379a439d4f6795b6fc9aa5687db461677a2dba"
    url = f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={token_address}&apikey={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        supply = int(response.json()["result"]) / 10**9
        print(f"The total supply of {token_address} is {supply}")
        return supply
    else:
        print(f"Request failed with status code {response.status_code}")
        return 0


api_key = os.environ["POLYGON_KEY"]
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

treasury_address = "0x6ef682f0223687c625e6c4a115f544a80c37da33"

dai_in_treasury = get_dai_in_treasury()
usdr_total_supply = get_usdr_total_supply()

# ratio of dai in treasury to total supply of usdr
ratio_of_dai_to_usdr = round(dai_in_treasury / usdr_total_supply * 100, 2)
print(
    f"The ratio of DAI in treasury to total supply of USDR is {ratio_of_dai_to_usdr}%"
)

threshold_ratio = float(os.getenv("USDR_DAI_THRESHOLD_RATIO", 100))

date = datetime.datetime.now()
formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
message = f"⚠️  USDR treasury has {ratio_of_dai_to_usdr}% of DAI at {formatted_date} ⚠️\nDAI in treasury: {dai_in_treasury:,.2f}\nTotal supply of USDR: {usdr_total_supply:,.2f}"
print(message)

if ratio_of_dai_to_usdr < threshold_ratio:
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    chat_id = os.environ["TELEGRAM_USDR_CHAT_ID"]
    print(f"Sending Telegram message")
    asyncio.run(bot.send_message(chat_id=chat_id, text=message))
