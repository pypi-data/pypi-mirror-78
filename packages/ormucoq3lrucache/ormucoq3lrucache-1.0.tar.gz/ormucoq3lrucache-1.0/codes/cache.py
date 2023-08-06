import datetime

class _Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None
        self.createTime = datetime.datetime.now()

class lru_cache():
    def __init__(self):
        self.size = 5
        self.hmap = {}
        self.head = _Node(0, 0)
        self.tail = _Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def put(self, key, val):
        if key in self.hmap:
            self.__removeNode(self.hmap[key])
        
        node = _Node(key, val)
        self.hmap[key] = node
        self.__addToTail(node)

        if len(self.hmap) > self.size:
            node = self.head.next
            del self.hmap[node.key]
            self.__removeNode(node)
    
    def get(self, key):
        if key in self.hmap:
            node = self.hmap[key]
            self.__removeNode(node)
            self.__addToTail(node)
            return {'key': node.key, 'value': node.val, 'create date': node.createTime.isoformat()}
        else:
            raise ValueError('Invalid Key')
    
    def view(self):
        node = self.tail.prev
        lru = []
        while node.prev:
            lru.append({'key': node.key, 'value': node.val, 'create date': node.createTime.isoformat()})
            node = node.prev
        return lru
    
    # expiry = seconds from creat date to expiry dates
    def removeExpired(self, expiry):
        currentTime = datetime.datetime.now()

        node = self.head.next
        while node.next:
            if currentTime-node.createTime > datetime.timedelta(seconds=expiry):
                self.__removeNode(node)
            node = node.next

    def reset(self):
        self.head.next = self.tail
        self.tail.prev = self.head
        self.hmap = {}

    def __removeNode(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def __addToTail(self, node):
        node.next = self.tail
        node.prev = self.tail.prev
        self.tail.prev.next = node
        self.tail.prev = node