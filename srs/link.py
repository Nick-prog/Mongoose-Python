class Node:

    def __init__(self, data: str):
        self.data = data
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None

    def append(self, data:str ):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def display(self, file):
        current = self.head
        with open(file, 'w') as f:
            while current:
                print(current.data, end= '->', file=f)
                current = current.next
            print("None\n", file=f)
            return

    def delete(self, data):
        current = self.head
        if current and current.data == data:
            self.head = current.next
            current = None
            return
        
        prev = None
        while current and current.data != data:
            prev = current
            current = current.next

        if current is None:
            print("Value not found in list.")
            return
        
        prev.next = current.next
        current = None