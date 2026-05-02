#!/usr/bin/env python3
"""Minimal HTML-to-PNG converter for debugging Graphify HTML artifacts."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render an HTML file to PNG using a local headless Chromium browser.")
    parser.add_argument("html", help="Input HTML file path")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--width", type=int, default=1600, help="Viewport width in pixels")
    parser.add_argument("--height", type=int, default=1200, help="Viewport height in pixels")
    return parser.parse_args()


def find_browser() -> str | None:
    env_browser = os.environ.get("GRAPHIFY_BROWSER")
    if env_browser and Path(env_browser).exists():
        return env_browser

    for candidate in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved

    playwright_candidates = [
        Path.home() / ".cache/ms-playwright/chromium-1217/chrome-linux/chrome",
        Path.home() / ".cache/ms-playwright/chromium-1217/chrome-linux64/chrome",
    ]
    for candidate in playwright_candidates:
        if candidate.exists():
            return str(candidate)

    return None


def main() -> int:
    args = parse_args()
    browser = find_browser()
    if not browser:
        print("BROWSER_NOT_FOUND: install Chromium or Chrome to enable HTML-to-PNG conversion.", file=sys.stderr)
        return 2

    html_path = Path(args.html).resolve()
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--window-size={args.width},{args.height}",
        f"--screenshot={output_path}",
        html_path.as_uri(),
    ]
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
