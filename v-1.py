from telethon import TelegramClient, events
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# Your API ID and Hash from my.telegram.org
api_id = 27412019  # Your API ID
api_hash = '53076f53c61caa3afcabfd5dc4bbe690'  # Your API hash

# Your bot token from BotFather
bot_token = '7824222086:AAHxmNIXsEINjaUEThp0FFP6KXOGgkW7yyw'  # Replace with your actual bot token

# Channel Username or ID (For example, '@my_channel_name' or '1234567890')
channel_username = '@finearts912'

# File path where filtered messages will be stored
file_path = 'filtered_messages.txt'


async def main():
    # Initialize the Telegram client
    client = TelegramClient('bot_session', api_id, api_hash)

    # Start the client with the bot token
    await client.start(bot_token=bot_token)

    print(f"Listening for new messages in {channel_username}...")

    # Event handler to capture new messages from the specific channel
    @client.on(events.NewMessage(chats=channel_username))
    async def handle_new_message(event):
        message_text = event.message.message

        # Check if the message starts with ❤️ or 💙
        if message_text.startswith('❤️') or message_text.startswith('💙'):
            # Get the current time in HH:MM:SS format
            current_time = datetime.now().strftime("%H:%M:%S")
            # Format the message to be saved
            filtered_message = f"[{current_time}] {message_text}\n"

            # Append the filtered message to the file with UTF-8 encoding
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(filtered_message)

            # Print the filtered message in the console
            print(f"Filtered message: {filtered_message.strip()}")

    # Keep the client running to receive messages
    await client.run_until_disconnected()


# Start the async main function
import asyncio

asyncio.run(main())
