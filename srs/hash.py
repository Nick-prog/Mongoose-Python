class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class HashLinkedList:
    def __init__(self):
        self.head = None
        self.hash_table = {}  # Hash table to store nodes by their data value

    def append(self, data):
        """Adds a new node to the end of the list and stores it in the hash table"""
        new_node = Node(data)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        # Store node reference in the hash table
        self.hash_table[data] = new_node

    def search(self, target):
        """Searches for a node in O(1) time using the hash table"""
        return self.hash_table.get(target, None)  # O(1) lookup
    
    def display(self, file):
        current = self.head
        with open(file, 'a+') as f:
            while current:
                print(current.data, end= '->', file=f)
                current = current.next
            print("None\n", file=f)
            return

    def delete(self, target):
        """Deletes a node and removes it from the hash table"""
        current = self.head
        previous = None
        while current:
            if current.data == target:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                del self.hash_table[target]  # Remove from hash table
                return True
            previous = current
            current = current.next
        return False  # Node not found