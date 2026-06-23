from __future__ import annotations

import argparse
import shutil
import sys

from .config import load_config
from .discovery import discover_monitors
from .planner import compute_placements
from .policy import assign_monitor_roles, plan_workspaces
from .reconcile import apply_once, watch_loop
from .window_manager import WM


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Layout engine v2")
    p.add_argument("mode", choices=["plan", "apply", "watch"])
    p.add_argument("--config", default="config/layout.yaml")
    p.add_argument("--interval", type=float, default=5.0)
    p.add_argument("--multitask-monitor", type=int, default=None)
    p.add_argument("--halls", default=None, help="Comma separated halls: A,B,C,D")
    p.add_argument("--window-timeout", type=float, default=12.0)
    p.add_argument("--poll-interval", type=float, default=0.15)
    return p


def _check_dependencies(mode: str) -> bool:
    missing = []
    if shutil.which("xrandr") is None:
        missing.append("xrandr")
    if mode in ("apply", "watch") and shutil.which("wmctrl") is None:
        missing.append("wmctrl")

    if missing:
        print(
            "[ERROR] Missing required dependency(s): " + ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "[HINT] Install the missing tools or run in 'plan' mode only.",
            file=sys.stderr,
        )
        return False
    return True


def main() -> int:
    args = build_parser().parse_args()

    if not _check_dependencies(args.mode):
        return 2

    cfg = load_config(args.config)

    if args.multitask_monitor is not None:
        cfg.policy.multitask_monitor_index = args.multitask_monitor
    if args.halls:
        cfg.policy.selected_halls = [h.strip().upper() for h in args.halls.split(",") if h.strip()]

    monitors = discover_monitors()
    if not monitors:
        print("[ERROR] No monitors detected", file=sys.stderr)
        return 2

    roles = assign_monitor_roles(monitors, cfg.policy.multitask_monitor_index)
    dual = len(monitors) == 2
    ws = plan_workspaces(cfg.policy.selected_halls, dual_monitor_mode=dual)

    placements = compute_placements(monitors, roles, ws, cfg.apps)

    if args.mode == "plan":
        print("=== Monitors ===")
        for i, m in enumerate(monitors):
            print(f"{i}: {m.name} ({m.width}x{m.height}+{m.x}+{m.y})")
        print("=== Roles ===")
        print(f"primary_static={roles.primary_static}, halls_swappable={roles.halls_swappable}, docs_static={roles.docs_static}")
        print("=== Workspaces ===")
        for k, v in ws.items():
            print(f"{k} -> {v.index}")
        print("=== Placements ===")
        for p in placements:
            print(f"{p.app.name}: ws={p.workspace}, zone={p.app.zone}, geom=({p.x},{p.y} {p.w}x{p.h})")
        return 0

    wm = WM(poll_interval=args.poll_interval, window_timeout=args.window_timeout)

    if args.mode == "apply":
        apply_once(wm, placements)
        wm.switch_workspace(0)
        return 0

    watch_loop(wm, placements, interval_sec=args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
