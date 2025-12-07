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

def recovery_algo(n, r, alloc, max_need, avail, pid, req):
    need = [[max_need[i][j] - alloc[i][j] for j in range(r)] for i in range(n)]

    if any(req[j] > need[pid][j] for j in range(r)):
        print(f"Process P{pid} request {req} exceeds its maximum declared need {need[pid]}.")
        return False

    if any(req[j] > avail[j] for j in range(r)):
        print(f"Not enough available resources to satisfy P{pid}'s request {req}. Available: {avail}")
        return False

    for j in range(r):
        alloc[pid][j] += req[j]
        avail[j] -= req[j]

    print(f"Process P{pid} requests {req} -> Tentatively allocated. Checking safety...")

    safe, safe_seq = is_safe(n, r, alloc, max_need, avail)
    if safe:
        print("System is safe after allocation.")
        print("Safe sequence:", safe_seq)
        print("Request granted.")
        return True
    else:
        # Rollback
        for j in range(r):
            alloc[pid][j] -= req[j]
            avail[j] += req[j]
        print("Request denied: system would be unsafe. Rolled back tentative allocation.")
        return False


if __name__ == "__main__":
    # simple diagnostic so the script definitely prints something when run
    print(">>> banker.py running...")

    # Example dataset (same as your example)
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

    # Initial safety check
    safe, seq = is_safe(n, r, [row[:] for row in alloc], max_need, avail[:])
    if safe:
        print("Initial: System is safe.")
        print("Safe sequence:", seq)
    else:
        print("Initial: System is NOT safe.")

    print()

    # Process P1 requesting [1,2,2]
    pid = 1
    req = [1, 2, 2]
    recovery_algo(n, r, alloc, max_need, avail, pid, req)

    # After granting check (alloc and avail will reflect the final state if granted)
    print()
    print("Final alloc matrix:")
    for i, a in enumerate(alloc):
        print(f"P{i}: {a}")
    print("Final available:", avail)
