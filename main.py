import asyncio

import processor

import twitter


async def main():
    twitter.login()
    processor.init_db()
    await processor.process_loop_search()


if __name__ == "__main__":
    asyncio.run(main())
