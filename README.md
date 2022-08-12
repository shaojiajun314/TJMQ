# TJMQ
Lightweight MQ for python

this MQ provide server and client

we can transfer msg p2p by server and client

# config
```shell
# change store dir (./var is the default dir)
export FifoDiskQueueDir=your_dir
```

****************************

# Demo
### server demo:
```python
from TJMQ.tj_mq.server import Server
if __name__ == '__main__':
    Server(port=5671).run()
```

### client demo:
```python
# client pusher
from TJMQ.tj_mq.client import Client
if __name__ == '__main__':
    c = Client(ip='127.0.0.1', port=5671)
    for i in range(50):
        c.push('queue1', str(i).encode())
    for i in range(50):
        c.push('queue2', str(i).encode())
    print('done')


# client puller from net
from TJMQ.tj_mq.client import Client
if __name__ == '__main__':
    c = Client(ip='127.0.0.1', port=5671, from_queue=False)
    for i in range(50):
        d = c.pop('queue1')
        print('queue1', d)
    for i in range(50):
        d = c.pop('queue2')
        print('queue2', d)

# client puller from queue, this mode require that client and server deploy on the same computer
from TJMQ.tj_mq.client import Client
if __name__ == '__main__':
    c = Client(ip='127.0.0.1', port=5671, from_queue=True)
    for i in range(50):
        d = c.pop('queue1')
        print('queue1', d)
    for i in range(50):
        d = c.pop('queue2')
        print('queue2', d)
```

****************************
# Overload Module
### Authority Authentication
#### server
The default strategy is that server accept all request
```python
from TJMQ.tj_mq.server import Server
class YourServer(Server):
  def receive_auth(self, msg):
      print(f'receive auth msg: {msg}')
      if do_sth(msg):
        return True # authorized
      else:
        return False # authentication failure
```

#### client
```python
from TJMQ.tj_mq.client import Client
class YourClient(Client):
  def send_auth(self):
    return sth # some bytes
```
