import pandas as pd

def sjf_preemptive(processes, arrival, burst):
    n = len(processes)
    remaining = burst[:]  # copy
    complete = 0
    time = 0
    schedule = []
    curr = None
    start_time = None

    while complete < n:
        idx = -1
        min_r = float('inf')

        # find shortest remaining among arrived
        for i in range(n):
            if arrival[i] <= time and remaining[i] > 0 and remaining[i] < min_r:
                idx = i
                min_r = remaining[i]

        if idx == -1:
            # CPU idle until next arrival (if any)
            # find next arrival time > time
            future_times = [a for a in arrival if a > time]
            if not future_times:
                break
            time = min(future_times)
            continue

        # context switch (process change)
        if curr != idx:
            if curr is not None and start_time is not None:
                schedule.append((processes[curr], start_time, time))
            curr = idx
            start_time = time

        # execute 1 unit
        remaining[idx] -= 1
        time += 1

        # if finished, record completion segment
        if remaining[idx] == 0:
            schedule.append((processes[idx], start_time, time))
            complete += 1
            curr = None
            start_time = None

    return schedule

def compute_metrics_from_schedule(schedule, processes, arrival, burst):
    # compute first start time and completion (last finish) per process
    first_start = {p: None for p in processes}
    completion = {p: 0 for p in processes}

    for p, s, e in schedule:
        if first_start[p] is None:
            first_start[p] = s
        completion[p] = max(completion[p], e)

    rows = []
    total_wait = 0
    total_tat = 0
    n = len(processes)

    for p, a, b in zip(processes, arrival, burst):
        s = first_start[p] if first_start[p] is not None else None
        comp = completion[p]
        tat = comp - a
        wait = tat - b
        rows.append([p, a, b, s, comp, wait, tat])
        total_wait += wait
        total_tat += tat

    df = pd.DataFrame(rows, columns=["Process", "Arrival", "Burst", "Start", "Completion", "Waiting", "Turnaround"])
    avg_wait = total_wait / n
    avg_tat = total_tat / n
    return df, avg_wait, avg_tat

def print_text_gantt(schedule):
    if not schedule:
        print("No schedule.")
        return
    out = ""
    for p, s, e in schedule:
        out += f"{s} | {p} | "
    out += str(schedule[-1][2])
    print("\nTEXT-BASED GANTT:\n")
    print(out, "\n")


# --------- example ----------
if __name__ == "__main__":
    processes = ["P1", "P2", "P3"]
    arrival   = [0, 1, 2]
    burst     = [7, 4, 1]

    schedule = sjf_preemptive(processes, arrival, burst)

    # metrics table using pandas
    df, avg_wait, avg_tat = compute_metrics_from_schedule(schedule, processes, arrival, burst)

    print("\nSJF (Preemptive) TABLE:\n")
    print(df.to_string(index=False))

    print(f"\nAverage Waiting Time: {avg_wait:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

    # text gantt
    print_text_gantt(schedule)
