import time
import asyncio
from rasa.core.agent import Agent
from multiprocessing import freeze_support
import os
import psutil
from memory_profiler import memory_usage
# Đường dẫn tới file model Rasa của bạn
model_path = "models/20230828-171633.tar.gz"

# Tạo đối tượng Agent từ model
agent = Agent.load(model_path)

async def measure_time():
    # Lời chào
    start_time = time.time()
    response = await agent.handle_text("Xin chào")
    end_time = time.time()

    # Tính thời gian chạy model
    elapsed_time = end_time - start_time
    print(f"Thời gian chạy model: {elapsed_time} giây")

def measure_memory():
    process = psutil.Process(os.getpid())
    memory_usage_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_usage_mb} MB")

# Hàm để đo CPU
def measure_cpu():
    cpu_percent = psutil.cpu_percent()
    print(f"CPU usage: {cpu_percent}%")
    
if __name__ == '__main__':
    freeze_support()
    
    # Đo bộ nhớ và CPU trước khi chạy model
    measure_memory()
    measure_cpu()

    # Đo bộ nhớ và CPU trong quá trình chạy model
    memory_usage(measure_memory)
    measure_cpu()

    # Đo bộ nhớ và CPU sau khi chạy xong model
    measure_memory()
    measure_cpu()
    
    asyncio.run(measure_time())