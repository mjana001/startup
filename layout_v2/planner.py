from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .models import AppSpec, Monitor, MonitorRoles, WorkspacePlan


@dataclass
class Placement:
    app: AppSpec
    workspace: int
    x: int
    y: int
    w: int
    h: int
    no_resize: bool


def _parse_pair(s: str) -> Tuple[str, str]:
    a, b = [p.strip() for p in s.split(",", 1)]
    return a, b


def _resolve_len(v: str, total: int) -> int:
    v = v.strip()
    if v.endswith("%"):
        return max(1, total * int(v[:-1]) // 100)
    return int(v)


def _anchor_xy(anchor: str, mx: int, my: int, mw: int, mh: int, sw: int, sh: int) -> Tuple[int, int]:
    a = anchor.upper()
    if a in ("TL", "TOP_LEFT"):
        return mx, my
    if a in ("TR", "TOP_RIGHT"):
        return mx + mw - sw, my
    if a in ("BL", "BOTTOM_LEFT"):
        return mx, my + mh - sh
    if a in ("BR", "BOTTOM_RIGHT"):
        return mx + mw - sw, my + mh - sh
    if a == "CENTER":
        return mx + (mw - sw) // 2, my + (mh - sh) // 2
    if a == "LEFT":
        return mx, my + (mh - sh) // 2
    if a == "RIGHT":
        return mx + mw - sw, my + (mh - sh) // 2
    if a == "TOP":
        return mx + (mw - sw) // 2, my
    if a == "BOTTOM":
        return mx + (mw - sw) // 2, my + mh - sh
    return mx, my


def zone_monitor_index(zone: str, roles: MonitorRoles) -> int:
    z = zone.lower()
    if z == "primary":
        return roles.primary_static
    if z == "docs":
        return roles.docs_static if roles.docs_static is not None else roles.primary_static
    if z == "halls":
        return roles.halls_swappable
    raise ValueError(f"Unknown zone: {zone}")


def workspace_for(app_ws: str, plans: Dict[str, WorkspacePlan]) -> int:
    if app_ws.startswith("hall:"):
        return plans.get(app_ws, plans["core"]).index
    return plans.get(app_ws, plans["core"]).index


def compute_placements(
    monitors: List[Monitor],
    roles: MonitorRoles,
    ws_plans: Dict[str, WorkspacePlan],
    apps: List[AppSpec],
) -> List[Placement]:
    placements: List[Placement] = []
    for app in apps:
        if not app.enabled:
            continue

        mon_idx = zone_monitor_index(app.zone, roles)
        mon = monitors[mon_idx]

        sw_raw, sh_raw = _parse_pair(app.size)
        ox_raw, oy_raw = _parse_pair(app.offset)

        sw = _resolve_len(sw_raw, mon.width)
        sh = _resolve_len(sh_raw, mon.height)
        ox = _resolve_len(ox_raw, mon.width)
        oy = _resolve_len(oy_raw, mon.height)

        x, y = _anchor_xy(app.anchor, mon.x, mon.y, mon.width, mon.height, sw, sh)
        x += ox
        y += oy

        ws = workspace_for(app.workspace, ws_plans)

        placements.append(
            Placement(
                app=app,
                workspace=ws,
                x=x,
                y=y,
                w=sw,
                h=sh,
                no_resize=app.no_resize,
            )
        )
    return placements
