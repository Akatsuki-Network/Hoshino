from Hoshino import ptbhoshi, pyrohoshi
import pyrogram

def main():
    ptbhoshi.run_polling()

async def run_clients():
      await pyrohoshi.start()
      await pyrogram.idle()
             
if __name__ == "__main__":
    main()
    pyrohoshi.loop.run_until_complete(run_clients())
    
