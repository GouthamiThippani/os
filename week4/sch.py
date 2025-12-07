import pandas as pd

# --------------------------
# Input
processes = ['P1','P2','P3','P4']
burst_time = [10, 5, 8, 6]
arrival_time = [0, 1, 2, 3]
time_quantum = 4  # For Round Robin
priority = [2, 1, 3, 2]  # Lower number => higher priority (for Priority Scheduling)

# --------------------------
# 1. FCFS Scheduling
def fcfs(processes, burst_time, arrival_time):
    n = len(processes)
    start_time = [0]*n
    completion_time = [0]*n
    waiting_time = [0]*n
    turnaround_time = [0]*n

    start_time[0] = arrival_time[0]
    completion_time[0] = start_time[0] + burst_time[0]
    turnaround_time[0] = completion_time[0] - arrival_time[0]
    waiting_time[0] = turnaround_time[0] - burst_time[0]

    for i in range(1, n):
        start_time[i] = max(completion_time[i-1], arrival_time[i])
        completion_time[i] = start_time[i] + burst_time[i]
        turnaround_time[i] = completion_time[i] - arrival_time[i]
        waiting_time[i] = turnaround_time[i] - burst_time[i]

    gantt = [(processes[i], start_time[i], completion_time[i]) for i in range(n)]

    df = pd.DataFrame({
        'Process': processes,
        'Arrival': arrival_time,
        'Burst': burst_time,
        'Start': start_time,
        'Completion': completion_time,
        'Waiting': waiting_time,
        'Turnaround': turnaround_time
    })

    avg_wt = sum(waiting_time)/n
    avg_tat = sum(turnaround_time)/n

    return df, gantt, avg_wt, avg_tat

# --------------------------
# 2. SJF Scheduling (Non-preemptive)
def sjf(processes, burst_time, arrival_time):
    n = len(processes)
    remaining = list(range(n))
    time = 0
    start_time = [0]*n
    completion_time = [0]*n
    waiting_time = [0]*n
    turnaround_time = [0]*n

    while remaining:
        arrived = [i for i in remaining if arrival_time[i] <= time]
        if not arrived:
            time += 1
            continue
        idx = min(arrived, key=lambda x: burst_time[x])
        start_time[idx] = time
        time += burst_time[idx]
        completion_time[idx] = time
        turnaround_time[idx] = completion_time[idx] - arrival_time[idx]
        waiting_time[idx] = turnaround_time[idx] - burst_time[idx]
        remaining.remove(idx)

    gantt = [(processes[i], start_time[i], completion_time[i]) for i in range(len(processes))]

    df = pd.DataFrame({
        'Process': processes,
        'Arrival': arrival_time,
        'Burst': burst_time,
        'Start': start_time,
        'Completion': completion_time,
        'Waiting': waiting_time,
        'Turnaround': turnaround_time
    })

    avg_wt = sum(waiting_time)/n
    avg_tat = sum(turnaround_time)/n
    return df, gantt, avg_wt, avg_tat

# --------------------------
# 3. Round Robin Scheduling
def round_robin(processes, burst_time, arrival_time, tq):
    n = len(processes)
    rem_bt = burst_time.copy()
    t = 0
    gantt = []
    waiting_time = [0]*n
    turnaround_time = [0]*n

    done = False
    # Simple RR that ignores arrival times ordering (keeps original order)
    while not done:
        done = True
        for i in range(n):
            if rem_bt[i] > 0:
                done = False
                start = t
                if rem_bt[i] > tq:
                    t += tq
                    rem_bt[i] -= tq
                    gantt.append((processes[i], start, t))
                else:
                    t += rem_bt[i]
                    gantt.append((processes[i], start, t))
                    waiting_time[i] = t - burst_time[i]
                    rem_bt[i] = 0

    for i in range(n):
        turnaround_time[i] = burst_time[i] + waiting_time[i]

    df = pd.DataFrame({
        'Process': processes,
        'Burst': burst_time,
        'Waiting': waiting_time,
        'Turnaround': turnaround_time
    })

    avg_wt = sum(waiting_time)/n
    avg_tat = sum(turnaround_time)/n
    return df, gantt, avg_wt, avg_tat

# --------------------------
# 4. Priority Scheduling (Non-preemptive)
def priority_scheduling(processes, burst_time, arrival_time, priority):
    n = len(processes)
    remaining = list(range(n))
    time = 0
    start_time = [0]*n
    completion_time = [0]*n
    waiting_time = [0]*n
    turnaround_time = [0]*n

    while remaining:
        arrived = [i for i in remaining if arrival_time[i] <= time]
        if not arrived:
            time += 1
            continue
        # pick by priority (lower number => higher priority). Tie-breaker: earlier arrival then lower index
        idx = min(arrived, key=lambda x: (priority[x], arrival_time[x], x))
        start_time[idx] = time
        time += burst_time[idx]
        completion_time[idx] = time
        turnaround_time[idx] = completion_time[idx] - arrival_time[idx]
        waiting_time[idx] = turnaround_time[idx] - burst_time[idx]
        remaining.remove(idx)

    gantt = [(processes[i], start_time[i], completion_time[i]) for i in range(n)]

    df = pd.DataFrame({
        'Process': processes,
        'Arrival': arrival_time,
        'Burst': burst_time,
        'Priority': priority,
        'Start': start_time,
        'Completion': completion_time,
        'Waiting': waiting_time,
        'Turnaround': turnaround_time
    })

    avg_wt = sum(waiting_time)/n
    avg_tat = sum(turnaround_time)/n
    return df, gantt, avg_wt, avg_tat

# --------------------------
# Run Algorithms
fcfs_table, fcfs_gantt, fcfs_wt, fcfs_tat = fcfs(processes, burst_time, arrival_time)
sjf_table, sjf_gantt, sjf_wt, sjf_tat = sjf(processes, burst_time, arrival_time)
rr_table, rr_gantt, rr_wt, rr_tat = round_robin(processes, burst_time, arrival_time, time_quantum)
pr_table, pr_gantt, pr_wt, pr_tat = priority_scheduling(processes, burst_time, arrival_time, priority)

# --------------------------
# Print Tables and plain-text Gantt (no plots)
print("\n--- FCFS Table ---")
print(fcfs_table.to_string(index=False))
print("\nFCFS Gantt (process, start, end):")
print(fcfs_gantt)

print("\n--- SJF Table ---")
print(sjf_table.to_string(index=False))
print("\nSJF Gantt (process, start, end):")
print(sjf_gantt)

print("\n--- Round Robin Table ---")
print(rr_table.to_string(index=False))
print("\nRound Robin Gantt (sequence of executions):")
print(rr_gantt)

print("\n--- Priority Scheduling Table ---")
print(pr_table.to_string(index=False))
print("\nPriority Scheduling Gantt (process, start, end):")
print(pr_gantt)

# --------------------------
# Comparison Table
comparison = pd.DataFrame({
    'Algorithm': ['FCFS','SJF','Round Robin', 'Priority (Non-preemptive)'],
    'Average Waiting Time': [fcfs_wt, sjf_wt, rr_wt, pr_wt],
    'Average Turnaround Time': [fcfs_tat, sjf_tat, rr_tat, pr_tat]
})
print("\n--- Comparison Table ---")
print(comparison.to_string(index=False))
