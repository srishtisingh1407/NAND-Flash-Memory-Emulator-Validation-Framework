#  NAND Flash Memory Emulator & Validation Framework

An end-to-end **Python simulation of NAND flash memory operations**, built for demonstrating validation workflows typically done in semiconductor product design engineering roles.

💻 **CLI-based and beginner-friendly**

---

## 🚀 Key Features

- 📦 Emulates NAND memory: **4 Blocks × 8 Pages each**
- ✍️ Supports **read, write, erase** operations
- ⚠️ Injects **random write failures** to simulate manufacturing defects
- 📈 Calculates **DPPM (Defective Parts Per Million)** and **Yield**
- 📊 Generates **failure trend graphs** using `matplotlib`
- 📁 Accepts **CSV input** for batch write simulation
- 💬 Runs via a simple, powerful **Command-Line Interface (CLI)**

---

## 📁 Project Structure

NAND-Flash-Emulator/
├── emulator.py # 🔧 Core NAND emulator logic
├── spicy_nand_data.csv # 🌶️ Sample test data file
├── failure_trend.png # 📉 Output from simulate mode
├── csv_failure_trend.png # 📊 Output from CSV write mode
├── README.md # 📘 This file!

---

## 🔄 How to Run

1. Clone or download this repo  
2. Run the emulator:

```bash
python emulator.py
Use the CLI options:

Command	Action
read	Read from a block/page
write	Manually write data
erase	Erase a specific block
simulate	Run 100 simulated writes and show failure trend
csvwrite	Write using data from CSV
show	Display full NAND memory
exit	Exit the emulator

🧪 Sample CSV File
This is what your spicy_nand_data.csv should look like:

csv
Copy
Edit
message
System check_0
Bootloader_0
NAND init_0
Page write_0
...
Voltage spike_9
I/O error_9
Pass check_9
Use this with csvwrite mode to simulate real-world data inputs.

📊 Sample Outputs
🔁 Simulate Mode
Plots a failure trend across 100 randomized writes:


📄 CSV Write Mode
Plots failures during batch write from CSV:



💻 Technologies Used
🐍 Python 3

📊 Matplotlib

📄 CSV File Handling

🎲 Random Module

🖥️ CLI Input/Output

🔠 Basic JSON pretty-printing
