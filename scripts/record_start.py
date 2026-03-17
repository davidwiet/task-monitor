#!/usr/bin/env python3
import sys
import os
import time

def main():
    # Record the current time to a temporary file
    start_file = os.path.expanduser("~/.gemini/tmp/task_start_time")
    os.makedirs(os.path.dirname(start_file), exist_ok=True)
    with open(start_file, "w") as f:
        f.write(str(time.time()))
    
    # Standard Hook Output
    print("{}")

if __name__ == "__main__":
    main()
