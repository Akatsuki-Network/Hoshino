from Hoshino import ptbhoshi, pyrohoshi
import asyncio

async def main():
    await ptbhoshi.initialize()
    await pyrohoshi.start()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
