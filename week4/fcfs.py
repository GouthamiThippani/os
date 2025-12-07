import pandas as pd

def fcfs(processes, arrival, burst):
    data = sorted(zip(processes, arrival, burst), key=lambda x: x[1])
    time = 0
    schedule = []
    rows = []

    for p, a, b in data:
        if time < a:
            time = a

        start = time
        finish = time + b

        schedule.append((p, start, finish))

        rows.append({
            "Process": p,
            "Arrival": a,
            "Burst": b,
            "Start": start,
            "Finish": finish,
            "Waiting": start - a,
            "Turnaround": finish - a
        })

        time = finish

    df = pd.DataFrame(rows)
    return schedule, df


def print_text_gantt(schedule):
    print("\nTEXT GANTT CHART:\n")

    output = ""
    for p, start, end in schedule:
        output += f"{start} | {p} | "
    output += f"{schedule[-1][2]}"  # Final time

    print(output)
    print("\n")


# ---------------- INPUT -----------------
processes = ["P1", "P2", "P3"]
arrival   = [0, 2, 4]
burst     = [5, 3, 1]

schedule, df = fcfs(processes, arrival, burst)

# PRINT TABLE
print("\nFCFS TABLE:\n")
print(df.to_string(index=False))

# PRINT AVERAGES
avg_wait = df["Waiting"].mean()
avg_tat  = df["Turnaround"].mean()

print("\nAverage Waiting Time:", avg_wait)
print("Average Turnaround Time:", avg_tat)

# PRINT TEXT GANTT
print_text_gantt(schedule)
