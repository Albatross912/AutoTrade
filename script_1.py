from kotakneo import KotakNeoClient

# Initialize the client with your API key and secret
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
client = KotakNeoClient(api_key=API_KEY, api_secret=API_SECRET)

# Authenticate
client.login()

# Define your parameters
symbol = "MID"  # The index you are trading on, e.g., Nifty MID cap
strike_price = 13000
option_type = "PE"  # Put option
buy_price_range = (100, 105)  # Buy price range
stop_loss_price = 95  # Stop-loss price
target_profit_difference = 5  # Target is 5 Rs more than buy price

# Find the trading symbol for the given parameters
trading_symbol = f"{symbol} {strike_price} {option_type}"

# Fetch the current price (you may need to use an API call to get the LTP)
ltp = client.get_ltp(trading_symbol)  # Replace with the actual API method for LTP

# Determine the buy price within the given range
if buy_price_range[0] <= ltp <= buy_price_range[1]:
    buy_price = ltp
else:
    print(f"LTP {ltp} is outside the buy range {buy_price_range}")
    exit()

# Place a buy order at the buy price
order_id = client.place_order(
    trading_symbol=trading_symbol,
    transaction_type="BUY",
    price=buy_price,
    quantity=1,  # Replace with the desired quantity
    order_type="LIMIT"
)
print(f"Order placed successfully. Order ID: {order_id}")

# Define target and stop-loss prices based on the buy price
target_price = buy_price + target_profit_difference
stop_loss_price = 95

# Monitor the price to either hit the target or the stop-loss
while True:
    current_price = client.get_ltp(trading_symbol)  # Replace with the method for fetching live prices

    # Check for stop-loss condition
    if current_price <= stop_loss_price:
        client.place_order(
            trading_symbol=trading_symbol,
            transaction_type="SELL",
            price=current_price,
            quantity=1,  # Replace with the desired quantity
            order_type="MARKET"
        )
        print(f"Stop-loss hit at {current_price}. Order sold.")
        break

    # Check for target condition
    elif current_price >= target_price:
        client.place_order(
            trading_symbol=trading_symbol,
            transaction_type="SELL",
            price=current_price,
            quantity=1,  # Replace with the desired quantity
            order_type="MARKET"
        )
        print(f"Target reached at {current_price}. Order sold.")
        break
