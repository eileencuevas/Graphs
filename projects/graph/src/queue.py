class Queue:
    def __init__(self):
        self.queue_size = 0
        self.storage = []

    def enqueue(self, item):
        self.queue_size += 1
        self.storage.append(item)

    def dequeue(self):
        if self.queue_size > 0:
            self.queue_size -= 1
            return self.storage.pop(0)

    def size(self):
        return self.queue_size
