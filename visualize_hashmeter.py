import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tdigest import TDigest
import probscale  # Corrected import

def import_tdigest(filename: str) -> TDigest:
    """Imports TDigest data from a JSON file (same as before)."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            centroids = data.get('centroids')
            if centroids is None:
                raise ValueError("The JSON file must contain a 'centroids' key.")
            td = TDigest()
            td.update_centroids_from_list(centroids)
            return td
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {filename}")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

def visualize_tdigest(td: TDigest,
                      xlabel: str = "Time (μs)",
                      ylabel: str = "Cumulative Probability",
                      log_scale: bool = False):
    """
    Visualizes the TDigest data with a Tufte-inspired style.
    """

    # --- Data Preparation ---
    percentiles = np.linspace(0, 100, 101)
    values = [td.percentile(p) for p in percentiles]
    probabilities = percentiles / 100.0

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(10, 5))

    # Use probscale for the y-axis
    ax.set_yscale('prob')
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

    # Plot the data (log or linear scale)
    if log_scale:
        ax.semilogx(values, probabilities, '-', color='steelblue', lw=2)
    else:
        ax.plot(values, probabilities, '-', color='steelblue', lw=2)

    # --- Ensure 0th percentile is visible ---
    min_val = td.percentile(0)
    # If min_val is very small or 0, set a tiny positive floor so log scale won't break
    if min_val <= 0:
        min_val = 1e-3
    ax.set_xlim(left=min_val * 0.9)

    # --- Key Percentiles (Markers and Annotations) ---
    key_percentiles = [25, 50, 75, 95, 99.99]
    key_values = [td.percentile(p) for p in key_percentiles]
    key_probabilities = [p / 100.0 for p in key_percentiles]

    # Markers
    ax.scatter(key_values, key_probabilities, color='firebrick', s=30, zorder=5)

    # Annotations
    for p in key_percentiles:
        val = td.percentile(p)
        prob = p / 100.0
        ax.annotate(f'{p}th: {val:.0f}μs',
                    (val, prob),
                    xytext=(15, 5),
                    textcoords='offset points',
                    fontsize=8,
                    color='dimgray',
                    ha='left',
                    va='bottom',
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="lightgray", lw=0.5))

    # --- Tufte-Inspired Styling ---
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('gray')
    ax.spines['bottom'].set_color('gray')
    ax.tick_params(axis='x', colors='dimgray', labelsize=9)
    ax.tick_params(axis='y', colors='dimgray', labelsize=9)
    ax.set_xlabel(xlabel, color='black', fontsize=10)
    ax.set_ylabel(ylabel, color='black', fontsize=10)
    ax.grid(True, which='both', ls='-', color='lightgray', lw=0.5)

    # --- Caption and Title ---
    fig.suptitle("HashTimer Performance", fontsize=14, fontweight='bold', x=0.125, ha='left')
    fig.text(0.125, 0.90, "Cumulative distribution of PBKDF2 hash times.  Log scale.", 
             fontsize=10, color='dimgray', ha='left')
    fig.text(0.125, 0.86, "By kha1n3vol3", fontsize=9, fontstyle='italic', color='gray', ha='left')

    # --- Final Adjustments ---
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    try:
        td = import_tdigest('./data/hashmeter.json')
        # visualize_tdigest(td) # Linear
        visualize_tdigest(td, log_scale=True)  # Log scale
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
