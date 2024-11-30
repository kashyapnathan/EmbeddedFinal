#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys


def plot_security_histograms(input_file, output_file):
    """Visualize security patterns from the dataset."""
    df = pd.read_csv(input_file)

    request_types = df['request_type'].unique()
    titles = {
        'normal': 'Normal Traffic Pattern',
        'milli_bottleneck_attack': 'Milli-Bottleneck Attack Pattern',
        'resource_exhaustion': 'Resource Exhaustion Pattern',
        'synchronized_attack': 'Synchronized Attack Pattern',
        'with_countermeasures': 'Pattern with Countermeasures'
    }

    descriptions = {
        'normal': 'Baseline response time distribution\nMean: ~100ms, Low variance',
        'milli_bottleneck_attack': 'Short, intense spikes in response times\nPossible DoS attempt',
        'resource_exhaustion': 'Gradual degradation pattern\nSystem resource depletion',
        'synchronized_attack': 'Coordinated attack pattern\nMultiple simultaneous requests',
        'with_countermeasures': 'Protected system response\nReduced impact of attacks'
    }

    colors = {
        'normal': 'green',
        'milli_bottleneck_attack': 'red',
        'resource_exhaustion': 'orange',
        'synchronized_attack': 'purple',
        'with_countermeasures': 'blue'
    }

    fig, axs = plt.subplots(len(request_types), 1,
                            figsize=(12, 25), tight_layout=True)

    for i, req_type in enumerate(request_types):
        df_type = df[df['request_type'] == req_type]

        # Create histogram
        axs[i].hist(
            df_type['response_time'],
            bins=50,
            color=colors[req_type],
            alpha=0.7
        )

        # Add statistics
        mean_rt = df_type['response_time'].mean()
        median_rt = df_type['response_time'].median()
        p95_rt = df_type['response_time'].quantile(0.95)

        # Plot styling
        axs[i].set_title(f"{titles[req_type]}\n{descriptions[req_type]}",
                         fontsize=12, pad=20)
        axs[i].set_xlabel('Response Time (ms)', fontsize=10)
        axs[i].set_ylabel('Frequency', fontsize=10)
        axs[i].grid(True, alpha=0.3)

        # Add statistics box
        stats_text = f"Mean: {mean_rt:.1f}ms\nMedian: {
            median_rt:.1f}ms\n95th: {p95_rt:.1f}ms"
        axs[i].text(0.95, 0.95, stats_text,
                    transform=axs[i].transAxes,
                    verticalalignment='top',
                    horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.suptitle('Response Time Analysis: Security Patterns',
                 fontsize=14, y=0.995)
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Visualization saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python plot_security_patterns.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = os.path.join("graphs", sys.argv[2])

    plot_security_histograms(input_file, output_file)
