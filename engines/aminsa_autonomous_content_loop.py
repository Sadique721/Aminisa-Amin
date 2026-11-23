#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aminsa Autonomous Content Loop Bridge / Alias
Directs execution to engines/md_sadique_amin_autonomous_content_loop.py
Prevents any missing file errors across workflows and external callers.
"""
import sys
import subprocess
from pathlib import Path

def main():
    target = Path(__file__).parent / "md_sadique_amin_autonomous_content_loop.py"
    if not target.exists():
        print(f"Notice: Target engine not found at {target}")
        sys.exit(0)
    
    cmd = [sys.executable, str(target)] + sys.argv[1:]
    res = subprocess.run(cmd)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
