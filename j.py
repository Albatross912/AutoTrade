# monday = mid(75), tues = fin(40), wedn = bn(15), thrus = Nifty(25), friday = sensex(10)

from math import isnan

import  neo_api_client

from neo_api_client import NeoAPI


def on_message(message):
    print(message)


def on_error(error_message):
    print(error_message)

def on_close(message):
    print(message)


def on_open(message):
    print(message)

client = NeoAPI(consumer_key="PPxoVSopZTI_2ujFbU3rdabWHsga", consumer_secret="IU5sFNqJF5_8DPAqLlGKqEbyuHga", environment='prod',
                access_token=None, neo_fin_key=None)
client.login(mobilenumber="+919610684338", password="Passwd$912")
client.session_2fa(OTP="223565")


def get_option_chain(symbol, strike_price, expiry="", option_t="PE"):
    # Search all options related to the specified symbol, strike price, and expiry date
    segment = "nse_fo"
    if symbol.upper() == "SENSEX":
        segment = "bse_fo"

    search_response = client.search_scrip(
        exchange_segment=segment,  # NSE Futures and Options segment
        symbol=symbol,
        strike_price=str(strike_price),
        option_type=option_t,  # 'PE' for Put, 'CE' for Call
        expiry=expiry  # Use a specific expiry date or leave it blank
    )

    # Prepare lists to store the result
    inst_tokens = []
    trading_symbol_tokens = []

    # Process the retrieved option chain and build the response
    if search_response:
        for scrip in search_response:
            print(
                f"Instrument Token: {scrip['pSymbol']}, "
                f"Trading Symbol: {scrip['pTrdSymbol']}, "
                f"Expiry Date: {scrip['pExpiryDate']}, "
                f"Option Type: {scrip['pInstType']}"
            )
            inst_tokens.append({
                "instrument_token": scrip['pSymbol'],  # Assuming 'pSymbol' holds instrument token
                "exchange_segment": segment
            })
            trading_symbol_tokens.append({
                "instrument_token": scrip['pSymbol'],
                "trading_symbol": scrip['pTrdSymbol'],
                "strike_price": strike_price,
                "option_type": option_t,
                "symbol": symbol,
            })
    else:
        print(f"No options found for {symbol} with strike price {strike_price} and expiry {expiry}.")

    return inst_tokens, trading_symbol_tokens


# Helper function to gather data for a list of strike prices and both 'CE' and 'PE' options
def collect_options_for_strikes(symbol, strike_prices, expiry):
    inst_tokens = []
    trading_symbol_tokens = []
    for strike_price in strike_prices:
        for option_type in ["CE", "PE"]:  # Looping through Call and Put options
            tokens, symbols = get_option_chain(symbol, strike_price, expiry, option_t=option_type)
            inst_tokens.extend(tokens)
            trading_symbol_tokens.extend(symbols)
    return inst_tokens, trading_symbol_tokens


# Collect results for each symbol and expiry
all_inst_tokens = []
all_trading_symbol_tokens = []

# Define symbol and strike price ranges with expiry dates
option_specs = [
  # {"symbol": "SENSEX", "strike_prices": range(75200, 79100, 100), "expiry": "04feb2035"},
    {"symbol": "NIFTY", "strike_prices": range(21850, 23801, 50), "expiry": "07feb2025"},
   # {"symbol": "BANKNIFTY", "strike_prices": range(47000, 50900, 100), "expiry": "28feb2025"},
   # {"symbol": "FINNIFTY", "strike_prices": range(21800, 25001, 50), "expiry": "27feb2025"},
   # {"symbol": "MIDCPNIFTY", "strike_prices": range(11175, 12151, 25), "expiry": "28feb2025"}
]

# Loop through each option specification and gather tokens
for spec in option_specs:
    inst_tokens, trading_symbol_tokens = collect_options_for_strikes(
        symbol=spec["symbol"],
        strike_prices=spec["strike_prices"],
        expiry=spec["expiry"]
    )
    all_inst_tokens.extend(inst_tokens)
    all_trading_symbol_tokens.extend(trading_symbol_tokens)

# Print the results
print("Instrument Tokens:", all_inst_tokens)
print("Trading Symbols and Strike Prices:", all_trading_symbol_tokens)

import pandas as pd
from datetime import datetime
import time

# Initialize a dictionary to store LTP values for each instrument token
ltp_map = {}


# Define callback function to handle received messages
def on_message(message):
    global ltp_map  # Access the global dictionary to update values
    try:
        # Ensure the message has 'data', expected to be a list of quotes
        if isinstance(message, dict) and 'data' in message:
            # Loop through each entry in the 'data' array
            for data_point in message['data']:
                # Extract instrument token and last price (ltp) if they exist
                instrument_token = data_point.get("tk")
                last_price = data_point.get("ltp")

                if instrument_token and last_price is not None:
                    # Update the dictionary with the latest LTP
                    ltp_map[instrument_token] = last_price
        else:
            print("Received message in an unexpected format:", message)
    except Exception as e:
        print("Error processing message:", e)


# Set up the client to use the defined on_message function
client.on_message = on_message

# Subscribe to tokens to receive live LTP data
client.subscribe(instrument_tokens=all_inst_tokens, isIndex=False, isDepth=False)

import nest_asyncio
from telethon import TelegramClient, events
import logging
from datetime import datetime
import re
import asyncio

# Allow nested event loops in Jupyter notebooks
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

