# Project: The 2.4 GHz Congestion Paradox

### Application Scenario
In high-density environments like the Johns Hopkins campus, the 2.4 GHz spectrum is notoriously crowded. We built a custom analysis engine that interfaces with a MacBook Pro (M1 Pro) in monitor mode to visualize real-time airtime utilization. This tool allows researchers to move beyond simple signal-strength bars and see the actual "duty cycle" of the frequency.

### What We Built
We developed a Python-based processing pipeline that aggregates raw 802.11 frames into 5-second windows. By summing the `wlan.duration` field—the literal microseconds reserved by the hardware for each transmission—we provide a high-fidelity look at channel occupancy and protocol overhead.

### Why It’s Useful
Standard tools often struggle to capture the efficiency of modern standards like 802.11ax (Wi-Fi 6). Our tool highlights the **Utilization Paradox**: high-density areas often show lower airtime utilization due to high-efficiency packets, even while suffering from extreme packet contention and "hidden node" interference.

### Highlight of Results
Our measurements revealed that the **Brody Atrium (Library)** maintained a lower average airtime utilization (~4.09%) than a **Sparse Outdoor Area** (~20.99%). This proves that legacy data rates and long-range beacons outdoors actually "choke" the channel more than high-speed modern infrastructure does.

![Protocol Proof: RadioTap Header and Monitor Mode Verification](docs/figures/apartment.png)