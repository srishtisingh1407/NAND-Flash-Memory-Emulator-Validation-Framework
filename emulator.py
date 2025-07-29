import random
import os
import json
import matplotlib.pyplot as plt
import csv

# Constants
BLOCKS = 4
PAGES_PER_BLOCK = 8
PAGE_SIZE = 256  # in bytes
FAILURE_RATE = 0.3  # 30% chance of write failure (for testing)
  # 1% chance of write failure

# Memory Structure: NAND is a list of blocks, each block is a list of pages
nand_memory = [[[0xFF] * PAGE_SIZE for _ in range(PAGES_PER_BLOCK)] for _ in range(BLOCKS)]

def write(block, page, data):
    if block >= BLOCKS or page >= PAGES_PER_BLOCK:
        return "Invalid address"
    if random.random() < FAILURE_RATE:
        return f"WRITE FAIL at B{block}P{page}"
    data_bytes = list(data.encode('utf-8'))[:PAGE_SIZE]
    nand_memory[block][page][:len(data_bytes)] = data_bytes
    return f"WRITE OK at B{block}P{page}"

def read(block, page):
    if block >= BLOCKS or page >= PAGES_PER_BLOCK:
        return "Invalid address"
    page_data = bytes(nand_memory[block][page]).decode('utf-8', errors='ignore')
    return f"READ B{block}P{page}: {page_data.strip()}"

def erase(block):
    if block >= BLOCKS:
        return "Invalid block"
    for page in range(PAGES_PER_BLOCK):
        nand_memory[block][page] = [0xFF] * PAGE_SIZE
    return f"ERASE OK B{block}"

def simulate():
    stats = {'writes': 0, 'fails': 0}
    failures = []
    for i in range(100):
        blk = random.randint(0, BLOCKS-1)
        pg = random.randint(0, PAGES_PER_BLOCK-1)
        data = f"Data_{i}"
        result = write(blk, pg, data)
        print(result)
        stats['writes'] += 1
        if 'FAIL' in result:
            stats['fails'] += 1
        failures.append(stats['fails'])
    dppm = (stats['fails'] / stats['writes']) * 1_000_000
    yield_percent = (1 - stats['fails']/stats['writes']) * 100
    print(f"DPPM: {dppm:.2f}, Yield: {yield_percent:.2f}%")

    # Plotting the failure trend
    plt.plot(range(1, 101), failures, label='Cumulative Failures')
    plt.xlabel('Write Operations')
    plt.ylabel('Failures')
    plt.title('NAND Write Failure Trend')
    plt.grid(True)
    plt.legend()
    plt.savefig("failure_trend.png")
    plt.show()

def write_from_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            stats = {'writes': 0, 'fails': 0}
            failures = []
            i = 0
            for row in reader:
                blk = i // PAGES_PER_BLOCK % BLOCKS
                pg = i % PAGES_PER_BLOCK
                msg = row.get('message', '')
                result = write(blk, pg, msg)
                print(result)
                stats['writes'] += 1
                if 'FAIL' in result:
                    stats['fails'] += 1
                failures.append(stats['fails'])
                i += 1
            dppm = (stats['fails'] / stats['writes']) * 1_000_000
            yield_percent = (1 - stats['fails']/stats['writes']) * 100
            print(f"DPPM: {dppm:.2f}, Yield: {yield_percent:.2f}%")

            # Plotting
            plt.plot(range(1, stats['writes']+1), failures, label='Cumulative Failures')
            plt.xlabel('CSV Write Ops')
            plt.ylabel('Failures')
            plt.title('CSV Write Failure Trend')
            plt.grid(True)
            plt.legend()
            plt.savefig("csv_failure_trend.png")
            plt.show()
    except FileNotFoundError:
        print("CSV file not found. Please check the path.")
    except Exception as e:
        print(f"Error: {e}")

def cli():
    print("Welcome to NAND Emulator CLI")
    while True:
        cmd = input("Enter command (read/write/erase/show/simulate/csvwrite/exit): ").strip().lower()
        if cmd == 'exit': break
        elif cmd == 'show':
            print(json.dumps(nand_memory, indent=1))
        elif cmd in ('read', 'write', 'erase'):
            b = int(input("Block: "))
            p = int(input("Page: ")) if cmd != 'erase' else 0
            if cmd == 'read':
                print(read(b, p))
            elif cmd == 'write':
                d = input("Data: ")
                print(write(b, p, d))
            else:
                print(erase(b))
        elif cmd == 'simulate':
            simulate()
        elif cmd == 'csvwrite':
            path = input("Enter CSV file path: ")
            write_from_csv(path)
        else:
            print("Invalid command")

if __name__ == '__main__':
    cli()
