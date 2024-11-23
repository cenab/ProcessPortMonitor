import subprocess
import jc
import threading
import time
from datetime import datetime

class ProcessPortMonitor:
    """
    Monitors active TCP ports for a specific process ID (PID) in real-time.
    
    This class provides functionality to track port changes, maintain history,
    and trigger callbacks when port status changes occur.
    """

    def __init__(self, pid, interval=1.0, callback=None):
        """
        Initialize the port monitor.

        :param pid: Process ID to monitor.
        :param interval: Monitoring interval in seconds.
        :param callback: Function to call when ports change.
        """
        self.pid = pid
        self.interval = interval
        self.callback = callback
        self._stop_event = threading.Event()
        self.active_ports = set()
        self.port_history = []
        self._thread = threading.Thread(target=self._monitor)
        self._thread.daemon = True  # Daemon thread exits when the main thread exits

    def retrieve_active_ports(self):
        """
        Retrieve the current active TCP ports for the PID.

        Returns:
            set: A set of active port numbers
        
        Raises:
            subprocess.SubprocessError: If the lsof command fails
            ValueError: If port parsing fails
            FileNotFoundError: If lsof is not installed
        """
        try:
            lsof_cmd = [
                'lsof',
                '-nP',
                '-iTCP',
                '-sTCP:ESTABLISHED',
                '-a',
                '-p', str(self.pid)
            ]
            result = subprocess.run(lsof_cmd, capture_output=True, text=True, check=True)
            output = result.stdout

            if not output.strip():
                return set()

            # Parse output with jc
            try:
                connections = jc.parse('lsof', output)
            except Exception as e:
                raise ValueError(f"Failed to parse lsof output: {str(e)}")

            ports = set()
            for conn in connections:
                local_address = conn.get('name', '')
                try:
                    if '->' in local_address:
                        local_part = local_address.split('->')[0]
                        if ':' in local_part:
                            local_port = local_part.rsplit(':', 1)[-1]
                            if local_port.isdigit():
                                ports.add(int(local_port))
                    elif ':' in local_address:
                        local_port = local_address.rsplit(':', 1)[-1]
                        if local_port.isdigit():
                            ports.add(int(local_port))
                except Exception as e:
                    raise ValueError(f"Failed to parse port from address {local_address}: {str(e)}")
            return ports
        except FileNotFoundError:
            raise FileNotFoundError("lsof command not found. Please install lsof package.")
        except subprocess.SubprocessError as e:
            raise subprocess.SubprocessError(f"Failed to execute lsof command: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while retrieving ports: {str(e)}")

    def start(self):
        """
        Start monitoring the active ports.
        """
        self._stop_event.clear()
        self._thread.start()

    def stop(self):
        """
        Stop monitoring the active ports.
        """
        self._stop_event.set()
        self._thread.join()

    def _monitor(self):
        """
        Internal method to monitor ports in a separate thread.
        """
        previous_ports = set()
        while not self._stop_event.is_set():
            current_ports = self.retrieve_active_ports()
            if current_ports != previous_ports:
                new_ports = current_ports - previous_ports
                closed_ports = previous_ports - current_ports

                timestamp = datetime.now().isoformat()
                if new_ports:
                    for port in new_ports:
                        self.port_history.append({
                            'timestamp': timestamp,
                            'port': port,
                            'action': 'added'
                        })
                if closed_ports:
                    for port in closed_ports:
                        self.port_history.append({
                            'timestamp': timestamp,
                            'port': port,
                            'action': 'removed'
                        })
                # Update the active ports
                self.active_ports = current_ports.copy()

                # Trigger the callback if provided
                if self.callback:
                    self.callback(new_ports, closed_ports, self.active_ports, self.port_history)

                # No terminal output when imported as a module

                previous_ports = current_ports.copy()

            time.sleep(self.interval)