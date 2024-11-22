from Hoshino import ptbhoshi, pyrohoshi

def main() -> None:    
    ptbhoshi.run_polling()
    pyrohoshi().start()
    
if __name__ == "__main__":
    main()
