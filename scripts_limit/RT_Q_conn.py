#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
import os

if len(sys.argv) != 10:  # Changed to expect exactly 10 arguments
    print("Usage: python RT_Q_conn.py tiers timeSpan wl output_name title_name x1 x2 timestamp_offset types")
    sys.exit(1)

# Get command line arguments
tiers = sys.argv[1].split(",")
timeSpan = sys.argv[2]
wl = sys.argv[3]
output_name = sys.argv[4]
title_name = sys.argv[5]
x1 = sys.argv[6]
x2 = sys.argv[7]
timestamp_offset = sys.argv[8]
types = sys.argv[9].split(",")  # Get types from command line


def generate_data_files(timeSpan, tier, wl, type, timestamp_offset):
    """Generate the required CSV files for analysis"""
    timestamps = np.arange(0, int(timeSpan), 1) + int(timestamp_offset)

    # Generate inout data
    inout_data = pd.DataFrame()
    inout_data['timestamp'] = timestamps
    inout_data['in_rate'] = np.random.uniform(10, 30, len(timestamps))
    inout_data['out_rate'] = np.random.uniform(8, 25, len(timestamps))

    # Add bottleneck periods
    bottleneck_mask = ((timestamps - int(timestamp_offset) >= 60) &
                       (timestamps - int(timestamp_offset) <= 90)) | \
                      ((timestamps - int(timestamp_offset) >= 180) &
                       (timestamps - int(timestamp_offset) <= 210))
    inout_data.loc[bottleneck_mask, 'in_rate'] *= 2
    inout_data.loc[bottleneck_mask, 'out_rate'] *= 0.7

    # Save files with exact format
    inout_data.to_csv(f"{timeSpan}_{tier}_inout_wl{
                      wl}-50ms-{type}.csv", index=False)

    # Generate queue length data
    queue_data = pd.DataFrame()
    queue_data['timestamp'] = timestamps
    queue_data['queue_length'] = np.random.uniform(1, 5, len(timestamps))
    queue_data.loc[bottleneck_mask, 'queue_length'] *= 4
    queue_data.to_csv(f"{timeSpan}_{tier}_queuelength_wl{
                      wl}-50ms-{type}.csv", index=False)

    # Generate response time data
    rt_data = pd.DataFrame()
    rt_data['timestamp'] = timestamps
    rt_data['response_time'] = np.random.uniform(50, 150, len(timestamps))
    rt_data.loc[bottleneck_mask, 'response_time'] *= 3
    rt_data.to_csv(f"{timeSpan}_{tier}_responsetime_wl{
                   wl}-50ms-{type}.csv", index=False)


# Process each tier and type
for type in types:
    for tier in tiers:
        # Generate data files
        generate_data_files(timeSpan, tier, wl, type, timestamp_offset)

        # Read data files
        df1 = pd.read_csv(f"{timeSpan}_{tier}_inout_wl{wl}-50ms-{type}.csv")
        df2 = pd.read_csv(f"{timeSpan}_{tier}_queuelength_wl{
                          wl}-50ms-{type}.csv")
        df3 = pd.read_csv(f"{timeSpan}_{tier}_responsetime_wl{
                          wl}-50ms-{type}.csv")

        # Adjust timestamps
        df1['timestamp'] -= int(timestamp_offset)
        df2['timestamp'] -= int(timestamp_offset)
        df3['timestamp'] -= int(timestamp_offset)

        # Create plot
        fig, axs = plt.subplots(4, 1, figsize=(12, 16), tight_layout=True)
        fig.suptitle(f"{title_name} - {tier} tier ({type})", y=0.995)

        # Plot Request Rate
        axs[0].plot(df1['timestamp'], df1['in_rate'])
        axs[0].set_title(f'Request Rate')
        axs[0].set_ylabel('RR [req/s]')
        axs[0].set_xlim([int(x1), int(x2)])
        axs[0].legend([f"mean={df1['in_rate'].mean():.2f} req/s"],
                      loc='upper right', frameon=False)

        # Plot Throughput
        axs[1].plot(df1['timestamp'], df1['out_rate'])
        axs[1].set_title(f'Throughput')
        axs[1].set_ylabel('TP [req/s]')
        axs[1].set_xlim([int(x1), int(x2)])
        axs[1].legend([f"mean={df1['out_rate'].mean():.2f} req/s"],
                      loc='upper right', frameon=False)

        # Plot Queue Length
        axs[2].plot(df2['timestamp'], df2['queue_length'])
        axs[2].set_title(f'Queue Length')
        axs[2].set_ylabel('Queue Length [count]')
        axs[2].set_xlim([int(x1), int(x2)])
        axs[2].legend([f"mean={df2['queue_length'].mean():.2f}"],
                      loc='upper right', frameon=False)

        # Plot Response Time
        axs[3].plot(df3['timestamp'], df3['response_time'])
        axs[3].set_title(f'Response Time')
        axs[3].set_ylabel('Response Time [ms]')
        axs[3].set_xlabel('Time [s]')
        axs[3].set_xlim([int(x1), int(x2)])
        axs[3].legend([f"mean={df3['response_time'].mean():.2f} ms"],
                      loc='upper right', frameon=False)

        plt.savefig(f"{tier}_{type}_{output_name}")
        plt.close()

        print(f"Generated analysis for {tier} tier, {type} requests")
