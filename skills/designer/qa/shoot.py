#!/usr/bin/env python3
"""QA capture for the designer skill / design-reviewer agent.

Usage:  python shoot.py <url-or-html-file> <out-dir> [--widths 390,768,1440]

Opens the page in real Chrome (Edge fallback) via Playwright, then for each width:
  - saves viewport screenshots at 5 scroll depths (0/25/50/75/100%) plus one full-page shot
  - records horizontal overflow, console errors, failed requests, h1 count, images without alt,
    missing viewport meta, text under 12px, tap targets under 40px (mobile widths only)
Then repeats the widest capture with prefers-reduced-motion emulated and reports how many
animations are still running. Writes <out-dir>/report.json and prints a short summary.
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

DEPTHS = [0, 25, 50, 75, 100]

CHECKS_JS = """
() => {
  const de = document.documentElement;
  const vw = window.innerWidth;
  const overflowers = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed') {
      if (overflowers.length < 6) overflowers.push((el.tagName + '.' + (el.className || '')).toString().slice(0, 60));
    }
  });
  const imgsNoAlt = [...document.images].filter(i => !i.hasAttribute('alt')).length;
  const smallText = [];
  document.querySelectorAll('p, li, a, button, span, label').forEach(el => {
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2);
    if (!hasText) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 12 && smallText.length < 5) smallText.push(el.textContent.trim().slice(0, 30) + ' (' + fs + 'px)');
  });
  const smallTargets = [];
  document.querySelectorAll('a, button, input, select, textarea, [role=button]').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && r.height && (r.height < 40 || r.width < 40) && smallTargets.length < 6)
      smallTargets.push(((el.textContent || el.name || el.tagName) + '').trim().slice(0, 24) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  });
  return {
    scrollWidth: de.scrollWidth, innerWidth: vw, scrollHeight: de.scrollHeight,
    hOverflow: de.scrollWidth > vw + 1, overflowers,
    h1: document.querySelectorAll('h1').length,
    viewportMeta: !!document.querySelector('meta[name=viewport]'),
    title: document.title, imgsNoAlt, smallText, smallTargets,
  };
}
"""

RUNNING_JS = "document.getAnimations().filter(a => a.playState === 'running' && a.effect && a.effect.getComputedTiming().iterations === Infinity).length"


def target_url(arg):
    if arg.startswith(("http://", "https://", "file://")):
        return arg
    return pathlib.Path(arg).resolve().as_uri()


def launch(p):
    for channel in ("chrome", "msedge"):
        try:
            return p.chromium.launch(channel=channel, headless=True)
        except Exception:
            continue
    return p.chromium.launch(headless=True)


def capture(browser, url, out, width, tag, reduced=False):
    height = 900 if width > 600 else 844
    ctx = browser.new_context(
        viewport={"width": width, "height": height},
        reduced_motion="reduce" if reduced else "no-preference",
        device_scale_factor=1,
    )
    page = ctx.new_page()
    errors, failed = [], []
    page.on("console", lambda m: errors.append(m.text[:160]) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)[:160]))
    page.on("requestfailed", lambda r: failed.append(r.url[-200:]))
    page.goto(url, wait_until="load", timeout=45000)
    page.wait_for_timeout(1200)
    metrics = page.evaluate(CHECKS_JS)
    total = metrics["scrollHeight"]
    shots = []
    for d in DEPTHS:
        y = int(max(total - height, 0) * d / 100)
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(700)
        f = out / f"{tag}-{width}-scroll{d:03d}.png"
        page.screenshot(path=str(f))
        shots.append(f.name)
    metrics["infiniteAnimationsRunning"] = page.evaluate(RUNNING_JS)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    full = out / f"{tag}-{width}-full.png"
    try:
        page.screenshot(path=str(full), full_page=True)
        shots.append(full.name)
    except Exception as e:
        errors.append("full-page shot failed: " + str(e)[:100])
    ctx.close()
    return {"width": width, "reduced_motion": reduced, "metrics": metrics,
            "console_errors": errors[:8], "failed_requests": failed[:8], "screenshots": shots}


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    target, outdir = args[0], pathlib.Path(args[1])
    widths = [390, 768, 1440]
    if "--widths" in args:
        widths = [int(x) for x in args[args.index("--widths") + 1].split(",")]
    outdir.mkdir(parents=True, exist_ok=True)
    url = target_url(target)
    results = []
    with sync_playwright() as p:
        browser = launch(p)
        for w in widths:
            results.append(capture(browser, url, outdir, w, "std"))
        results.append(capture(browser, url, outdir, max(widths), "reduced", reduced=True))
        browser.close()
    (outdir / "report.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("QA capture:", url)
    for r in results:
        m = r["metrics"]
        label = f"{r['width']}px" + (" reduced-motion" if r["reduced_motion"] else "")
        flags = []
        if m["hOverflow"]:
            flags.append(f"H-OVERFLOW {m['scrollWidth']}>{m['innerWidth']} {m['overflowers'][:3]}")
        if m["h1"] != 1:
            flags.append(f"h1 count={m['h1']}")
        if not m["viewportMeta"]:
            flags.append("no viewport meta")
        if m["imgsNoAlt"]:
            flags.append(f"{m['imgsNoAlt']} img without alt")
        if m["smallText"]:
            flags.append(f"text under 12px: {m['smallText'][:2]}")
        if r["width"] <= 500 and m["smallTargets"]:
            flags.append(f"small tap targets: {m['smallTargets'][:3]}")
        if r["console_errors"]:
            flags.append(f"console errors: {r['console_errors'][:2]}")
        if r["failed_requests"]:
            flags.append(f"failed requests: {r['failed_requests'][:2]}")
        if r["reduced_motion"] and m["infiniteAnimationsRunning"]:
            flags.append(f"{m['infiniteAnimationsRunning']} infinite animations still running under reduced motion")
        print(f"  {label}: " + ("; ".join(flags) if flags else "clean"))
    print("Screenshots + report.json in", outdir)


if __name__ == "__main__":
    main()
