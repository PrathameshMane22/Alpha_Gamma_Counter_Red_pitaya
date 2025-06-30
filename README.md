

# Alpha Gamma Counter on Red Pitaya
This repository contains the source code, HDL logic, and documentation for implementing an **Alpha-Gamma Coincidence Counter** on the **Red Pitaya** platform. The project is based on an enhanced version of Mario Vretenar’s Alpha-Gamma Counter, with additional features and improvements to the signal processing pipeline.

## 📌 Overview
The Alpha-Gamma Counter is designed to measure and correlate events detected by alpha and gamma detectors. It performs real-time coincidence detection, timestamping, amplitude measurement, and basic filtering. This implementation is tailored for the **Zynq 7010** FPGA on the Red Pitaya board, providing a compact and efficient data acquisition solution for nuclear physics experiments.

## ⚙️ Features
- Coincidence detection between alpha and gamma signals  
- Timestamping with nanosecond precision  
- Amplitude measurement with configurable thresholds  
- FIFO buffering of data samples  
- UART/UDP-based data transfer to host PC  
- Optional enhancements like:
     - Trapezoidal Filtering
     - Time Over Threshold (ToT) calculatiom

## 🧰 Project Structure
```markdown
Alpha_Gamma_Counter_Red_pitaya
├── server/                 # C++ source files for Red Pitaya user-space applications
├── client/                 # Python code for sending the data from RP to th PC
├── rtl/                    # Verilog/Vivado project files (PL logic)
├── xdc/                    # Master XDC file for Red pitaya
├── results/                # CSV file, Excel file and energy spectrum for reference
└── README.md               # Project documentation

````

---

## 🔧 Requirements

- **Red Pitaya** board (Zynq 7010)
- **Vivado Design Suite** (2021.1 or compatible)
- **GCC / G++** for C++ compilation on ARM
- **Python 3.x** for CSV analysis and plotting
- Optional: **MATLAB** or **GNU Octave** for signal visualization

---

## 🚀 Getting Started

1. **Clone the repository**  
   ```bash
   git clone https://github.com/PrathameshMane22/Alpha_Gamma_Counter_Red_pitaya.git
   cd Alpha_Gamma_Counter_Red_pitaya


2. **Build and deploy bitstream**

   * Open Vivado project under `hdl/`
   * Generate bitstream and export hardware
   * Deploy the `.bit` file to your Red Pitaya

3. **Compile user-space code**

   ```bash
   cd /Alpha_Gamma_Counter_Red_pitaya/server
   cmake .
   make
   ./agc_server    # Run the Alpha-Gamma counter server program
   ```

4. **Receive and log data**

   * Data is printed to terminal or sent over UDP
   * Use Python scripts (client_unified and csv_file) to log and analyze data
   * python client_unified.py "ip address of RP" "port" "name of csv file that you want to give"

---

## 📊 Sample Output

Each event is logged with:

* Event type (alpha/gamma/coincidence)
* Timestamp (in seconds)
* Amplitude (in V)

Example:

```
Alpha Detected: Time = 0.00001 s | Amplitude = 0.230 V
Gamma Detected: Time = 0.00002 s | Amplitude = 0.810 V
```

---

## 📊 Result section

* CSV file
* Converted excel file
* Energy spectrum generated from dat file using GNUplot

---

## 📈 Planned Improvements

* Add **trapezoidal filter** for digital pulse shaping
* Implement **Time Over Threshold (ToT)** logic
* Store data directly to SD card or DDR memory
* Improve GUI/CLI for configuration

---

## 🤝 Acknowledgements

* Based on original work by **Mario Vretenar**
* Developed as part of academic research using the Red Pitaya platform
* Special thanks to mentors and collaborators at \[TIFR and SPIT]

---

## 📄 License

This project is released under the MIT License. See `LICENSE` file for details.
