# Test-Task
This Python program synchronizes two folders, source and replica, maintaining a full and identical copy of source folder at replica folder 

## Features

- One-way synchronization from source to replica.
- Periodic synchronization based on a specified interval.
- Logging of file creation, copying, and removal operations to a specified log file and console output.

## Usage

```bash
python3 sync_tool.py -s /path/to/source/folder -r /path/to/replica/folder -l /path/to/log/file.log -i interval_in_seconds 
