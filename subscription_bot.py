import discord
import os, requests
import datetime
import time
import asyncio


COUNTER = 70

headers = {
    "accept": "application/json",
    "x-client-id": "309166281246dddd1cf4405c19661903",
    "x-client-secret": "88db0d7814415b80e7869cf7443caa85e3b472d8",
    "x-api-version": "2022-09-01",
    "content-type": "application/json"
}

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    
    global COUNTER
    print(message.content)
    

    if message.content.startswith('!hello'):
        await message.reply('Hello!')

    if message.content == '!help':
        await message.reply("**!buy** \n\t- _buy extension subscription_\n**!check_validity** \n\t- _check subscription validity/status_")

    if message.content == '!buy':
        link_id = f"my_link_id{COUNTER}"
        payload = {
            "customer_details": {
                "customer_phone": "9876543210",
                "customer_email": "customer@mail.com",
                "customer_name": "Divij"
            },
            "link_notify": {
                "send_sms": False,
                "send_email": False
            },
            "link_id": link_id, # Unique ID
            "link_amount": 100,
            "link_currency": "INR",
            "link_purpose": "extension_subscription"
        }

        COUNTER += 1
        url = "https://sandbox.cashfree.com/pg/links"
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        await message.reply(response.json()['link_url'])
        print('Payment Link Sent !')

        asyncio.create_task(check_payment_status(message, link_id))


async def check_payment_status(message, link_id):
    url = f"https://sandbox.cashfree.com/pg/links/{link_id}"

    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < 300:
        res = requests.get(url, headers=headers, verify=False)
        if res.json()['link_status'] == 'PAID':
            await message.reply('Congrats! You have successfully subscribed. Here is your Token - 1@10!c73cwd')
            break
        time.sleep(5)
    if res.json()['link_status'] == 'ACTIVE':
        await message.reply('Payment failed! Try again.')

# client.run(os.environ['TOKEN'])
client.run('OTIwMTY4MjU4MjgyMzI4MDk0.GKqp-g.mD_eeQ-a4Ks0g_BK72mMYtzrhah19Zd8NHl3bo')