from Hoshino import ptbhoshi, pyrohoshi

async def main():
    await ptbhoshi.initialize()
    await pyrohoshi.start()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