# Your API ID and Hash from my.telegram.org
api_id = 28059844
api_hash = '7ef57d924f83752e18736e32d2fcd7f1'

# Your bot token from BotFather
bot_token = '7824222086:AAHxmNIXsEINjaUEThp0FFP6KXOGgkW7yyw'

# Channel Username or ID
channel_username = '@finearts912'

# File path where filtered messages will be stored
file_path = 'filtered_messages.txt'

# Regular expression pattern to extract components
pattern = r'\b(N|BN|MID|FN|SEN)\s+(\d+)\s+(CE|PE)\b'


# Assume ltp_map and client are defined elsewhere in the context


async def place_order_with_client(client, trading_symbol, quantity):
    segment = "nse_fo"
    if trading_symbol.startswith('SEN'):
        segment = "bse_fo"
    try:
        response = client.place_order(
            exchange_segment=segment,
            product="NRML",
            price="",
            order_type="MKT",
            quantity=str(quantity),
            validity="DAY",
            trading_symbol=trading_symbol,
            transaction_type="B",
            amo="NO",
            disclosed_quantity="0",
            market_protection="0",
            pf="N",
            trigger_price="",
            tag=""
        )
        print(f"Buy order placed successfully for {trading_symbol}: {response}")
    except Exception as e:
        print(f"Failed to place buy order for {trading_symbol}: {e}")


async def sell_order_with_client(client, trading_symbol, quantity):
    segment = "nse_fo"
    if trading_symbol.startswith('SEN'):
        segment = "bse_fo"
    try:
        response = client.place_order(
            exchange_segment=segment,
            product="NRML",
            price="",
            order_type="MKT",
            quantity=str(quantity),
            validity="DAY",
            trading_symbol=trading_symbol,
            transaction_type="S",
            amo="NO",
            disclosed_quantity="0",
            market_protection="0",
            pf="N",
            trigger_price="",
            tag=""
        )
        print(f"Sell order placed successfully for {trading_symbol}: {response}")
    except Exception as e:
        print(f"Failed to place sell order for {trading_symbol}: {e}")


def search_instruments(symbol, strike_price, option_type):
    result = []
    for item in all_trading_symbol_tokens:
        if item['symbol'] == symbol and item['strike_price'] == strike_price and item['option_type'] == option_type:
            result.append({'instrument_token': item['instrument_token'], 'trading_symbol': item['trading_symbol']})
    return result


async def monitor_and_place_order(client, instrument_token, buy_price, trading_symbol, quantity):
    buy_price = float(buy_price)

    while True:
        # Get the current LTP (Last Traded Price) from the map
        ltp = ltp_map.get(instrument_token)

        if ltp is None:
            print(f"LTP not available for instrument token: {instrument_token}")
            await asyncio.sleep(0.5)
            continue

        ltp = float(ltp)
        print(f"LTP of {trading_symbol} : {ltp}")
        # Calculate stop loss and target prices
        stop_loss = buy_price - (0.10 * buy_price)  # 5% below the buy price
        target = buy_price +  (0.05 * buy_price)  # 5% above the buy price

        # Check if LTP hits stop loss or target
        if ltp <= stop_loss or ltp >= target:
            # If LTP hits stop loss or target, sell the position
            await sell_order_with_client(client, trading_symbol, quantity)
            print(f"Sell order placed for {trading_symbol} at LTP {ltp} buy price {buy_price} (Stop Loss or Target hit)")
            break  # Exit the loop after placing the sell order

        # Sleep for a short time before checking again
        await asyncio.sleep(0.5)


async def handle_new_trade(client, symbol, strike_price, option_type, quantity):
    # Search for instruments based on the extracted components
    results = search_instruments(symbol, int(strike_price), option_type)

    if not results:
        print(f"No instrument found for {symbol} {strike_price} {option_type}.")
        return

    trading_symbol = results[0]['trading_symbol']
    instrument_token = results[0]['instrument_token']

    # Place the buy order
    await place_order_with_client(client, trading_symbol, quantity)

    # Get the initial buy price from the LTP map
    buy_price = ltp_map.get(instrument_token)

    if buy_price is None:
        print(f"Buy price not available for instrument token: {instrument_token}")
        return

    # Monitor and place sell order in parallel
    await monitor_and_place_order(client, instrument_token, buy_price, trading_symbol, quantity)


async def main():
    tele_client = TelegramClient('bot_session', api_id, api_hash)

    await tele_client.start(bot_token=bot_token)

    print(f"Listening for new messages in {channel_username}...")

    @tele_client.on(events.NewMessage(chats=channel_username))
    async def handle_new_message(event):
        message_text = event.message.message

        if message_text.startswith('❤️') or message_text.startswith('💙') or message_text.startswith('🔹'):
            match = re.search(pattern, message_text)

            if match:
                stock_type, strike_price, option_type = match.groups()

                symbol_map = {
                    'N': ("NIFTY", 375),
                    'BN': ("BANKNIFTY", 390),
                    'MID': ("MIDCPNIFTY", 400),
                    'SEN': ("SENSEX", 200),
                    'FN': ("FINNIFTY", 400)
                }
                symbol, quantity = symbol_map.get(stock_type, (None, 0))

                if symbol:
                    # Launch a separate task for this trade
                    asyncio.create_task(
                        handle_new_trade(client, symbol, strike_price, option_type, quantity)
                    )
                else:
                    print(f"Unknown stock type: {stock_type}")
            else:
                print("Pattern not matched in message.")

    await tele_client.run_until_disconnected()


asyncio.run(main())
