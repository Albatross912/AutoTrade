import threading
from neo_api_client import NeoAPI


# Define callback functions
def on_message(message):
    print("Message received:", message)


def on_close(message):
    print("Connection closed:", message)


def on_open(message):
    print("Connection opened:", message)


def on_error(error_message):
    print("Error occurred:", error_message)


# Define a callback function specifically for handling quote responses
def on_quote_received(quote_data):
    print("Quote received:", quote_data)


# Initialize client
client = NeoAPI(
    consumer_key="PPxoVSopZTI_2ujFbU3rdabWHsga",
    consumer_secret="IU5sFNqJF5_8DPAqLlGKqEbyuHga",
    environment="prod"
)

# Set standard callbacks
client.on_message = on_message
client.on_close = on_close
client.on_open = on_open
client.on_error = on_error

# Define instrument tokens
inst_tokens = [
    {"instrument_token": "26000", "exchange_segment": "nse_cm"},
    {"instrument_token": "1594", "exchange_segment": "nse_cm"},
    {"instrument_token": "11915", "exchange_segment": "nse_cm"},
    {"instrument_token": "13245", "exchange_segment": "nse_cm"}
]


# Method to asynchronously handle quotes
def subscribe_to_quotes():
    try:
        # Log in and authenticate
        client.login(mobilenumber="+919610684338", password="Passwd$912")

        # Ask user for OTP input
        otp = input("Please enter the OTP sent to your mobile number: ")
        client.session_2fa(OTP=otp)

        # Subscribe to the quotes with async callback
        client.quotes(
            instrument_tokens=inst_tokens,
            callback=on_message()  # Pass the quote callback
        )
    except Exception as e:
        print(f"Exception while subscribing to quotes: {e}")


# Run the quote subscription in a separate thread
quote_thread = threading.Thread(target=subscribe_to_quotes)
quote_thread.start()

# Main program can perform other tasks here
print("Quote subscription started in a separate thread.")
