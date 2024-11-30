#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def analyze_milli_bottlenecks(input_file, output_dir):
    """
    Comprehensive analysis of milli-bottlenecks including:
    - Response time patterns
    - Bottleneck propagation
    - Queue length analysis
    - Impact assessment
    """
    print(f"\nReading data from: {input_file}")
    print(f"Saving results to: {output_dir}")

    # Load the data
    client_data = pd.read_csv(input_file)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Identify bottleneck periods
    rt_threshold = client_data['RT'].quantile(
        0.95)  # 95th percentile as threshold
    client_data['is_bottleneck'] = client_data['RT'] > rt_threshold

    # Analyze bottleneck characteristics
    bottleneck_analysis = {
        'total_requests': len(client_data),
        'bottleneck_requests': client_data['is_bottleneck'].sum(),
        'bottleneck_percentage': client_data['is_bottleneck'].mean() * 100,
        'avg_normal_rt': client_data.loc[~client_data['is_bottleneck'], 'RT'].mean(),
        'avg_bottleneck_rt': client_data.loc[client_data['is_bottleneck'], 'RT'].mean(),
        'bottleneck_threshold': rt_threshold,
    }

    # Generate visualizations

    # Response Time Distribution
    plt.figure(figsize=(10, 6))
    client_data['RT'].plot(kind='hist', bins=50,
                           alpha=0.7, label='Response Time')
    plt.axvline(rt_threshold, color='r', linestyle='--',
                label='95th Percentile Threshold')
    plt.title('Response Time Distribution')
    plt.xlabel('Response Time (ms)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    rt_distribution_path = os.path.join(output_dir, 'rt_distribution.pdf')
    plt.savefig(rt_distribution_path)
    plt.close()

    # Bottleneck Timeline
    client_data['timestamp'] = pd.to_datetime(
        client_data['starttime'], unit='ms')
    request_rate = client_data.set_index('timestamp').resample('1S').size()
    bottleneck_rate = client_data.loc[client_data['is_bottleneck']].set_index(
        'timestamp').resample('1S').size()

    plt.figure(figsize=(12, 6))
    plt.plot(request_rate.index, request_rate.values, label='Total Requests')
    plt.plot(bottleneck_rate.index, bottleneck_rate.values,
             label='Bottleneck Requests', color='red')
    plt.title('Request Rate and Bottlenecks Over Time')
    plt.xlabel('Time')
    plt.ylabel('Requests per Second')
    plt.legend()
    plt.grid(True)
    bottleneck_timeline_path = os.path.join(
        output_dir, 'bottleneck_timeline.pdf')
    plt.savefig(bottleneck_timeline_path)
    plt.close()

    # Save bottleneck summary
    summary_path = os.path.join(output_dir, 'summary.txt')
    with open(summary_path, 'w') as f:
        f.write("Milli-Bottleneck Analysis Summary\n")
        f.write("=" * 40 + "\n\n")
        for key, value in bottleneck_analysis.items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")

        # Additional analysis for bottleneck durations
        bottleneck_durations = []
        current_duration = 0
        for is_bottleneck in client_data['is_bottleneck']:
            if is_bottleneck:
                current_duration += 1
            elif current_duration > 0:
                bottleneck_durations.append(current_duration)
                current_duration = 0

        if bottleneck_durations:
            f.write("\nBottleneck Duration Analysis:\n")
            f.write(f"Average Bottleneck Duration: {
                    np.mean(bottleneck_durations):.2f} requests\n")
            f.write(f"Maximum Bottleneck Duration: {
                    max(bottleneck_durations)} requests\n")
            f.write(f"Number of Bottleneck Events: {
                    len(bottleneck_durations)}\n")

    print(f"\nAnalysis completed! Results saved in '{output_dir}' directory:")
    print(f"1. {rt_distribution_path} - Response time distribution visualization")
    print(f"2. {bottleneck_timeline_path} - Timeline of bottleneck events")
    print(f"3. {summary_path} - Detailed analysis results")

    return bottleneck_analysis


if __name__ == "__main__":
    # Input and output paths
    input_file = 'client_req.csv'  # Assuming the input file is in the root folder
    output_dir = 'graphs'

    analyze_milli_bottlenecks(input_file, output_dir)
