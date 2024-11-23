import argparse
import sys
import signal
from .monitor import PortMonitor

def main():
    parser = argparse.ArgumentParser(description='Monitor active ports for a PID in real-time.')
    parser.add_argument('pid', type=int, help='Process ID to monitor')
    parser.add_argument('--interval', type=float, default=1.0, help='Monitoring interval in seconds (default: 1 second)')
    args = parser.parse_args()

    pid = args.pid
    interval = args.interval

    monitor = PortMonitor(pid, interval=interval, callback=print_port_changes)

    print(f"Monitoring active ports for PID {pid} every {interval} second(s). Press Ctrl+C to stop.")

    def signal_handler(sig, frame):
        print("\nStopping monitoring.")
        monitor.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    monitor.start()
    monitor._thread.join()

def print_port_changes(new_ports, closed_ports, active_ports, port_history):
    if new_ports:
        print(f"New ports opened: {new_ports}")
    if closed_ports:
        print(f"Ports closed: {closed_ports}")
    print(f"Active ports: {active_ports}")

if __name__ == '__main__':
    main()
