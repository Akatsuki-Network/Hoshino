from Hoshino import ptbhoshi, pyrohoshi, setup_telegram_logging, hoshi, capture_err
from config import CHAT_ID

@capture_err
async def sample_command(pyrohoshi, message):
    raise ValueError("Test error handling")

def main() -> None:
    ptbhoshi.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:
        pyrohoshi.start()  
        setup_telegram_logging()
        hoshi.info("Pyrogram client started successfully.")
        main()
    except Exception as e:
        hoshi.error(f"Failed to start bot due to error: {e}")
        pyrohoshi.send_message(CHAT_ID, f"**Critical Error in Bot Startup**: {e}")
