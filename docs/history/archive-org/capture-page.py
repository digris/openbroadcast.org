#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "playwright",
# ]
# ///

"""
Capture a Wayback Machine replay with Chromium and save a browser-native MHTML snapshot.

Why MHTML:
- Chromium loads the page normally, so only resources actually requested by the browser
  are considered.
- No recursive CSS/asset crawling.
- No manual rewriting of CSS url(...) / @import chains.
- The snapshot is self-contained and can be opened directly in Chromium/Chrome/Edge.

Output:
    <host>/<YYYY-MM-DD>/index.mhtml
    <host>/<YYYY-MM-DD>/index.html   (cleaned rendered DOM, useful for inspection)

Example:
    uv run capture-page.py \
      'https://web.archive.org/web/20100612192940/http://openbroadcast.ch/de/'

First run, if Chromium is not installed:
    uv run capture-page.py --install-browser
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


WAYBACK_RE = re.compile(
    r"^https?://web\.archive\.org/web/(\d{14})(?:[a-z_]+)?/(https?://.+)$",
    re.IGNORECASE,
)

WAYBACK_SELECTORS = [
    "#wm-ipp-base",
    "#wm-ipp-print",
    "#wm-capinfo",
    "#donato",
    ".wb-autocomplete-suggestions",
]

# These are useful while Wayback is replaying the page, so we do NOT block them.
# We only remove their DOM/script/link elements immediately before serialization.
WAYBACK_URL_MARKERS = (
    "web-static.archive.org/_static/",
    "/static/js/",
    "archive_analytics",
    "bundle-playback.js",
    "wombat.js",
    "ruffle.js",
    "banner-styles.css",
    "iconochive.css",
)


def parse_wayback_url(url: str) -> tuple[str, str]:
    m = WAYBACK_RE.match(url)
    if not m:
        raise ValueError(
            "Expected a Wayback replay URL like:\n"
            "https://web.archive.org/web/20100612192940/http://example.com/"
        )
    return m.group(1), m.group(2)


def output_dir_for(url: str, root: Path) -> Path:
    timestamp, original_url = parse_wayback_url(url)
    host = (urlsplit(original_url).hostname or "unknown-host").lower()
    if host.startswith("www."):
        host = host[4:]
    day = datetime.strptime(timestamp[:8], "%Y%m%d").strftime("%Y-%m-%d")
    return root / host / day


def install_browser() -> int:
    print("install  chromium")
    return subprocess.call([sys.executable, "-m", "playwright", "install", "chromium"])


def clean_wayback_dom(page) -> None:
    """
    Remove Wayback's toolbar/overlay and replay helper tags after the historical
    page has finished loading. We intentionally leave them available during load,
    because Wombat/replay rewriting can be required to fetch the archived page.
    """
    page.evaluate(
        """({selectors, markers}) => {
            for (const selector of selectors) {
                document.querySelectorAll(selector).forEach(el => el.remove());
            }

            const markerMatch = (value) => {
                if (!value) return false;
                const v = String(value).toLowerCase();
                return markers.some(m => v.includes(m));
            };

            for (const script of [...document.querySelectorAll("script")]) {
                const src = script.getAttribute("src") || "";
                const body = script.textContent || "";
                if (
                    markerMatch(src) ||
                    body.includes("__wm.") ||
                    body.includes("__wm_") ||
                    body.includes("archive_analytics") ||
                    body.includes("RufflePlayer")
                ) {
                    script.remove();
                }
            }

            for (const link of [...document.querySelectorAll("link")]) {
                if (markerMatch(link.getAttribute("href") || "")) {
                    link.remove();
                }
            }

            for (const style of [...document.querySelectorAll("style")]) {
                const body = style.textContent || "";
                if (
                    body.includes("#wm-ipp") ||
                    body.includes(".wb-autocomplete") ||
                    body.includes("Wayback")
                ) {
                    style.remove();
                }
            }

            // Wayback sometimes leaves this class/style state behind.
            document.documentElement.style.removeProperty("--wm-toolbar-height");
            document.body?.style.removeProperty("padding-top");
            document.body?.style.removeProperty("margin-top");
        }""",
        {
            "selectors": WAYBACK_SELECTORS,
            "markers": [m.lower() for m in WAYBACK_URL_MARKERS],
        },
    )


def capture(
    url: str,
    output_root: Path,
    wait_seconds: float,
    timeout_seconds: float,
    headed: bool,
    save_html: bool,
    screenshot: bool,
) -> Path:
    out_dir = output_root
    out_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context(
            viewport={"width": 1440, "height": 1000},
            service_workers="block",
        )
        page = context.new_page()

        # Keep useful logging small: failed browser requests only.
        page.on(
            "requestfailed",
            lambda request: print(f"fail   {request.resource_type:10s} {request.url}"),
        )

        print(f"page   {url}")

        try:
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=timeout_seconds * 1000,
            )
        except PlaywrightTimeoutError:
            # Old archived pages often never become perfectly idle. If the DOM
            # committed, we can still capture what Chromium managed to render.
            print("warn   navigation timed out; capturing loaded state")

        # Give ordinary load handlers and dynamically requested assets a short
        # chance to finish. Do not use networkidle: historical pages can poll,
        # hang, or reference permanently missing resources.
        try:
            page.wait_for_load_state("load", timeout=min(timeout_seconds, 10) * 1000)
        except PlaywrightTimeoutError:
            pass

        if wait_seconds > 0:
            page.wait_for_timeout(wait_seconds * 1000)

        # Stop late timers/navigation from changing the snapshot underneath us.
        cdp = context.new_cdp_session(page)
        try:
            cdp.send("Page.stopLoading")
        except PlaywrightError:
            pass

        clean_wayback_dom(page)

        # Save the cleaned rendered DOM as a convenience. It is NOT the offline
        # artifact; index.mhtml below is the self-contained browser snapshot.
        if save_html:
            html_path = out_dir / "index.html"
            html_path.write_text(page.content(), encoding="utf-8")
            print(f"html   {html_path}")

        if screenshot:
            screenshot_path = out_dir / "screenshot.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"shot   {screenshot_path}")

        # Browser-native serialization. Chromium packs the document and its
        # loaded external resources into a single MHTML file.
        result = cdp.send("Page.captureSnapshot", {"format": "mhtml"})
        mhtml_path = out_dir / "index.mhtml"
        mhtml_path.write_text(result["data"], encoding="utf-8")
        print(f"mhtml  {mhtml_path}")

        context.close()
        browser.close()

    return mhtml_path


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Capture a Wayback replay as a Chromium MHTML snapshot."
    )
    ap.add_argument("wayback_url", nargs="?", help="Full Wayback replay URL")
    ap.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=Path("."),
        help="Output directory (default: current directory)",
    )
    ap.add_argument(
        "--wait",
        type=float,
        default=2.0,
        help="Seconds to wait after load before capture (default: 2)",
    )
    ap.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Navigation timeout in seconds (default: 30)",
    )
    ap.add_argument(
        "--headed",
        action="store_true",
        help="Show Chromium while capturing",
    )
    ap.add_argument(
        "--no-html",
        action="store_true",
        help="Do not also save the cleaned rendered DOM as index.html",
    )
    ap.add_argument(
        "--screenshot",
        action="store_true",
        help="Also save screenshot.png",
    )
    ap.add_argument(
        "--install-browser",
        action="store_true",
        help="Install Playwright Chromium and exit",
    )
    args = ap.parse_args()

    if args.install_browser:
        return install_browser()

    if not args.wayback_url:
        ap.error("wayback_url is required unless --install-browser is used")

    try:
        capture(
            args.wayback_url,
            args.output,
            max(0.0, args.wait),
            max(1.0, args.timeout),
            args.headed,
            not args.no_html,
            args.screenshot,
        )
    except ValueError as exc:
        ap.error(str(exc))
    except PlaywrightError as exc:
        message = str(exc)
        if (
            "Executable doesn't exist" in message
            or "playwright install" in message.lower()
        ):
            print(
                "error  Playwright Chromium is not installed.\n"
                "       Run:\n"
                "       uv run capture-page.py --install-browser",
                file=sys.stderr,
            )
            return 2
        raise

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
