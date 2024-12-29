from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import time

# Replace with your API ID, API Hash, and Bot Token
API_ID = '29732480'  # Get this from https://my.telegram.org/auth
API_HASH = '0eaeef7ea191be42709b1e4eb4129ae2'  # Get this from https://my.telegram.org/auth
BOT_TOKEN = '7668554192:AAFFhJLfitnTzhDfMWzb5evslqqLlrmMzEI'  # Get this from @BotFather

# Initialize the bot with your API credentials
app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document)
async def send_file_url(client, message):
    """
    When a user sends a document, this function generates and sends the direct link to the file.
    """
    try:
        # Get file information
        file_id = message.document.file_id
        file_name = message.document.file_name

        # Get file from Telegram's servers using the file_id
        file = await client.get_file(file_id)

        # We need to get the file URL by combining bot token and file path
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

        # Respond with the generated link
        await message.reply_text(f"Here is your direct link for the file:\n\n{file_url}\n\nFile Name: {file_name}")

    except FloodWait as e:
        # Handle Telegram rate limits gracefully
        await message.reply_text(f"Rate limit exceeded, please wait {e.x} seconds before trying again.")
        time.sleep(e.x)
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@app.on_message(filters.command("start"))
async def start_command(client, message):
    """
    Responds to the /start command with instructions.
    """
    await message.reply_text("Welcome to the File-to-Link Generator Bot!\n\n"
                              "Send me a file, and I will generate a direct link for you.")

if __name__ == "__main__":
    app.run()
