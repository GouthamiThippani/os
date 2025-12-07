class ContinuousAllocation:
    def __init__(self, total_block):
        self.disk = [0] * total_block
        self.file = {}

    def allocate(self, name, size):
        for i in range(len(self.disk) - size + 1):
            if all(b == 0 for b in self.disk[i:i + size]):
                for j in range(i, i + size):
                    self.disk[j] = 1
                self.file[name] = (i, size)
                print(f"{name} allocated blocks {i} to {i + size - 1}")
                self.show_disk()
                return True
        print(f"Error: Not enough contiguous space for {name}.")
        self.show_disk()
        return False



    def deallocate(self, name):
        if name in self.file:
            start, size = self.file.pop(name)
            for i in range(start, start + size):
                self.disk[i] = 0
            print(f"{name} deallocated: blocks {start} to {start + size - 1}")
            self.show_disk()
            return True
        else:
            print("Error: File not found.")
            self.show_disk()
            return False

    def show_disk(self):
        print("Disk Status:", self.disk)
        print("--------------------------------------------------")


if __name__ == "__main__":
    contig = ContinuousAllocation(20)
    contig.allocate("FileA", 5)
    
    contig.deallocate("FileA")
