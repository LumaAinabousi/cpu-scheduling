from tabulate import tabulate
import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, burst_time, priority=None):
        self.pid = pid
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time

def fcfs(processes):
    n = len(processes)
    wait_time = {}
    turnaround_time = {}

    processes.sort(key=lambda p: p.pid)

    wait_time[0] = 0
    for i in range(1, n):
        wait_time[i] = processes[i - 1].burst_time + wait_time[i - 1]

    for i in range(n):
        turnaround_time[i] = processes[i].burst_time + wait_time[i]

    tot_wait_time = sum(wait_time.values())
    tot_turnaround_time = sum(turnaround_time.values())

    avg_wait_time = tot_wait_time / n
    avg_turnaround_time = tot_turnaround_time / n

    return wait_time, turnaround_time, avg_wait_time, avg_turnaround_time

def srtf(processes):
    n = len(processes)
    wait_time = [0] * n
    turnaround_time = [0] * n
    curr_time = 0

    while True:
        remaining_burst_times = [process.remaining_time for process in processes if process.remaining_time > 0]
        if not remaining_burst_times:
            break

        min_remaining_time = min(remaining_burst_times)
        min_index = processes.index(next(process for process in processes if process.remaining_time == min_remaining_time))

        if processes[min_index].remaining_time > 1:
            curr_time += 1
            processes[min_index].remaining_time -= 1
        else:
            curr_time += processes[min_index].remaining_time
            processes[min_index].remaining_time = 0
            turnaround_time[min_index] = curr_time
            wait_time[min_index] = curr_time - processes[min_index].burst_time

    for i in range(n):
        turnaround_time[i] -= processes[i].burst_time

    avg_wait_time = sum(wait_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    return wait_time, turnaround_time, avg_wait_time, avg_turnaround_time

def round_robin(processes, quantum):
    n = len(processes)
    wait_time = [0] * n
    turnaround_time = [0] * n
    remaining_time = [process.burst_time for process in processes]
    curr_time = 0

    while True:
        done = True
        for i in range(n):
            if remaining_time[i] > 0:
                done = False
                if remaining_time[i] > quantum:
                    curr_time += quantum
                    remaining_time[i] -= quantum
                else:
                    curr_time += remaining_time[i]
                    wait_time[i] = curr_time - processes[i].burst_time
                    remaining_time[i] = 0
                    turnaround_time[i] = curr_time

        if done:
            break

    for i in range(n):
        turnaround_time[i] -= processes[i].burst_time

    avg_wait_time = sum(wait_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    return wait_time, turnaround_time, avg_wait_time, avg_turnaround_time


def priority_scheduling(processes):
    n = len(processes)
    wait_time = {}
    turnaround_time = {}

    processes.sort(key=lambda p: (p.priority if p.priority is not None else float('inf'), p.pid))

    wait_time[0] = 0
    for i in range(1, n):
        wait_time[i] = processes[i - 1].burst_time + wait_time[i - 1]

    for i in range(n):
        turnaround_time[i] = processes[i].burst_time + wait_time[i]

    tot_wait_time = sum(wait_time.values())
    tot_turnaround_time = sum(turnaround_time.values())

    avg_wait_time = tot_wait_time / n
    avg_turnaround_time = tot_turnaround_time / n

    return wait_time, turnaround_time, avg_wait_time, avg_turnaround_time

def display_processes_table(processes):
    headers = ["Process ID", "Burst Time", "Priority"]
    data = []

    for process in processes:
        pid = f"P{process.pid}"
        burst_time = process.burst_time
        priority = process.priority if process.priority is not None else "-"
        data.append([pid, burst_time, priority])

    print("Processes:")
    print(tabulate(data, headers=headers, tablefmt="grid"))
    print()

def display_turnaround_time_table(title, processes, fcfs_result, srtf_result, rr_result, ps_result):
    headers = ["Process ID", "FCFS", "SRTF", "RR", "PS"]
    data = []

    for i in range(len(processes)):
        pid = f"P{i}"
        fcfs_val = fcfs_result[1][i]
        srtf_val = srtf_result[1][i]
        rr_val = rr_result[1][i]
        ps_val = ps_result[1][i]
        data.append([pid, fcfs_val, srtf_val, rr_val, ps_val])

    avg_row = ["Avg. Turnaround Time (ms)", fcfs_result[3], srtf_result[3], rr_result[3], ps_result[3]]
    data.append(avg_row)

    print(title)
    print(tabulate(data, headers=headers, tablefmt="grid"))
    print()

def display_waiting_time_table(title, processes, fcfs_result, srtf_result, rr_result, ps_result):
    headers = ["Process ID", "FCFS", "SRTF", "RR", "PS"]
    data = []

    for i in range(len(processes)):
        pid = f"P{i}"
        fcfs_val = fcfs_result[0][i]
        srtf_val = srtf_result[0][i]
        rr_val = rr_result[0][i]
        ps_val = ps_result[0][i]
        data.append([pid, fcfs_val, srtf_val, rr_val, ps_val])

    avg_row = ["Avg. Waiting Time (ms)", fcfs_result[2], srtf_result[2], rr_result[2], ps_result[2]]
    data.append(avg_row)

    print(title)
    print(tabulate(data, headers=headers, tablefmt="grid"))
    print()

processes = [
    Process(0, 6, 3 ),
    Process(1, 18, 1),
    Process(2, 20, 2),
    Process(3, 23, 4)
]

quantum = 2

fcfs_result = fcfs(processes)
srtf_result = srtf(processes)
rr_result = round_robin(processes, quantum)
ps_result = priority_scheduling(processes)

display_processes_table(processes)
display_waiting_time_table("Waiting Time", processes, fcfs_result, srtf_result, rr_result, ps_result)
display_turnaround_time_table("Turnaround Time", processes, fcfs_result, srtf_result, rr_result, ps_result)


####################################

def plot_comparison_bar_chart(title, labels, fcfs_data, srtf_data, rr_data, ps_data, ylabel):
    x = range(len(labels))
    width = 0.00001

    plt.figure(figsize=(10, 6))

    plt.bar([i - width*1.5 for i in x], fcfs_data, width, label='FCFS', color='lightblue', edgecolor='black', linewidth=1, alpha=0.7)
    plt.bar([i - width/2 for i in x], srtf_data, width, label='SRTF', color='lightgreen', edgecolor='black', linewidth=1, alpha=0.7)
    plt.bar([i + width/2 for i in x], rr_data, width, label='RR', color='lightsalmon', edgecolor='black', linewidth=1, alpha=0.7)
    plt.bar([i + width*1.5 for i in x], ps_data, width, label='PS', color='lightcoral', edgecolor='black', linewidth=1, alpha=0.7)

    plt.xlabel('Algorithms', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    plt.xticks(x, labels, fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

#turnaround time comparison
turnaround_labels = ['Avg. Turnaround Time']
turnaround_fcfs = [fcfs_result[3]]
turnaround_srtf = [srtf_result[3]]
turnaround_rr = [rr_result[3]]
turnaround_ps = [ps_result[3]]

plot_comparison_bar_chart('Turnaround Time Comparison', turnaround_labels, turnaround_fcfs, turnaround_srtf, turnaround_rr, turnaround_ps, 'Time (ms)')

#waiting time comparison
waiting_labels = ['Avg. Waiting Time']
waiting_fcfs = [fcfs_result[2]]
waiting_srtf = [srtf_result[2]]
waiting_rr = [rr_result[2]]
waiting_ps = [ps_result[2]]

plot_comparison_bar_chart('Waiting Time Comparison', waiting_labels, waiting_fcfs, waiting_srtf, waiting_rr, waiting_ps, 'Time (ms)')

