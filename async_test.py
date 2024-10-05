import asyncio
import sys

# interruption flag for other tasks 
interrupt_flag = False

async def read_input():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    # Создаем поток для чтения из stdin
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    global interrupt_flag
    while True:
        # Читаем строку из stdin
        line = await reader.readline()
        if not line:
            interrupt_flag = True  # Прерывание выполнения из других задач
            break  # Если EOF, выходим из цикла
        message = line.decode().strip()
        print(f"Entered message: {message}")
        # Здесь можно добавить логику для прерывания выполнения
        if message == "stop":
            interrupt_flag = True  # Прерывание выполнения из других задач

async def perform_other_tasks():
    global interrupt_flag
    while True:
        if interrupt_flag:
            print("Stopping execution...")  # Здесь можно добавить логику для прерывания выполнения
            interrupt_flag = False
            return
        print("Performing other tasks...")
        await asyncio.sleep(5)  # Имитация длительной работы

async def main():
    listener_task = asyncio.create_task(read_input())
    other_tasks_task = asyncio.create_task(perform_other_tasks())

    await asyncio.gather(listener_task, other_tasks_task)

if __name__ == "__main__":
    asyncio.run(main())