# Layout Engine v2

Declarative multi-monitor/workspace window layout engine.

## Goals

- Keep **General Tools** screen static
- Keep **Docs (ELOG/Firefox/Passdown)** screen static when 3+ monitors are available
- Put hall/liveplot workloads on a **swappable monitor** with workspace-driven switching
- Support both one-shot apply and continuous watch/reconcile modes

## Structure

- `config/layout.yaml` — declarative policy and window specs
- `layout_v2/cli.py` — CLI entrypoint
- `layout_v2/config.py` — config loader
- `layout_v2/models.py` — typed models
- `layout_v2/discovery.py` — monitor/window/workspace discovery
- `layout_v2/policy.py` — monitor role mapping and workspace planning
- `layout_v2/planner.py` — concrete placement plan generation
- `layout_v2/window_manager.py` — wmctrl/xrandr command wrapper
- `layout_v2/reconcile.py` — apply/reconcile loop

## Quick start

```bash
python3 -m layout_v2.cli plan --config config/layout.yaml
python3 -m layout_v2.cli apply --config config/layout.yaml
python3 -m layout_v2.cli watch --config config/layout.yaml --interval 5
```

## Notes

This scaffold intentionally separates:

1. discovery,
2. policy,
3. planning,
4. reconcile/apply.

That makes window behavior easier to evolve without changing core logic.
