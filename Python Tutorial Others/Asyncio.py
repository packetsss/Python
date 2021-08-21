import asyncio

async def print_nums():
    for i in range(10):
        print(f"{i}, ", end="")
        await asyncio.sleep(0.25)
    print("Done task 2")

async def foo(text):
    print(text)

    await asyncio.sleep(1)
    # returns a co-routine
    # must be inside async function

    print("\nDone task 1")

async def main():
    print("Hi?!")
    task1 = asyncio.create_task(foo("Me"))
    task2 = asyncio.create_task(print_nums())

    value = await task1
    # wait for task to finish
    print(f"\nvalue: {value}")
    await task2

    await asyncio.sleep(0.5)
    # wait 0.5s after task 1 finishes

    print("\nFinished")

asyncio.run(main())
# create an event loop and run the code
