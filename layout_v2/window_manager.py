from __future__ import annotations

import re
import shlex
import subprocess
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Window:
    wid: str
    desktop: int
    host: str
    title: str


class WM:
    def __init__(self, poll_interval: float = 0.15, window_timeout: float = 12.0) -> None:
        self.poll_interval = poll_interval
        self.window_timeout = window_timeout

    def run(self, cmd: List[str], check: bool = False) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True, text=True, check=check)

    def list_windows(self) -> List[Window]:
        out = self.run(["wmctrl", "-l"]).stdout
        wins: List[Window] = []
        for line in out.splitlines():
            parts = line.split(None, 3)
            if len(parts) < 4:
                continue
            wid, desk, host, title = parts[0], int(parts[1]), parts[2], parts[3]
            wins.append(Window(wid=wid, desktop=desk, host=host, title=title))
        return wins

    def find_window(self, matchers: List[str]) -> Optional[Window]:
        wins = self.list_windows()
        for w in wins:
            for m in matchers:
                if m.startswith("EXACT:") and w.title == m[6:]:
                    return w
                if m.startswith("SUB:") and m[4:] in w.title:
                    return w
                if m.startswith("REGEX:"):
                    if re.search(m[6:], w.title):
                        return w
        return None

    def launch(self, command: str) -> subprocess.Popen:
        return subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def launch_and_wait(self, command: str, matchers: List[str]) -> Optional[Window]:
        self.launch(command)
        waited = 0.0
        while waited < self.window_timeout:
            w = self.find_window(matchers)
            if w:
                return w
            time.sleep(self.poll_interval)
            waited += self.poll_interval
        return None

    def switch_workspace(self, ws: int) -> None:
        self.run(["wmctrl", "-s", str(ws)])

    def move_to_workspace(self, wid: str, ws: int) -> None:
        self.run(["wmctrl", "-i", "-r", wid, "-t", str(ws)])

    def place(self, wid: str, x: int, y: int, w: int, h: int, no_resize: bool = False) -> None:
        if no_resize:
            self.run(["wmctrl", "-i", "-r", wid, "-e", f"0,{x},{y},-1,-1"])
        else:
            self.run(["wmctrl", "-i", "-r", wid, "-e", f"0,{x},{y},{w},{h}"])

    def retitle(self, wid: str, title: str) -> None:
        self.run(["wmctrl", "-i", "-r", wid, "-N", title])
