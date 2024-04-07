import asyncio

async def multitask_loop(iterator, callback, max_concurrent_tasks):
    async def perform_action(item):
        try:
            await callback(item)
        except Exception as e:
            print(f"Error: {e}")

    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    async def limited_perform_action(item):
        async with semaphore:
            await perform_action(item)

    tasks = [limited_perform_action(item) for item in iterator]
    await asyncio.gather(*tasks)

# Example callback function
async def my_callback(item):
    # Your specific action or callback logic here
    print(f"Processing item: {item}")
    await asyncio.sleep(5)  # Simulating a delay

def main():
    my_iterator = range(20)  # Example iterator (you can use any iterable)
    max_concurrent = 20 # Maximum concurrent tasks
    asyncio.run(multitask_loop(my_iterator, my_callback, max_concurrent))

# Run the main function (assuming it's in an async environment)
# asyncio.run(main())
