#!/usr/bin/env python3
import os
import sys

def two_way():
    # Pipe 1: Parent writes -> Child reads
    r1, w1 = os.pipe()
    # Pipe 2: Child writes -> Parent reads
    r2, w2 = os.pipe()

    pid = os.fork()

    if pid > 0:
        # ---------------- Parent Process ----------------
        os.close(r1)   # Parent does NOT read from pipe1
        os.close(w2)   # Parent does NOT write to pipe2

        # Send message to child
        parent_msg = b"Hello From Parent !!\n"
        os.write(w1, parent_msg)
        os.close(w1)   # Finished writing

        # Read reply from child
        child_reply = os.read(r2, 1024)
        print("Parent Received:", child_reply.decode().strip())
        os.close(r2)

        os.wait()      # Wait for child to exit

    else:
        # ---------------- Child Process ----------------
        os.close(w1)   # Child does NOT write to pipe1
        os.close(r2)   # Child does NOT read pipe2

        # Read parent's message
        msg = os.read(r1, 1024)
        print("Child Received:", msg.decode().strip())
        os.close(r1)

        # Send reply to parent
        child_msg = b"Hello From Child !!\n"
        os.write(w2, child_msg)
        os.close(w2)

        sys.exit(0)


if __name__ == "__main__":
    two_way()
