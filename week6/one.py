
import os

def main():
    # Create pipe
    r, w = os.pipe()
    pid = os.fork()

    if pid > 0:
        # Parent process
        os.close(r)
        message = b"Hello from parent through pipe!"
        os.write(w, message)
        os.close(w)
    else:
        # Child process
        os.close(w)
        rfd = os.fdopen(r)
        message = rfd.read()
        print("Child received:", message)
        rfd.close()

if __name__ == "__main__":
    main()
