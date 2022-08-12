import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from TJMQ.tj_mq.server import Server


Server(port=5671).run()
