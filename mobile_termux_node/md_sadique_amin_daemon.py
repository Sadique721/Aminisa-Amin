"""
Compatibility forwarding layer to aminsa_daemon.py
"""
import sys
from aminsa_daemon import execute_slot_cycle, run_daemon_loop

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        execute_slot_cycle(skip_yt_generation=False)
    elif len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        execute_slot_cycle(skip_yt_generation=True)
    elif len(sys.argv) > 1 and sys.argv[1] == "--slot":
        slot_num = int(sys.argv[2])
        execute_slot_cycle(slot_idx=slot_num, skip_yt_generation=False)
    else:
        run_daemon_loop()
