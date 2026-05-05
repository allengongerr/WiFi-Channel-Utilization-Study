# Wi-Fi Channel Utilization Study

## i. Introduction

This project investigates the channel utilization of the 2.4 GHz band across diverse environments. Using passive sniffing on a MacBook Pro (M1 Pro), we analyze how protocol overhead (beacons) and contention control (RTS/CTS) impact the availability of the medium for IoT devices.

## ii. Hardware Details

- **Host Machine**: MacBook Pro 14" (M1 Pro Chip)
- **Wireless Card**: Internal Apple Silicon Wi-Fi interface (`en0`)
- **Band**: 2.4 GHz (Locked to Channel 11)

## iii. Software Environment

- **Language**: Python 3.9+
- **Dependencies**: `pyshark`, `matplotlib`
- **Sniffing Tool**: macOS Native Wireless Diagnostics (Sniffer Tool)
- **Analysis Engine**: TShark (Wireshark)

## iv. Reproducibility Guide

### 1. Hardware Setup (Monitor Mode)

1. Hold `Option` (⌥) and click the Wi-Fi icon in the macOS menu bar.
2. Select **Open Wireless Diagnostics...**
3. Go to the top menu bar and select `Window > Sniffer`.
4. Select **Channel 11** and **20MHz** width.
5. Click **Start**. The Wi-Fi icon will change to a "small eye" symbol, confirming the card is in Monitor Mode.
6. When finished, click **Stop**. The file is saved to `/var/tmp/`.

### 2. Environment Setup

Install the necessary command-line tools and Python libraries:

```bash
brew install wireshark
python3 -m pip install pyshark matplotlib
```

### 3. Running the Analysis

To generate utilization graphs and calculate airtime metrics, run the script with the path to your `.pcap` file:

```bash
python3 scripts/analyze_utilization.py data/your_capture.pcap
```

> **Note:** The script automatically saves the resulting fluctuation graphs as PNG files to `docs/figures/`.

## v. Key Results & Metrics

| Location  | Avg Utilization | State            | Key Driver                                           |
| --------- | --------------- | ---------------- | ---------------------------------------------------- |
| Library   | 4.09%           | Efficient/Noisy  | High-speed Wi-Fi 6 with high collision (2,695 retries) |
| Outdoors  | 20.99%          | Active           | Legacy data rates and long-range beacons             |
| Apartment | 16.42%          | Moderate         | Balanced residential IoT and streaming mix           |

## vi. Troubleshooting

- **TShark Crash (Retcode 14)**: Occurs if a capture is stopped mid-packet. The script includes a `TSharkCrashException` handler to process all valid data before the crash.
- **Command not found (pip)**: Use `python3 -m pip install` to target the correct Python environment on macOS.
- **Empty Graphs**: Ensure your sniffer was locked to the correct channel (Channel 11). Sniffing an idle channel will result in 0% utilization.
