from __future__ import annotations

from typing import Dict, List

from .models import Monitor, MonitorRoles, WorkspacePlan


HALLS = ["A", "B", "C", "D"]


def assign_monitor_roles(monitors: List[Monitor], multitask_index: int) -> MonitorRoles:
    n = len(monitors)
    if n == 0:
        raise RuntimeError("No monitors detected")

    multitask_index = max(0, min(multitask_index, n - 1))

    if n == 1:
        return MonitorRoles(primary_static=0, halls_swappable=0, docs_static=None)

    if n == 2:
        other = 1 - multitask_index
        return MonitorRoles(primary_static=other, halls_swappable=multitask_index, docs_static=None)

    static_candidates = [i for i in range(n) if i != multitask_index]
    primary_static = static_candidates[0]
    docs_static = static_candidates[1]
    return MonitorRoles(
        primary_static=primary_static,
        halls_swappable=multitask_index,
        docs_static=docs_static,
    )


def plan_workspaces(selected_halls: List[str], dual_monitor_mode: bool) -> Dict[str, WorkspacePlan]:
    plans: Dict[str, WorkspacePlan] = {
        "core": WorkspacePlan(name="core", index=0),
    }

    next_idx = 2 if dual_monitor_mode else 1
    for hall in HALLS:
        if hall in selected_halls:
            plans[f"hall:{hall}"] = WorkspacePlan(name=f"hall:{hall}", index=next_idx)
            next_idx += 1

    plans["shared_plots"] = WorkspacePlan(name="shared_plots", index=0)

    if dual_monitor_mode:
        plans["docs"] = WorkspacePlan(name="docs", index=1)
    else:
        plans["docs"] = WorkspacePlan(name="docs", index=0)

    return plans
