from Hoshino import ptbhoshi, pyrohoshi
import asyncio

async def main():
    await pyrohoshi().start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    ptb_task = loop.create_task(ptbhoshi.run_polling())

    loop.run_until_complete(main())

    loop.run_until_complete(ptb_task)
