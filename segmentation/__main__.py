"""Offline CLI for declarative segmentation policy validation and reporting."""
import argparse
import json
import sys
from pathlib import Path
from .core import evaluate, render_nftables, report

def main():
    parser = argparse.ArgumentParser(description="Offline, non-invasive OT segmentation policy validator")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "report", "render"):
        p = sub.add_parser(command)
        p.add_argument("--policy", type=Path, required=True)
        if command != "validate":
            p.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"))
        issues = evaluate(policy)
        if issues:
            for item in issues:
                print(f"ERROR: {item}", file=sys.stderr)
            return 1
        if args.command == "validate":
            print("PASS: policy structurally valid; no declared forbidden conduits")
        elif args.command == "report":
            args.output.write_text(json.dumps(report(policy), indent=2) + "\n", encoding="utf-8")
            print(f"Wrote offline assurance report: {args.output}")
        else:
            args.output.write_text(render_nftables(policy), encoding="utf-8")
            print(f"Wrote illustrative ruleset (NOT activated): {args.output}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())

