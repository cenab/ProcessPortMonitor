# ProcessPortMonitor

**ProcessPortMonitor** is a Python package that allows you to monitor active TCP ports used by a specific process (PID) in real-time. It provides both a command-line interface (CLI) and an importable module for integration into your Python scripts. The package can asynchronously track port changes, trigger callbacks when changes occur, and maintain a history of port activity with timestamps.
---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
    - [Basic Usage](#basic-usage)
    - [Options](#options)
  - [As a Python Module](#as-a-python-module)
    - [Basic Usage](#basic-usage-module)
    - [Customizing the Callback Function](#customizing-the-callback-function)
    - [Accessing Port History](#accessing-port-history)
- [Examples](#examples)
  - [Example CLI Session](#example-cli-session)
  - [Example Python Script](#example-python-script)
- [Requirements](#requirements)
- [Limitations](#limitations)
- [License](#license)

---

## Features

- **Real-Time Monitoring**: Continuously monitors active TCP ports used by a specific PID.
- **Asynchronous Operation**: Runs in a separate thread to avoid blocking your main program.
- **Callback Mechanism**: Triggers a user-defined callback function when port changes are detected.
- **Port History Tracking**: Maintains a history of port additions and removals with timestamps.
- **Command-Line Interface**: Provides a convenient CLI for quick monitoring from the terminal.
- **Python Module**: Can be imported and used within your Python applications without terminal output.

---

## Installation

### Prerequisites

- **Python 3.6 or higher**
- **`lsof` command**: Available on most Unix-like systems (macOS, Linux).
- **`jc` library**: JSON Convert library for parsing command output.

### Install Using `pip`

```bash
pip3 install ProcessPortMonitor
```

Alternatively, you can install from source:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ProcessPortMonitor.git
   ```

2. **Navigate to the Package Directory**

   ```bash
   cd ProcessPortMonitor
   ```

3. **Install the Package**

   ```bash
   pip3 install .
   ```

---

## Usage

### Command-Line Interface

#### Basic Usage

Run `ProcessPortMonitor` followed by the PID of the process you wish to monitor. You may need to run the command with `sudo` to have the necessary permissions.

```bash
sudo ProcessPortMonitor <PID>
```

#### Options

- `--interval INTERVAL`: Set the monitoring interval in seconds (default is 1.0 second).

```bash
sudo ProcessPortMonitor <PID> --interval 0.5
```

#### Example

```bash
sudo ProcessPortMonitor 16609 --interval 1
```

**Output:**

```
Monitoring active ports for PID 16609 every 1.0 second(s). Press Ctrl+C to stop.
New ports opened: {50260}
Active ports: {50260}
New ports opened: {50390}
Active ports: {50260, 50390}
Ports closed: {50260}
Active ports: {50390}
```

### As a Python Module

#### Basic Usage (Module)

Import the `ProcessPortMonitor` class into your Python script and create an instance to monitor a specific PID.

```python
from ProcessPortMonitor import ProcessPortMonitor
import time

def my_callback(new_ports, closed_ports, active_ports, port_history):
    # Handle port changes here
    if new_ports:
        print(f"Ports added: {new_ports}")
    if closed_ports:
        print(f"Ports removed: {closed_ports}")
    # You can also process active_ports and port_history as needed

pid_to_monitor = 16609  # Replace with the actual PID
monitor = ProcessPortMonitor(pid_to_monitor, interval=1.0, callback=my_callback)
monitor.start()

try:
    while True:
        # Your main program logic here
        time.sleep(1)
except KeyboardInterrupt:
    monitor.stop()
    print("Stopped monitoring.")
```

#### Customizing the Callback Function

The callback function should accept four parameters:

- `new_ports`: A set of ports that have been added since the last check.
- `closed_ports`: A set of ports that have been closed since the last check.
- `active_ports`: The current set of active ports.
- `port_history`: A list of dictionaries containing the history of port changes with timestamps.

Example of a callback function:

```python
def my_callback(new_ports, closed_ports, active_ports, port_history):
    if new_ports:
        print(f"New ports opened: {new_ports}")
    if closed_ports:
        print(f"Ports closed: {closed_ports}")
    print(f"Current active ports: {active_ports}")
    # Optionally, process port_history
```

#### Accessing Port History

The `port_history` attribute of the `ProcessPortMonitor` instance stores the history of port changes.

```python
# Access the port history
print(monitor.port_history)
```

Each entry in `port_history` is a dictionary:

```python
{
    'timestamp': '2023-10-03T12:00:00.000000',
    'port': 50260,
    'action': 'added'  # or 'removed'
}
```

---

## Examples

### Example CLI Session

```bash
sudo ProcessPortMonitor 12345 --interval 0.5
```

**Output:**

```
Monitoring active ports for PID 12345 every 0.5 second(s). Press Ctrl+C to stop.
New ports opened: {8080}
Active ports: {8080}
Ports closed: {8080}
Active ports: set()
```

### Example Python Script

```python
from ProcessPortMonitor import ProcessPortMonitor
import time

def log_port_changes(new_ports, closed_ports, active_ports, port_history):
    if new_ports:
        print(f"[+] Ports opened: {new_ports}")
    if closed_ports:
        print(f"[-] Ports closed: {closed_ports}")
    print(f"[=] Current ports: {active_ports}")

pid = 12345
monitor = ProcessPortMonitor(pid, interval=0.5, callback=log_port_changes)
monitor.start()

try:
    while True:
        # Main application logic
        time.sleep(1)
except KeyboardInterrupt:
    monitor.stop()
    print("Monitoring stopped.")
```

---

## Requirements

- **Python 3.6 or higher**
- **`lsof` command**: The script uses `lsof` to retrieve active TCP connections.
- **`jc` library**: Install via `pip3 install jc`.

---

## Limitations

- **Permissions**: Monitoring processes other than your own may require root privileges.
- **Platform Compatibility**: Designed for Unix-like systems (macOS, Linux) with `lsof` available.
- **System Resources**: Frequent monitoring intervals may impact system performance due to repeated `lsof` calls.
- **TCP Connections Only**: Currently monitors TCP connections in the `ESTABLISHED` state.

---

## License

**ProcessPortMonitor** is released under the [MIT License](https://opensource.org/licenses/MIT).

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or report bugs.

---

## Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/cenab/ProcessPortMonitor) or contact the maintainer at [batu.bora.tech@gmail.com](mailto:batu.bora.tech@gmail.com).