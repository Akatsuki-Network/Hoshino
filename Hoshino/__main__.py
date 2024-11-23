from Hoshino import ptbhoshi, pyrohoshi, telegram_handler

def main() -> None:
    """kuch nahi bhai gend fat gayi ye kang karne me choro kya hi bolu abb"""
    ptbhoshi.run_polling(drop_pending_updates=True)
    
if __name__ == "__main__":
    pyrohoshi.start()
    telegram_handler.set_client_ready()
    main()
