#!/usr/bin/env python3

import json
import argparse
from tdigest import TDigest
from typing import Dict

def print_banner(filename: str = 'banner.txt') -> None:
    """Prints the banner from the provided file."""
    try:
        with open(filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("Banner file not found.")

def print_help() -> None:
    """Displays help information about the tool."""
    print("""
Hashmeter Analysis Tool

This tool analyzes hashmeter data to provide key performance and stability metrics useful for SecDevOps engineers.

Key Features:
- Performance Profiling: Understand the efficiency of cryptographic operations.
- Stability Analysis: Assess the consistency of execution times to identify potential timing attacks or performance bottlenecks.
- Sample Size Adequacy: Ensure statistical significance of performance data.
- Outlier Detection: Detect unusual or suspicious activities that may indicate security threats.
- Timing Consistency: Gain immediate insight into the reliability of operations over time.

Usage:
- Run the script without arguments to analyze the default 'data/hashmeter.json' file.
- Use the '-f' or '--file' option to specify an alternative data file.
- Use the '--help' flag to display this help message.
""")

def analyze_hashmeter_data(filename: str = 'data/hashmeter.json') -> Dict[str, float]:
    """Analyzes hashmeter data and returns key statistics."""
    with open(filename, 'r') as file:
        data = json.load(file)
        centroids = data.get('centroids', [])
        if not centroids:
            raise ValueError("No centroids data found in the file.")

    td = TDigest()
    td.update_centroids_from_list(centroids)

    total_runs = int(td.n)
    if total_runs == 0:
        raise ValueError("No measurements found in the data.")

    min_time = td.percentile(0)
    max_time = td.percentile(100)
    median_time = td.percentile(50)
    iqr = td.percentile(75) - td.percentile(25)
    timing_range = max_time - min_time
    p90 = td.percentile(90)
    p10 = td.percentile(10)
    estimated_std = (p90 - p10) / 2.56
    stability_ratio = iqr / median_time
    outlier_ratio = (max_time - td.percentile(99)) / iqr

    print_banner()

    print(f"""
Hashmeter Analysis:
==================
Total Measurements: {total_runs}

Basic Statistics:
-----------------
Minimum Time: {min_time:.2f}μs
Maximum Time: {max_time:.2f}μs
Median Time: {median_time:.2f}μs
IQR: {iqr:.2f}μs

Stability Metrics:
------------------
Timing Range: {timing_range:.2f}μs
Estimated Std Dev: {estimated_std:.2f}μs
Stability Ratio (IQR/Median): {stability_ratio:.3f}
Outlier Impact Ratio: {outlier_ratio:.3f}

Timing Consistency: {"Stable" if stability_ratio < 0.5 else "Variable"}
Outlier Presence: {"High" if outlier_ratio > 2 else "Normal"}
Sample Size Adequacy: {"Good" if total_runs > 1000 else "Need more samples"}

Key Percentiles:
----------------
25th Percentile: {td.percentile(25):.2f}μs
75th Percentile: {td.percentile(75):.2f}μs
95th Percentile: {td.percentile(95):.2f}μs
99th Percentile: {td.percentile(99):.2f}μs
""")

    return {
        'total_runs': total_runs,
        'min_time': min_time,
        'max_time': max_time,
        'median_time': median_time,
        'iqr': iqr,
        'stability_ratio': stability_ratio,
        'outlier_ratio': outlier_ratio
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-f', '--file', type=str, default='data/hashmeter.json', help='Path to the hashmeter data file.')
    parser.add_argument('--help', action='store_true', help='Show help information.')
    args = parser.parse_args()

    if args.help:
        print_help()
    else:
        analyze_hashmeter_data(args.file)
