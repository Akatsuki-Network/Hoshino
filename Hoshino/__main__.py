from Hoshino import ptbhoshi, pyrohoshi, setup_telegram_logging, hoshi

def main() -> None:
    ptbhoshi.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    pyrohoshi.start()  
    setup_telegram_logging()  # Set up Telegram log handler after Pyro client starts
    hoshi.info("Pyrogram client started successfully.")
    main()
