#随即等待
#防止反爬
import random
import time

def random_sleep(a=1, b=3):
    time.sleep(random.uniform(a, b))