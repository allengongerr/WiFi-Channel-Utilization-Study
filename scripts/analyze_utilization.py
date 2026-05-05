import pyshark
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse
import sys
import os

def analyze_pcap(file_path, window_size=5.0):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    buckets = defaultdict(float)
    print(f"Opening {file_path}... Analyzing in {window_size}s windows.")
    
    # We use a display filter for 'wlan' to focus only on Wi-Fi frames
    cap = pyshark.FileCapture(file_path, keep_packets=False, display_filter='wlan')

    first_ts = None
    try:
        for packet in cap:
            try:
                curr_ts = float(packet.sniff_timestamp)
                if first_ts is None:
                    first_ts = curr_ts
                
                rel_ts = curr_ts - first_ts
                bucket_index = int(rel_ts // window_size) * window_size
                
                duration = float(packet.wlan.duration) / 1000000
                buckets[bucket_index] += duration
            except AttributeError:
                continue
    except pyshark.capture.capture.TSharkCrashException:
        print("Note: Reached end of file (encountered a truncated packet). Processing data collected so far...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        try:
            cap.close()
        except:
            pass # Ignore errors during closing if TShark already exited

    if not buckets:
        print("No valid Wi-Fi packets found in the capture.")
        return

    # Prep data for the graph
    times = sorted(buckets.keys())
    utilization_pcts = [(buckets[t] / window_size) * 100 for t in times]

    # Generate the Chart
    plt.figure(figsize=(10, 5))
    plt.plot(times, utilization_pcts, marker='o', color='#1f77b4', linewidth=2)
    plt.fill_between(times, utilization_pcts, color='#1f77b4', alpha=0.2)
    plt.title(f'Channel Utilization Fluctuations: {os.path.basename(file_path)}')
    plt.xlabel('Seconds Since Start of Capture')
    plt.ylabel('Airtime Utilization (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.ylim(0, max(utilization_pcts + [15]) + 10)
    
    output_dir = "docs/figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Clean up the filename so it saves nicely as a PNG
    base_name = os.path.basename(file_path).replace(".pcap", ".png").replace(".wcap", ".png")
    save_path = os.path.join(output_dir, base_name)
    
    plt.savefig(save_path)
    print(f"\n✅ Graph saved automatically to: {save_path}")
    
    # Display the graph for the live demo
    print("Graph generated. Close the window to finish.")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Wi-Fi Channel Utilization Fluctuations from a PCAP.")
    parser.add_argument("pcap_file", help="The path to the .pcap file you want to analyze.")
    parser.add_argument("--window", type=float, default=5.0, help="Time window size in seconds (default: 5.0)")
    
    args = parser.parse_args()
    analyze_pcap(args.pcap_file, args.window)