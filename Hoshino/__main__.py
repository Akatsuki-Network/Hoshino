from Hoshino import ptbhoshi, pyrohoshi

def main() -> None:    
   
    ptbhoshi.run_polling()
    ai_hoshi = pyrohoshi()  
    ai_hoshi.run() 

if __name__ == "__main__":
    main()
