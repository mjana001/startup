from __future__ import annotations

import time
from typing import List

from .planner import Placement
from .window_manager import WM


def apply_once(wm: WM, placements: List[Placement], switch_each_workspace: bool = True) -> None:
    # group by workspace for deterministic launch behavior
    by_ws = {}
    for p in placements:
        by_ws.setdefault(p.workspace, []).append(p)

    for ws in sorted(by_ws.keys()):
        if switch_each_workspace:
            wm.switch_workspace(ws)
            time.sleep(0.1)

        for p in by_ws[ws]:
            w = wm.find_window(p.app.matchers)
            if w is None:
                w = wm.launch_and_wait(p.app.command, p.app.matchers)
            if w is None:
                print(f"[WARN] timeout launching/matching {p.app.name}")
                continue

            wm.move_to_workspace(w.wid, p.workspace)
            wm.place(w.wid, p.x, p.y, p.w, p.h, no_resize=p.no_resize)
            if p.app.retitle:
                wm.retitle(w.wid, p.app.retitle)

            print(
                f"[OK] {p.app.name}: ws={p.workspace} "
                f"geom=({p.x},{p.y} {p.w}x{p.h}) no_resize={p.no_resize}"
            )


def watch_loop(wm: WM, placements: List[Placement], interval_sec: float = 5.0) -> None:
    while True:
        apply_once(wm, placements, switch_each_workspace=False)
        time.sleep(interval_sec)
