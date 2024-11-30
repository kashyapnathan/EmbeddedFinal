#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def analyze_queues():
    # Read the data
    client_data = pd.read_csv('client_req.csv')
    queue_data = pd.read_csv('queue_length.csv')
    client_queue = pd.read_csv('queue_length_client.csv')
    server_queue = pd.read_csv('queue_length_server.csv')

    # Create time-based plots using matplotlib instead of gnuplot
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

    # Plot 1: Response Time Components
    ax1.set_title('Response Time Components')
    ax1.plot(client_data.index,
             client_data['RT'], label='Total RT', color='blue', alpha=0.6)
    ax1.plot(queue_data.index, queue_data['queue_time'],
             label='Queue Time', color='red', alpha=0.6)
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Response Time (ms)')
    ax1.grid(True)
    ax1.legend()

    # Plot 2: Queue Lengths
    ax2.set_title('Queue Lengths Over Time')
    ax2.plot(queue_data.index,
             queue_data['queue_length'], label='Total Queue', color='purple')
    ax2.plot(client_queue.index,
             client_queue['queue_length'], label='Client Queue', color='green')
    ax2.plot(server_queue.index,
             server_queue['queue_length'], label='Server Queue', color='orange')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Queue Length')
    ax2.grid(True)
    ax2.legend()

    # Plot 3: Bottleneck Periods
    ax3.set_title('Bottleneck Detection')
    ax3.plot(queue_data.index, queue_data['is_bottleneck'], label='Bottleneck Periods',
             color='red', drawstyle='steps-post')
    ax3.set_xlabel('Time (seconds)')
    ax3.set_ylabel('Is Bottleneck')
    ax3.grid(True)
    ax3.legend()

    plt.tight_layout()
    plt.savefig('queue_analysis.pdf')
    plt.close()

    # Generate statistics
    stats = {
        'avg_queue_length': queue_data['queue_length'].mean(),
        'max_queue_length': queue_data['queue_length'].max(),
        'bottleneck_queue_length': queue_data[queue_data['is_bottleneck']]['queue_length'].mean(),
        'normal_queue_length': queue_data[~queue_data['is_bottleneck']]['queue_length'].mean(),
        'client_queue_avg': client_queue['queue_length'].mean(),
        'server_queue_avg': server_queue['queue_length'].mean()
    }

    # Save statistics
    with open('queue_analysis.txt', 'w') as f:
        f.write("Queue Analysis Results\n")
        f.write("=====================\n\n")
        f.write(f"Average Queue Length: {stats['avg_queue_length']:.2f}\n")
        f.write(f"Maximum Queue Length: {stats['max_queue_length']:.2f}\n")
        f.write(f"Average Queue Length during Bottlenecks: {
                stats['bottleneck_queue_length']:.2f}\n")
        f.write(f"Average Queue Length during Normal Operation: {
                stats['normal_queue_length']:.2f}\n")
        f.write(f"\nPer-Tier Statistics:\n")
        f.write(f"Client Tier Average Queue: {
                stats['client_queue_avg']:.2f}\n")
        f.write(f"Server Tier Average Queue: {
                stats['server_queue_avg']:.2f}\n")

    print("\nAnalysis complete! Generated files:")
    print("1. queue_analysis.pdf - Visual analysis of queues and bottlenecks")
    print("2. queue_analysis.txt - Statistical analysis of queue behavior")

    return stats


if __name__ == "__main__":
    stats = analyze_queues()

    print("\nKey Statistics:")
    print(f"Average Queue Length: {stats['avg_queue_length']:.2f}")
    print(f"Bottleneck Queue Length: {stats['bottleneck_queue_length']:.2f}")
    print(f"Normal Queue Length: {stats['normal_queue_length']:.2f}")
