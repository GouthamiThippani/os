from collections import deque
import pandas as pd

def rr(processes, arrival, burst, quantum):
    # sort by arrival
    data = sorted(zip(processes, arrival, burst), key=lambda x: x[1])
    processes, arrival, burst = zip(*data)

    n = len(processes)
    remaining = list(burst)
    time = 0
    schedule = []
    q = deque()
    i = 0

    while True:
        # add newly arrived processes
        while i < n and arrival[i] <= time:
            q.append(i)
            i += 1

        if not q:
            if i < n:
                time = arrival[i]
                continue
            else:
                break

        idx = q.popleft()
        run = min(quantum, remaining[idx])

        start = time
        end = time + run
        schedule.append((processes[idx], start, end))

        remaining[idx] -= run
        time = end

        # add arrivals during execution
        while i < n and arrival[i] <= time:
            q.append(i)
            i += 1

        # re-queue if not finished
        if remaining[idx] > 0:
            q.append(idx)

        # stop if all done
        if all(r == 0 for r in remaining):
            break

    return schedule, list(processes), list(arrival), list(burst)


def compute_rr_metrics(schedule, processes, arrival, burst):
    # completion = last finish time of each process
    completion = {p: 0 for p in processes}
    for p, s, e in schedule:
        completion[p] = max(completion[p], e)

    rows = []
    for p, a, b in zip(processes, arrival, burst):
        comp = completion[p]
        tat = comp - a
        wait = tat - b
        rows.append({
            "Process": p,
            "Arrival": a,
            "Burst": b,
            "Completion": comp,
            "Waiting": wait,
            "Turnaround": tat
        })

    return pd.DataFrame(rows)


def print_text_gantt(schedule):
    print("\nTEXT-BASED GANTT CHART:\n")

    out = ""
    for p, s, e in schedule:
        out += f"{s} | {p} | "
    out += f"{schedule[-1][2]}"   # final finish time

    print(out)
    print()


# ---------------- EXAMPLE ----------------
processes = ["P1", "P2", "P3"]
arrival   = [0, 1, 2]
burst     = [5, 3, 8]
quantum   = 2

schedule, procs, arr, bur = rr(processes, arrival, burst, quantum)

# create metrics table
df = compute_rr_metrics(schedule, procs, arr, bur)

print("\nRR TABLE:\n")
print(df.to_string(index=False))

# averages
print("\nAverage Waiting Time:", df["Waiting"].mean())
print("Average Turnaround Time:", df["Turnaround"].mean())

# text gantt
print_text_gantt(schedule)
