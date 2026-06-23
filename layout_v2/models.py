from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Monitor:
    name: str
    x: int
    y: int
    width: int
    height: int


@dataclass
class WorkspacePlan:
    name: str
    index: int


@dataclass
class MonitorRoles:
    primary_static: int
    halls_swappable: int
    docs_static: Optional[int] = None


@dataclass
class AppSpec:
    name: str
    matchers: List[str]
    command: str
    zone: str
    workspace: str
    anchor: str
    size: str
    offset: str = "0,0"
    retitle: Optional[str] = None
    no_resize: bool = False
    enabled: bool = True


@dataclass
class LayoutPolicy:
    selected_halls: List[str] = field(default_factory=lambda: ["A", "B", "C", "D"])
    multitask_monitor_index: int = 0


@dataclass
class Config:
    policy: LayoutPolicy
    apps: List[AppSpec]
