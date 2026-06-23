# Layout Engine v2

Declarative multi-monitor/workspace window layout engine.

## What it does

This project starts and arranges commonly used windows across multiple monitors and workspaces so the start-of-shift setup is consistent.

### Goals

- Keep **General Tools** screen static
- Keep **Docs (ELOG/Firefox/Passdown)** screen static when 3+ monitors are available
- Put hall/liveplot workloads on a **swappable monitor** with workspace-driven switching
- Support both one-shot apply and continuous watch/reconcile modes

## How to run

The CLI lives in `layout_v2/cli.py` and supports three modes:

```bash
python3 -m layout_v2.cli plan --config config/layout.yaml
python3 -m layout_v2.cli apply --config config/layout.yaml
python3 -m layout_v2.cli watch --config config/layout.yaml --interval 5
```

If `run_layout_v2.sh` appears to do nothing, check that:

- `xrandr` can detect your monitors
- `wmctrl` is installed and working
- `config/layout.yaml` exists and contains at least one enabled app
- the window matchers in the config actually match the running window titles

## Project structure

- `config/layout.yaml` — declarative policy and window specs
- `layout_v2/cli.py` — CLI entrypoint
- `layout_v2/config.py` — config loader
- `layout_v2/models.py` — typed models
- `layout_v2/discovery.py` — monitor discovery via `xrandr`
- `layout_v2/policy.py` — monitor role mapping and workspace planning
- `layout_v2/planner.py` — concrete placement plan generation
- `layout_v2/window_manager.py` — `wmctrl` wrapper for window operations
- `layout_v2/reconcile.py` — apply/reconcile loop

## Notes

The code is intentionally split into:

1. discovery,
2. policy,
3. planning,
4. reconcile/apply.

That keeps layout behavior easier to evolve without changing the core flow.
