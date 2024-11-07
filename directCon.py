from telethon import TelegramClient, events
import logging

logging.basicConfig(level=logging.INFO)
# Your API ID and Hash from my.telegram.org
api_id = 27412019  # Your API ID
api_hash = '53076f53c61caa3afcabfd5dc4bbe690'  # Your API hash

# Your bot token from BotFather
bot_token = '7824222086:AAHxmNIXsEINjaUEThp0FFP6KXOGgkW7yyw'  # Replace with your actual bot token

# Channel Username or ID (For example, '@my_channel_name' or '1234567890')
channel_username = '@finearts912'

# Choose a name for your client session
async def main():
    # Initialize the Telegram client
    client = TelegramClient('bot_session', api_id, api_hash)
    
    # Start the client with the bot token
    await client.start(bot_token=bot_token)

    print(f"Listening for new messages in {channel_username}...")

    # Event handler to capture new messages from the specific channel
    @client.on(events.NewMessage(chats=channel_username))
    async def handle_new_message(event):
        # Print the message when a new one is received in the specific channel
        print(f"New message in {channel_username}: {event.message.message}")

    # Keep the client running to receive messages
    await client.run_until_disconnected()

# Start the async main function
import asyncio
asyncio.run(main())
