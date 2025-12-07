import random

# Linked Allocation
class LinkedAllocation:
    def __init__(self, block_size):
        # Create disk of given size (0 = free, 1 = used)
        self.disk = [0] * block_size
        # Store file starting block
        self.files = {}
        # Store next pointers for each block
        self.next_block = {}

    def allocate(self, name, size):
        # Find all free blocks
        free = [i for i, b in enumerate(self.disk) if b == 0]
        if len(free) < size:
            print("Error: Not enough space to allocate", name)
            self.show_disk()
            return
        
        # Randomly select free blocks to simulate linked allocation
        blocks = random.sample(free, size)

        # Mark selected blocks as used
        for b in blocks:
            self.disk[b] = 1

        # Link the blocks (chain)
        for i in range(size - 1):
            self.next_block[blocks[i]] = blocks[i + 1]
        self.next_block[blocks[-1]] = -1  # -1 indicates end of file

        # Store starting block of the file
        self.files[name] = blocks[0]
        print(f"{name} allocated in blocks {blocks}")
        self.show_disk()
    def deallocate(self, name):
        if name not in self.files:
            print("Error: File not found.")
            self.show_disk()
            return

        # Traverse and free all blocks linked to the file
        current = self.files.pop(name)
        while current != -1:
            self.disk[current] = 0
            nxt = self.next_block.pop(current)
            current = nxt
        print(f"{name} deallocated successfully")
        self.show_disk()

    def show_disk(self):
        print("Disk Status:", self.disk)
        print("--------------------------------------------------")


# Main Program
if __name__ == "__main__":
    linked = LinkedAllocation(20)
    linked.allocate("FileB", 5)
    
    linked.deallocate("FileB")
