/*
    Alpha Gamma Counter
    Copyright (C) 2025 Prathamesh Mane
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#!/usr/bin/env python3
"""
Python TCP Client to receive streaming CSV data from Red Pitaya
Usage: python3 tcp_client.py <red_pitaya_ip> [port] [output_file]
"""

import socket
import sys
import signal
import time
from datetime import datetime

class TCPClient:
    def __init__(self, host, port=8888, output_file="unified_timestamps.csv"):
        self.host = host
        self.port = port
        self.output_file = output_file
        self.running = True
        self.sock = None
        self.file_handle = None
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        print(f"\nReceived signal {signum}, closing connection...")
        self.running = False
    
    def connect(self):
        """Connect to Red Pitaya"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connecting to Red Pitaya at {self.host}:{self.port}...")
            self.sock.connect((self.host, self.port))
            print("Connected successfully!")
            return True
        except Exception as e:
            print(f"ERROR: Could not connect to Red Pitaya: {e}")
            return False
    
    def open_file(self):
        """Open output file"""
        try:
            self.file_handle = open(self.output_file, 'w')
            print(f"Saving data to: {self.output_file}")
            return True
        except Exception as e:
            print(f"ERROR: Could not open output file: {e}")
            return False
    
    def receive_data(self):
        """Main data reception loop"""
        total_bytes = 0
        line_count = 0
        start_time = time.time()
        last_update = start_time
        
        print("Press Ctrl+C to stop and close connection")
        
        try:
            while self.running:
                # Receive data
                data = self.sock.recv(4096)
                
                if not data:
                    print("Connection closed by Red Pitaya")
                    break
                
                # Decode and write to file
                text_data = data.decode('utf-8', errors='ignore')
                self.file_handle.write(text_data)
                self.file_handle.flush()  # Ensure immediate write
                
                # Update statistics
                total_bytes += len(data)
                line_count += text_data.count('\n')
                
                # Print status update every second
                current_time = time.time()
                if current_time - last_update >= 1.0:
                    elapsed = current_time - start_time
                    rate = total_bytes / elapsed if elapsed > 0 else 0
                    print(f"\rReceived: {total_bytes:,} bytes, {line_count:,} lines, "
                          f"Rate: {rate/1024:.1f} KB/s, Time: {elapsed:.1f}s", end='', flush=True)
                    last_update = current_time
                    
        except Exception as e:
            print(f"\nERROR during data reception: {e}")
        
        # Final statistics
        elapsed = time.time() - start_time
        avg_rate = total_bytes / elapsed if elapsed > 0 else 0
        print(f"\nFinal stats: {total_bytes:,} bytes, {line_count:,} lines")
        print(f"Average rate: {avg_rate/1024:.1f} KB/s over {elapsed:.1f} seconds")
    
    def cleanup(self):
        """Clean up resources"""
        if self.file_handle:
            self.file_handle.close()
        if self.sock:
            self.sock.close()
        print(f"Data saved to: {self.output_file}")
    
    def run(self):
        """Main execution function"""
        if not self.connect():
            return False
        
        if not self.open_file():
            self.cleanup()
            return False
        
        try:
            self.receive_data()
        finally:
            self.cleanup()
        
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tcp_client.py <red_pitaya_ip> [port] [output_file]")
        print("Example: python3 tcp_client.py 192.168.1.50 8888 data.csv")
        return 1
    
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8888
    output_file = sys.argv[3] if len(sys.argv) > 3 else f"unified_timestamps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    client = TCPClient(host, port, output_file)
    success = client.run()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
