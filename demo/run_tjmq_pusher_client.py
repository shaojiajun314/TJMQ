import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from TJMQ.tj_mq.client import Client
from time import sleep


if __name__ == '__main__':
    c = Client(ip='127.0.0.1', port=5671)
    for i in range(50):
        c.push('queue1', str(i).encode())
    for i in range(50):
        c.push('queue2', str(i).encode())
    sleep(2)
    print('done')