import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))


from TJMQ.tj_mq.client import Client


if __name__ == '__main__':
    c = Client(ip='127.0.0.1', port=5671, from_queue=False)
    for i in range(50):
        d = c.pop('queue1')
        print('queue1', d)
    for i in range(50):
        d = c.pop('queue2')
        print('queue2', d)