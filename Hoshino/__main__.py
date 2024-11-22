from Hoshino import ptbhoshi, pyrohoshi

async def main():    
   pyrohoshi().run()   
    
if __name__ == "__main__":
   ptbhoshi.run_polling()  
   pyrohoshi().loop.run_until_complete(main())
   
    
