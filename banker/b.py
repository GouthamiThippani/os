def is_safe(n, r, alloc, max_need, avail):
    need = [[max_need[i][j] - alloc[i][j] for j in range(r)] for i in range(n)]
    work = avail.copy()
    finish = [False] * n
    safe_seq = []
    while len(safe_seq) < n:
        progress = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(r)):
                for j in range(r):
                    work[j] += alloc[i][j]
                finish[i] = True
                safe_seq.append(i)
                progress = True
        if not progress:
            break
    if len(safe_seq) == n:
        return True, safe_seq
    else:
        return False, None


if __name__ == "__main__":
    print(">>> banker.py running (safety-only version)...")

    # Example dataset
    n, r = 5, 3
    alloc = [[0, 1, 0],
             [2, 0, 0],
             [3, 0, 2],
             [2, 1, 1],
             [0, 0, 2]]
    max_need = [[7, 5, 3],
                [3, 2, 2],
                [9, 0, 2],
                [2, 2, 2],
                [4, 3, 3]]
    avail = [3, 3, 2]

    # Safety check only
    safe, seq = is_safe(n, r, [row[:] for row in alloc], max_need, avail[:])
    if safe:
        print("Initial: System is SAFE.")
        print("Safe sequence:", seq)
    else:
        print("Initial: System is NOT safe.")
