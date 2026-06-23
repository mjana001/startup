from __future__ import annotations

import re
import subprocess
from typing import List

from .models import Monitor


XRANDR_RE = re.compile(r"^([A-Za-z0-9-]+) connected.*? ([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)")


def discover_monitors() -> List[Monitor]:
    proc = subprocess.run(["xrandr", "--query"], capture_output=True, text=True, check=False)
    monitors: List[Monitor] = []
    for line in proc.stdout.splitlines():
        m = XRANDR_RE.search(line)
        if not m:
            continue
        name, w, h, x, y = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
        monitors.append(Monitor(name=name, x=x, y=y, width=w, height=h))

    monitors.sort(key=lambda mm: mm.x)
    return monitors
