#!/usr/bin/env python3
import sys
import re
import time
import csv
import subprocess
import math
import os
import numpy as np
import datetime

# Get current working directory properly
pwd = os.getcwd()

# Look for client log file
client_file = subprocess.getstatusoutput("ls | grep 'client-requests.log'")

if client_file[0] != 0:
    print("No client log files found!")
    sys.exit(1)

hfile = os.path.join(pwd, "client-requests.log")
output = os.path.join(pwd, "client_req.csv")

print(f"Reading from: {hfile}")
print(f"Writing to: {output}")

try:
    with open(hfile) as f, open(output, "w", newline='') as w:
        fieldnames = ['starttime', 'endtime', 'reqType', 'RT']
        writer = csv.DictWriter(w, fieldnames=fieldnames)
        writer.writeheader()

        for line in f:
            parts = line.strip().split(' | ')
            if len(parts) < 4:
                continue

            timestamp = parts[0].split(',')
            if len(timestamp) < 2:
                continue

            try:
                # Convert timestamp to milliseconds
                base_time = int(time.mktime(time.strptime(
                    timestamp[0], "%Y-%m-%d %H:%M:%S")))
                starttime = (base_time - 21600) * 1000 + int(timestamp[1])

                reqMethod = parts[1]
                reqName = parts[2]
                response = int(float(parts[3]))
                endtime = starttime + response

                # Determine request type
                reqType = reqName
                if reqMethod == 'POST':
                    reqType += "_add-item"
                elif reqMethod == 'DELETE':
                    reqType += "_delete-item"

                writer.writerow({
                    'starttime': starttime,
                    'endtime': endtime,
                    'reqType': reqType,
                    'RT': response
                })

            except (ValueError, IndexError) as e:
                print(f"Skipping malformed line: {line.strip()}")
                continue

except FileNotFoundError:
    print(f"Could not find input file: {hfile}")
    sys.exit(1)
except Exception as e:
    print(f"Error processing file: {str(e)}")
    sys.exit(1)

print(f"Successfully processed client requests to {output}")
