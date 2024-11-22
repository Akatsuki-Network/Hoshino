from Hoshino import ptbhoshi, pyrohoshi

async def main():    
    await pyrohoshi.start()

if __name__ == "__main__":
    import asyncio
    ptbhoshi.run_polling()
    asyncio.run(main())
