import asyncio
import threading
import time
import queue
import logging


logging.basicConfig(filename="RunningInfo.log", level=logging.INFO, filemode='w')

async def async_function(queue: asyncio.Queue):
    try:
        while True:
                # print("async:")
                l = queue.get()
                async with asyncio.Lock():
                    l['async'] += 1
                    logging.info(f"asycn {l}")
                queue.put(l)
                await asyncio.sleep(6)
    except KeyboardInterrupt:
        print("End async function")

def thread_function(queue: queue.Queue):
    try:
        while True:
            # print("threading:")
            l = queue.get()
            l['thread'] += 1
            logging.info(f"thread {l}")
            queue.put(l)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("End async function")

if __name__ == "__main__":
    q = queue.Queue()
    
    t1 = threading.Thread(target=thread_function, args=(q,))

    l = {
        'async': 0,
        'thread': 0
    }

    q.put(l)

    t1.start()
    print("asyncio running...")
    print("thread running...")
    asyncio.run(async_function(q))


    t1.join()