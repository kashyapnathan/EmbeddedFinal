#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data_file = "merged_data.csv"
output_dir = "graphs"
df = pd.read_csv(data_file)

# Convert timestamp to seconds for better readability
df['timestamp'] = (df['timestamp'] - df['timestamp'].min()) / 1000

# Create output directory if not exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 1. Response Time Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df, x="response_time", hue="is_bottleneck_x",
             kde=True, palette="viridis", bins=50)
plt.title("Response Time Distribution")
plt.xlabel("Response Time (ms)")
plt.ylabel("Frequency")
plt.savefig(f"{output_dir}/response_time_distribution.png")
plt.close()

# 2. Queue Length and Queue Time Over Time
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['queue_length_x'],
         label='Queue Length (JMeter)', alpha=0.7)
plt.plot(df['timestamp'], df['queue_length_y'],
         label='Queue Length (Queue Data)', alpha=0.7)
plt.plot(df['timestamp'], df['queue_time'], label='Queue Time', alpha=0.7)
plt.title("Queue Length and Queue Time Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Metrics")
plt.legend()
plt.savefig(f"{output_dir}/queue_length_time.png")
plt.close()

# 3. CPU Utilization Over Time
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['cpu_utilization'],
         label='CPU Utilization', alpha=0.7)
plt.plot(df['timestamp'], df['CPU_User'], label='CPU User Time', alpha=0.7)
plt.plot(df['timestamp'], df['CPU_Idle'], label='CPU Idle Time', alpha=0.7)
plt.title("CPU Utilization Over Time")
plt.xlabel("Time (s)")
plt.ylabel("CPU Usage (%)")
plt.legend()
plt.savefig(f"{output_dir}/cpu_utilization_time.png")
plt.close()

# 4. Memory Usage Over Time
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['memory_usage'],
         label='Memory Usage', alpha=0.7, color='purple')
plt.title("Memory Usage Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Memory Usage (MB)")
plt.legend()
plt.savefig(f"{output_dir}/memory_usage_time.png")
plt.close()

# 5. Bottleneck Frequency Over Time
plt.figure(figsize=(12, 6))
bottleneck_counts = df[['timestamp', 'is_bottleneck_x', 'is_bottleneck_y']].melt(
    'timestamp', value_name='is_bottleneck')
sns.histplot(data=bottleneck_counts[bottleneck_counts['is_bottleneck']],
             x='timestamp', hue='variable', bins=50, multiple="stack", palette="coolwarm")
plt.title("Bottleneck Frequency Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Frequency")
plt.savefig(f"{output_dir}/bottleneck_frequency.png")
plt.close()

# 6. CPU Metrics by Core
plt.figure(figsize=(12, 6))
available_cores = [col for col in df.columns if col.startswith(
    "CPU") and col.endswith("_Total")]
for core in available_cores:
    plt.plot(df['timestamp'], df[core], label=f'{core}', alpha=0.7)
plt.title("CPU Metrics by Core")
plt.xlabel("Time (s)")
plt.ylabel("CPU Usage (%)")
plt.legend()
plt.savefig(f"{output_dir}/cpu_metrics_by_core.png")
plt.close()

# 7. Network Throughput
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['KBIn'], label='KB In', alpha=0.7)
plt.plot(df['timestamp'], df['KBOut'], label='KB Out', alpha=0.7)
plt.plot(df['timestamp'], df['KBIn_Rate'], label='KB In Rate', alpha=0.7)
plt.plot(df['timestamp'], df['KBOut_Rate'], label='KB Out Rate', alpha=0.7)
plt.title("Network Throughput")
plt.xlabel("Time (s)")
plt.ylabel("Network Traffic (KB/s)")
plt.legend()
plt.savefig(f"{output_dir}/network_throughput.png")
plt.close()

# 8. Correlation Between Queue Length and Response Time
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="queue_length_y", y="response_time",
                hue="is_bottleneck_x", palette="viridis", alpha=0.7)
plt.title("Correlation Between Queue Length and Response Time")
plt.xlabel("Queue Length")
plt.ylabel("Response Time (ms)")
plt.savefig(f"{output_dir}/correlation_queue_response_time.png")
plt.close()


# 9. Bottleneck Impact on Resource Utilization
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="is_bottleneck_x", y="cpu_utilization",
            palette="viridis", hue="is_bottleneck_x", dodge=False)
plt.title("CPU Utilization During Bottleneck vs. Non-Bottleneck")
plt.xlabel("Is Bottleneck")
plt.ylabel("CPU Utilization (%)")
plt.legend([], [], frameon=False)  # Remove redundant legend
plt.savefig(f"{output_dir}/bottleneck_impact_cpu.png")
plt.close()

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="is_bottleneck_x", y="memory_usage",
            palette="coolwarm", hue="is_bottleneck_x", dodge=False)
plt.title("Memory Usage During Bottleneck vs. Non-Bottleneck")
plt.xlabel("Is Bottleneck")
plt.ylabel("Memory Usage (MB)")
plt.legend([], [], frameon=False)  # Remove redundant legend
plt.savefig(f"{output_dir}/bottleneck_impact_memory.png")
plt.close()

# 10. Time Series Heatmap of CPU Metrics
cpu_heatmap_data = df[available_cores + ['timestamp']].set_index('timestamp')
plt.figure(figsize=(12, 6))
sns.heatmap(cpu_heatmap_data.T, cmap="coolwarm",
            cbar_kws={'label': 'CPU Usage (%)'})
plt.title("Time Series Heatmap of CPU Metrics")
plt.xlabel("Time (s)")
plt.ylabel("CPU Core")
plt.savefig(f"{output_dir}/cpu_heatmap.png")
plt.close()

# 11. Combined View of Response Time, Queue Length, and CPU Utilization
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Response Time (ms)", color="tab:blue")
ax1.plot(df['timestamp'], df['response_time'],
         label='Response Time', color="tab:blue", alpha=0.7)
ax1.tick_params(axis='y', labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.set_ylabel("Queue Length", color="tab:green")
ax2.plot(df['timestamp'], df['queue_length_y'],
         label='Queue Length', color="tab:green", alpha=0.7)
ax2.tick_params(axis='y', labelcolor="tab:green")

fig.tight_layout()
plt.title("Combined View of Response Time, Queue Length, and CPU Utilization")
plt.savefig(f"{output_dir}/combined_view.png")
plt.close()
