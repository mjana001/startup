from __future__ import annotations

import yaml
from typing import Any, Dict, List

from .models import AppSpec, Config, LayoutPolicy


def load_config(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        raw: Dict[str, Any] = yaml.safe_load(f)

    policy_raw = raw.get("policy", {})
    policy = LayoutPolicy(
        selected_halls=policy_raw.get("selected_halls", ["A", "B", "C", "D"]),
        multitask_monitor_index=int(policy_raw.get("multitask_monitor_index", 0)),
    )

    apps: List[AppSpec] = []
    for a in raw.get("apps", []):
        apps.append(
            AppSpec(
                name=a["name"],
                matchers=list(a.get("matchers", [])),
                command=a["command"],
                zone=a["zone"],
                workspace=a["workspace"],
                anchor=a.get("anchor", "TL"),
                size=a.get("size", "100%,100%"),
                offset=a.get("offset", "0,0"),
                retitle=a.get("retitle"),
                no_resize=bool(a.get("no_resize", False)),
                enabled=bool(a.get("enabled", True)),
            )
        )

    return Config(policy=policy, apps=apps)
