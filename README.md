

# Alpha Gamma Counter on Red Pitaya
This repository contains the source code, HDL logic, and documentation for implementing an **Alpha-Gamma Coincidence Counter** on the **Red Pitaya** platform. The project is based on an enhanced version of Mario Vretenar’s Alpha-Gamma Counter, with additional features and improvements to the signal processing pipeline. This system aims to deliver a low-cost, portable, and open-source alternative to expensive DAQ systems like Pixie-16.


## Overview
The Alpha-Gamma Counter is designed to measure and correlate events detected by alpha and gamma detectors. It performs real-time coincidence detection, timestamping, amplitude measurement, and basic filtering. This implementation is tailored for the **Zynq 7010** FPGA on the Red Pitaya board, providing a compact and efficient data acquisition solution for nuclear physics experiments.

## Features
- Coincidence detection between alpha and gamma signals  
- Timestamping with nanosecond precision  
- Amplitude measurement with configurable thresholds  
- FIFO buffering of data samples  
- UART/UDP-based data transfer to host PC  
- Optional enhancements like:
     - Trapezoidal Filtering
     - Time Over Threshold (ToT) calculatiom

## Project Structure
```markdown
Alpha_Gamma_Counter_Red_pitaya
├── server/                 # C++ source files for Red Pitaya user-space applications
├── client/                 # Python code for sending the data from RP to th PC
├── rtl/                    # Verilog/Vivado project files (PL logic)
├── xdc/                    # Master XDC file for Red pitaya
├── results/                # CSV file, Excel file and energy spectrum for reference
└── README.md               # Project documentation

````

## Requirements

- **Red Pitaya** board (Zynq 7010)
- **Vivado Design Suite** (2021.1 or compatible)
- **GCC / G++** for C++ compilation on ARM
- **Python 3.x** for CSV analysis and plotting
- Optional: **MATLAB** or **GNU Octave** for signal visualization


## Setup Instructions

### Hardware Setup

1. **Power**: 5V via micro-USB (≥2A recommended)
2. **Ethernet**: Direct to PC or via router (DHCP-enabled)
3. **Inputs**: Connect detectors via BNC-to-SMA adapters to IN1/IN2

### Software Setup

- Download Red Pitaya OS: [Red Pitaya OS Images](https://redpitaya.readthedocs.io/en/latest/quickStart/SDcard/SDcard.html#os-versions)
- Flash with Balena Etcher or Rufus
- Access via SSH:  
  ```bash
  ssh root@169.254.250.211
  # Password: root
  ```

## FPGA Build & Deployment

### Step 1: HDL Setup in Vivado

```tcl
cd path/to/v0.94/ip
source systemZ10.tcl   # Setup base project
```

- Copy Verilog files from `rtl/` to the Vivado project directory
- Modify `agc_counter.v` as needed
- Generate `.bit` file

### Step 2: Boot Files

```bash
echo all:{ system_wrapper.bit } > system_wrapper.bif
bootgen -image system_wrapper.bif -arch zynq -process_bitstream bin -o system_wrapper.bit.bin -w
```

- Export hardware to get `.xsa`
- Use `.xsa` in **Vitis** to create FSBL ELF file
- Copy files to SD card under `FPGA/z10_125/v0.94/`:
  - `fpga.bit`
  - `fpga.bif`
  - `fpga.bit.bin`
  - `fsbl.elf`

## Running the System

### Server-Side (on Red Pitaya)

```bash
scp -r server/ root@169.254.250.211:/root
ssh root@169.254.250.211
cd /root/server
cmake .
make
./agc_server
```

### Client-Side (on PC)

```bash
python client_unified.py 169.254.250.211 1234 mydata.csv
```

- Logs data to CSV in real-time
- Data format:  
  ```
  Alpha Detected: Time = 0.00001 s | Amplitude = 0.230 V
  Gamma Detected: Time = 0.00002 s | Amplitude = 0.810 V
  ```

## Results & Visualization

### 1. `.dat` Files (binary format)

Transfer files:
```bash
scp root@169.254.250.211:/root/server/measurements/* /path/to/local/
```

Plot using GNUplot:
```gnuplot
plot "alpha.dat" binary format='%uint32' using ($0):1 with lines
plot "gamma.dat" binary format='%uint32' using ($0):1 with lines
```

### 2. `.csv` Files

Process with script:
```bash
python csv_file.py   # Make sure file path is updated in script
```

Generates:
- Cleaned CSV
- Optional Excel-compatible version

## Sample Output

Each event is logged with:

* Event type (alpha/gamma/coincidence)
* Timestamp (in seconds)
* Amplitude (in V)

Example:

```
Alpha Detected: Time = 0.00001 s | Amplitude = 0.230 V
Gamma Detected: Time = 0.00002 s | Amplitude = 0.810 V
```

## Result section in repository

* CSV file
* Converted excel file
* Energy spectrum generated from dat file using GNUplot


## Planned Improvements

* Add **trapezoidal filter** for digital pulse shaping
* Implement **Time Over Threshold (ToT)** logic
* Store data directly to SD card or DDR memory
* Improve GUI/CLI for configuration

## Acknowledgements

* Based on original work by **Mario Vretenar**
* Developed as part of academic research using the Red Pitaya platform
* Special thanks to mentors and collaborators at \[TIFR and SPIT]

## License

This project is released under the MIT License. See `LICENSE` file for details.
