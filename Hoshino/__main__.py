from Hoshino import ptbhoshi, pyrohoshi

def main() -> None:
    """Run bot."""
    ptbhoshi.run_polling(drop_pending_updates=True)
    
if __name__ == "__main__":
    pyrohoshi.start()
    main()
