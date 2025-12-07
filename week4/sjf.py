import pandas as pd

def sjf(processes, arrival, burst):
    n = len(processes)
    done = [False] * n
    completed = 0
    time = 0
    schedule = []

    while completed < n:
        idx = -1
        min_b = float('inf')

        # choose shortest job available at current time
        for i in range(n):
            if arrival[i] <= time and not done[i] and burst[i] < min_b:
                idx = i
                min_b = burst[i]

        if idx == -1:
            time += 1
            continue

        start = time
        finish = time + burst[idx]
        time = finish
        done[idx] = True
        completed += 1

        schedule.append((processes[idx], start, finish))

    return schedule


def compute_metrics(schedule, processes, arrival, burst):
    start_time = {}
    finish_time = {}

    for p, s, f in schedule:
        start_time[p] = s
        finish_time[p] = f

    rows = []

    for p, a, b in zip(processes, arrival, burst):
        s = start_time[p]
        f = finish_time[p]
        tat = f - a
        wait = tat - b

        rows.append([p, a, b, s, f, wait, tat])

    df = pd.DataFrame(rows, columns=["Process", "Arrival", "Burst", "Start", "Finish", "Waiting", "Turnaround"])
    return df


def print_text_gantt(schedule):
    print("\nTEXT BASED GANTT CHART:\n")
    line = ""
    for p, s, f in schedule:
        line += f"{s} | {p} | "
    line += str(schedule[-1][2])   # last finish
    print(line, "\n")


# ------------ INPUT ------------
processes = ["P1", "P2", "P3"]
arrival   = [0, 1, 2]
burst     = [7, 4, 1]

# run SJF
schedule = sjf(processes, arrival, burst)

# metrics
df = compute_metrics(schedule, processes, arrival, burst)

# print table
print("\nSJF TABLE:\n")
print(df.to_string(index=False))

# print averages
print("\nAverage Waiting Time:", df["Waiting"].mean())
print("Average Turnaround Time:", df["Turnaround"].mean())

# text gantt
print_text_gantt(schedule)
