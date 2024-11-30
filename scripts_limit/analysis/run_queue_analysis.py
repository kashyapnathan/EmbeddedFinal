#!/usr/bin/env python3
import subprocess
import os
import time


def run_queue_analysis():
    # Get current timestamp
    current_time = int(time.time())

    # Parameters
    timespan = "300"  # 5 minutes
    workload = "main"
    tiers = "client,server"
    types = "get,post"

    # 1. Extract queue length
    print("Extracting queue length...")
    cmd1 = f"python scripts_limit/extract_queue_length.py {
        timespan} {workload} {tiers} {types}"
    subprocess.run(cmd1.split())

    # 2. Run RT queue connection analysis
    print("\nAnalyzing RT queue connections...")
    output_name = "queue_analysis.pdf"
    title_name = "Queue Analysis"
    cmd2 = f"python scripts_limit/RT_Q_conn.py {tiers} {timespan} {workload} {output_name} \"{
        title_name}\" 0 {timespan} {current_time} collectl_cpu_host0.txt,collectl_cpu_host1.txt"
    subprocess.run(cmd2.split())

    # 3. Generate queue component plots
    print("\nGenerating queue component visualizations...")
    with open('scripts_limit/RT_Q_components.gnuplot', 'w') as f:
        f.write('''
set terminal pdfcairo size 10in,6in
set output 'RT_queue_components.pdf'

# Plot styling
set style data linespoints
set grid

# Multiple plot layout
set multiplot layout 2,1 title "Response Time and Queue Analysis"

# Plot 1: Response Time Components
set title "Response Time Components"
set xlabel "Time (s)"
set ylabel "Response Time (ms)"
plot 'client_req.csv' using ($1/1000):4 title 'Total RT' with lines, \
     'queue_length.csv' using 1:2 title 'Queue Time' with lines

# Plot 2: Queue Length
set title "Queue Length Over Time"
set xlabel "Time (s)"
set ylabel "Queue Length"
plot 'queue_length.csv' using 1:3 title 'Queue Length' with lines

unset multiplot
''')

    subprocess.run(['gnuplot', 'scripts_limit/RT_Q_components.gnuplot'])

    print("\nAnalysis complete! Generated files:")
    print("1. queue_analysis.pdf - Queue connection analysis")
    print("2. RT_queue_components.pdf - Queue components visualization")
    print("3. queue_length.csv - Raw queue length data")


if __name__ == "__main__":
    run_queue_analysis()
