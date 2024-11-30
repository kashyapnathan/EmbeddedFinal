#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def analyze_response_times(input_dir='.', output_dir='graphs', time_window=None):
    """
    Analyze response times and generate time-series visualizations.

    Args:
    - input_dir: Directory containing input files.
    - output_dir: Directory to save analysis results.
    - time_window: Time window size in seconds for aggregation. Auto-calculated if None.
    """
    try:
        # Read the data
        client_req_path = os.path.join(input_dir, 'client_req.csv')
        client_reqs = pd.read_csv(client_req_path)

        print(f"Successfully loaded data from '{client_req_path}'.")
        if client_reqs.empty:
            raise ValueError("The input dataset is empty.")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Convert timestamps to relative time
        client_reqs['relative_time'] = (
            client_reqs['starttime'] - client_reqs['starttime'].min()) / 1000

        # Adjust bin size dynamically if not provided
        if not time_window:
            time_window = max(1, int(client_reqs['relative_time'].max() / 100))
        bins = np.arange(
            0, client_reqs['relative_time'].max() + time_window, time_window)
        time_windows = pd.cut(client_reqs['relative_time'], bins=bins)

        # Group by time windows and calculate statistics
        time_stats = client_reqs.groupby(time_windows)['RT'].agg(
            mean='mean',
            std='std',
            count='count',
            p95=lambda x: np.percentile(x, 95),
            p99=lambda x: np.percentile(x, 99)
        ).reset_index()

        # Replace interval indices with midpoints
        time_stats['time_midpoint'] = time_stats['relative_time'].apply(
            lambda x: x.mid if pd.notna(x) else np.nan
        )

        # Determine bottleneck threshold
        bottleneck_threshold = client_reqs['RT'].quantile(0.95)
        client_reqs['is_bottleneck'] = client_reqs['RT'] > bottleneck_threshold

        # Bottleneck percentage over time
        bottleneck_stats = client_reqs.groupby(time_windows).agg(
            bottleneck_count=('is_bottleneck', 'sum'),
            total_count=('RT', 'size')
        ).reset_index()
        bottleneck_stats['time_midpoint'] = bottleneck_stats['relative_time'].apply(
            lambda x: x.mid if pd.notna(x) else np.nan
        )
        bottleneck_stats['bottleneck_percentage'] = (
            bottleneck_stats['bottleneck_count'] / bottleneck_stats['total_count']) * 100

        # Plot time-series analysis
        fig, axs = plt.subplots(3, 1, figsize=(12, 15), sharex=True)

        # 1. Response Times over time
        axs[0].plot(time_stats['time_midpoint'], time_stats['mean'],
                    'b-', label='Mean RT')
        axs[0].fill_between(time_stats['time_midpoint'],
                            time_stats['mean'] - time_stats['std'],
                            time_stats['mean'] + time_stats['std'],
                            alpha=0.2, label='Std Dev Range')
        axs[0].plot(time_stats['time_midpoint'], time_stats['p95'],
                    'g--', label='95th Percentile')
        axs[0].plot(time_stats['time_midpoint'], time_stats['p99'],
                    'r--', label='99th Percentile')
        axs[0].set_ylabel('Response Time (ms)')
        axs[0].set_title('Response Time Analysis')
        axs[0].grid(True)
        axs[0].legend()

        # 2. Request rate over time
        axs[1].plot(time_stats['time_midpoint'], time_stats['count'],
                    'g-', label='Requests/sec')
        axs[1].set_ylabel('Requests per Second')
        axs[1].set_title('Request Rate Over Time')
        axs[1].grid(True)
        axs[1].legend()

        # 3. Bottleneck percentage over time
        axs[2].plot(bottleneck_stats['time_midpoint'],
                    bottleneck_stats['bottleneck_percentage'], 'r-', label='Bottleneck %')
        axs[2].set_ylabel('Bottleneck Percentage (%)')
        axs[2].set_xlabel('Time (seconds)')
        axs[2].set_title('Bottleneck Percentage Over Time')
        axs[2].grid(True)
        axs[2].legend()

        plt.tight_layout()
        output_file = os.path.join(output_dir, 'time_series_analysis.pdf')
        plt.savefig(output_file)
        plt.close()

        print(f"Analysis complete. Time series visualization saved to '{
              output_file}'.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the input file exists.")
    except ValueError as e:
        print(f"Error: {e}. Please check the input dataset.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Default parameters for quick testing
    analyze_response_times(input_dir='.', output_dir='graphs')
