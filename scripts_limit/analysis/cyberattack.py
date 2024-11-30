#!/usr/bin/env python3
import requests
import time
import random
import argparse
import csv
import os


def send_requests(url, request_type, rate, duration, output_file):
    """
    Send requests to a target URL to simulate different traffic patterns and save results to a CSV file.

    Args:
    - url: Target URL (e.g., http://localhost:8080).
    - request_type: Type of traffic ('normal', 'milli_bottleneck_attack', 'resource_exhaustion', 'synchronized_attack').
    - rate: Number of requests per second.
    - duration: Total duration of the attack in seconds.
    - output_file: Path to the output CSV file.
    """
    end_time = time.time() + duration
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'request_type',
                      'response_code', 'response_time', 'error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        while time.time() < end_time:
            try:
                response_time = None
                if request_type == 'normal':
                    response_time = random.gauss(50, 10) / 1000  # Mean 50ms
                elif request_type == 'milli_bottleneck_attack':
                    response_time = random.gauss(800, 150) / 1000  # Mean 800ms
                elif request_type == 'resource_exhaustion':
                    response_time = random.expovariate(
                        1 / 300) / 1000  # Exponential
                elif request_type == 'synchronized_attack':
                    response_time = random.gamma(
                        4, 100) / 1000  # Gamma distribution

                if response_time:
                    time.sleep(response_time)  # Simulate traffic delay

                # Send HTTP request
                start = time.time()
                response = requests.get(url)
                elapsed_time = (time.time() - start) * 1000  # Convert to ms
                writer.writerow({
                    'timestamp': int(time.time() * 1000),
                    'request_type': request_type,
                    'response_code': response.status_code,
                    'response_time': round(elapsed_time, 2),
                    'error': ''
                })
                print(
                    f"Request Type: {request_type}, Response Code: {response.status_code}, Response Time: {round(elapsed_time, 2)} ms")

            except Exception as e:
                writer.writerow({
                    'timestamp': int(time.time() * 1000),
                    'request_type': request_type,
                    'response_code': '',
                    'response_time': '',
                    'error': str(e)
                })
                print(f"Error: {e}")

            time.sleep(1 / rate)


def simulate_attacks(url, duration, output_file):
    """
    Simulate different attack scenarios in sequence and save results to a CSV file.

    Args:
    - url: Target URL (e.g., http://localhost:8080).
    - duration: Total duration for each scenario in seconds.
    - output_file: Path to the output CSV file.
    """
    attack_scenarios = [
        ('normal', 10),
        ('milli_bottleneck_attack', 50),
        ('resource_exhaustion', 30),
        ('synchronized_attack', 20)
    ]

    # Write header to the CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'request_type',
                      'response_code', 'response_time', 'error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for scenario, rate in attack_scenarios:
        print(
            f"Simulating {scenario} at {rate} requests/second for {duration} seconds...")
        send_requests(url, scenario, rate, duration, output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Simulate cyberattacks on port 8080.")
    parser.add_argument('--url', type=str, default='http://localhost:8080',
                        help='Target URL (default: http://localhost:8080)')
    parser.add_argument('--duration', type=int, default=60,
                        help='Duration of each attack scenario in seconds (default: 60)')
    parser.add_argument('--output', type=str, default='attack_simulation.csv',
                        help='Output CSV file (default: attack_simulation.csv)')
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Starting simulation on {args.url}...")
    simulate_attacks(args.url, args.duration, args.output)
    print(f"Simulation completed. Results saved to {args.output}")


if __name__ == "__main__":
    main()
