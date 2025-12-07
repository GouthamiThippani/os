import random

class IndexedAllocation:
    def __init__(self, total_blocks):
        # 0 = free, 1 = used
        self.disk = [0] * total_blocks
        self.files = {}          # stores {filename: index_block}
        self.index_table = {}    # stores {index_block: [data_blocks]}

    def allocate(self, name, size):
        if name in self.files:
            print(f"Error: File '{name}' already exists.")
            self.show_disk()
            return False

        # Find all free blocks
        free = [i for i, b in enumerate(self.disk) if b == 0]

        # Need one block for index + size blocks for data
        if len(free) < size + 1:
            print("Error: Not enough free blocks.")
            self.show_disk()
            return False

        # Randomly choose one block as index
        index = random.choice(free)
        self.disk[index] = 1
        free.remove(index)

        # Randomly choose data blocks
        data = random.sample(free, size)
        for b in data:
            self.disk[b] = 1

        # Save file info
        self.files[name] = index
        self.index_table[index] = data
        print(f"{name} allocated: index {index} -> data blocks {data}")
        self.show_disk()
        return True

  
    def deallocate(self, name):
        if name not in self.files:
            print("Error: File not found.")
            self.show_disk()
            return False

        index = self.files.pop(name)
        # Free data blocks
        for b in self.index_table.pop(index, []):
            self.disk[b] = 0
        # Free index block
        self.disk[index] = 0
        print(f"{name} deallocated (index {index} and its data blocks freed)")
        self.show_disk()
        return True

    def show_disk(self):
        print("Disk Status:", self.disk)
        print("--------------------------------------------------")


# Demo
if __name__ == "__main__":
    indexed = IndexedAllocation(20)
    indexed.allocate("FileC", 5)
 
    indexed.deallocate("FileC")
