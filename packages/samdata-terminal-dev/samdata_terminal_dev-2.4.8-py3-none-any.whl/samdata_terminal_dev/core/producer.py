from queue import Queue
import threading
from concurrent.futures import ThreadPoolExecutor

log_queue = Queue()
order_queue = Queue()

def OrderProduce(order):
    """
    订单生产者
    """
    global order_queue
    order_queue.put(order)

def LogProduce(log):
    """
    日志生产者
    """
    global log_queue
    log_queue.put(log)

