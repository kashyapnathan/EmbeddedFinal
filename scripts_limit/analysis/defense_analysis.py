#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys


def load_attack_data(csv_file):
    """
    Load attack simulation data from a CSV file.

    Args:
    - csv_file: Path to the CSV file.

    Returns:
    - A pandas DataFrame containing the attack data.
    """
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded data from {csv_file}.")
        return df
    except Exception as e:
        print(f"Error loading data from {csv_file}: {e}")
        sys.exit(1)


def plot_defense_analysis(data, output_file):
    """
    Create visualizations for defense mechanism analysis.

    Args:
    - data: A pandas DataFrame containing attack simulation data.
    - output_file: Path to save the output PDF file.
    """
    defense_types = data['defense_type'].unique()

    # Create main figure
    fig = plt.figure(figsize=(15, 25))
    plt.suptitle('Defense Mechanism Analysis', fontsize=16, y=0.95)

    # 1. Time series plot
    ax1 = plt.subplot(311)
    for defense in defense_types:
        df_defense = data[data['defense_type'] == defense]
        ax1.plot(df_defense['timestamp'], df_defense['response_time'],
                 label=f"{defense} ({df_defense['description'].iloc[0]})", alpha=0.7)

    ax1.set_title('Response Time Over Time (Including Attack Periods)')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Response Time (ms)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # 2. Effectiveness comparison by defense type
    ax2 = plt.subplot(312)
    effectiveness_data = data.groupby('defense_type')['effectiveness'].mean()
    bars = ax2.bar(effectiveness_data.index,
                   effectiveness_data.values, color='skyblue')
    ax2.set_title('Effectiveness by Defense Type')
    ax2.set_ylabel('Effectiveness (%)')
    ax2.grid(True, alpha=0.3)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height:.2f}', ha='center', va='bottom')

    # 3. Response time distribution by period
    ax3 = plt.subplot(313)
    periods = data['period'].unique()
    for period in periods:
        df_period = data[data['period'] == period]
        ax3.hist(df_period['response_time'], bins=50, alpha=0.5, label=period)

    ax3.set_title('Response Time Distribution by Period')
    ax3.set_xlabel('Response Time (ms)')
    ax3.set_ylabel('Frequency')
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Save plot
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Saved visualizations to {output_file}.")


if __name__ == "__main__":
    csv_file = "graphs/defense_mechanisms_data.csv"
    output_file = "graphs/defense_analysis.pdf"

    # Load data from CSV
    data = load_attack_data(csv_file)

    # Create visualizations
    plot_defense_analysis(data, output_file)
