#!/usr/bin/env python3
from datetime import datetime
import sys
import csv
import os
import numpy as np

pwd = os.getcwd()


def create_detail_rt():
    input_file = os.path.join(pwd, "client_req.csv")
    output_file = os.path.join(pwd, "detailRT-client_wlindex.html.csv")

    with open(input_file, 'r') as f, open(output_file, 'w', newline='') as w:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(
            w, fieldnames=['starttime', 'endtime', 'reqType', 'RT'])
        writer.writeheader()

        data = list(reader)  # Read all data first
        if data:
            # Get timestamp range from the data
            start_times = [int(float(row['starttime'])) for row in data]
            min_time = min(start_times)
            max_time = max(start_times)

            print(f"Data timestamp range: {datetime.fromtimestamp(
                min_time/1000)} to {datetime.fromtimestamp(max_time/1000)}")

            # Write all data
            for row in data:
                writer.writerow(row)

    print(f"Created detailed RT file: {output_file}")
    return output_file, min_time, max_time


# Create the detailed RT file and get timestamp range
detail_rt_file, runtime_start, runtime_end = create_detail_rt()

output = os.path.join(pwd, "RT_client_dist.csv")
print(f"Reading from: {detail_rt_file}")
print(f"Writing to: {output}")

response = []
with open(detail_rt_file) as f, open(output, "w", newline='') as w:
    reader = csv.DictReader(f)
    for row in reader:
        starttime = int(float(row['starttime']))
        if runtime_start <= starttime <= runtime_end:
            response.append(float(row['RT']))

    if not response:
        print("No responses found in the specified time range!")
        sys.exit(1)

    print(f"Analyzing {len(response)} responses")

    fieldnames = ['Percentile', 'RT']
    writer = csv.DictWriter(w, fieldnames=fieldnames)
    writer.writeheader()

    res_arr = np.array(response)
    for i in range(0, 100):
        writer.writerow({
            'Percentile': i,
            'RT': np.percentile(res_arr, i)
        })

    # Add final percentile
    writer.writerow({
        'Percentile': 100,
        'RT': np.percentile(res_arr, 99.995)
    })

    # Print some basic statistics
    print("\nResponse Time Statistics:")
    print(f"Min RT: {np.min(res_arr):.2f}ms")
    print(f"Max RT: {np.max(res_arr):.2f}ms")
    print(f"Mean RT: {np.mean(res_arr):.2f}ms")
    print(f"Median RT: {np.median(res_arr):.2f}ms")
    print(f"95th percentile: {np.percentile(res_arr, 95):.2f}ms")
    print(f"99th percentile: {np.percentile(res_arr, 99):.2f}ms")

print("\nResponse time distribution analysis completed")
