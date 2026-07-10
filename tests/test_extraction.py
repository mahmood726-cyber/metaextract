"""Regression tests for MetaExtract.html's extractAll() engine.

The extraction core is JavaScript embedded in MetaExtract.html. These tests
load the <script> block, run extractAll() via Node, and assert on the parsed
output. They cover the demo/placeholder string and per-type CI separators,
which previously extracted nothing (silent zero-output bugs).

If Node is unavailable the tests skip rather than fail, so the smoke suite
still runs everywhere.
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "MetaExtract.html"

NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js not available")


def _run(text: str):
    """Run extractAll(text) from MetaExtract.html and return the parsed list."""
    html = HTML.read_text(encoding="utf-8")
    start = html.index("<script>") + len("<script>")
    end = html.index("</script>", start)
    js = html[start:end]
    js = js[: js.index("/* ── Main Extract ── */")]
    driver = (
        js
        + "\nconst __input = JSON.parse(process.argv[2]);"
        + "\nprocess.stdout.write(JSON.stringify(extractAll(__input)));\n"
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".mjs", delete=False, encoding="utf-8"
    ) as fh:
        fh.write(driver)
        path = fh.name
    try:
        out = subprocess.run(
            [NODE, path, json.dumps(text)],
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8",
        )
    finally:
        Path(path).unlink(missing_ok=True)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def _types(results):
    return sorted(r["effectType"] for r in results)


# --- F1: the app's own placeholder/demo string must extract HR + EVENTS ---
DEMO = (
    "The hazard ratio for the primary composite endpoint was 0.77 "
    "(95% CI 0.61-0.96; P=0.02). Events occurred in 131/2366 (5.5%) "
    "colchicine vs 170/2379 (7.1%) placebo patients."
)


def test_placeholder_demo_extracts_hr_and_events():
    results = _run(DEMO)
    assert _types(results) == ["EVENTS", "HR"], results
    hr = next(r for r in results if r["effectType"] == "HR")
    assert hr["value"] == 0.77
    assert hr["ciLo"] == 0.61 and hr["ciHi"] == 0.96
    ev = next(r for r in results if r["effectType"] == "EVENTS")
    assert (ev["tE"], ev["tN"], ev["cE"], ev["cN"]) == (131, 2366, 170, 2379)


def test_events_with_arm_label_between_pct_and_comparator():
    # F1(a): arm label between "(5.5%)" and "vs" previously broke EVENT_RX
    results = _run("131/2366 (5.5%) colchicine vs 170/2379 (7.1%) placebo")
    assert _types(results) == ["EVENTS"]


def test_hazard_ratio_with_intervening_words():
    # F1(b): words between "hazard ratio" and the value previously failed
    results = _run("hazard ratio for the endpoint was 0.77 (95% CI 0.61-0.96)")
    assert _types(results) == ["HR"]


# --- F2: both dash and "to" CI separators for every parenthetical type ---
@pytest.mark.parametrize(
    "etype,text_dash,text_to,val,lo,hi",
    [
        ("OR", "OR 2.10 (95% CI 1.50-3.00)", "OR 2.10 (95% CI 1.50 to 3.00)", 2.10, 1.50, 3.00),
        ("RR", "RR 0.80 (95% CI 0.65-0.95)", "RR 0.80 (95% CI 0.65 to 0.95)", 0.80, 0.65, 0.95),
        ("HR", "HR 0.77 (95% CI 0.61-0.96)", "HR 0.77 (95% CI 0.61 to 0.96)", 0.77, 0.61, 0.96),
        ("NNT", "NNT 25 (95% CI 15-50)", "NNT 25 (95% CI 15 to 50)", 25, 15, 50),
        ("SMD", "SMD 0.30 (95% CI 0.10-0.50)", "SMD 0.30 (95% CI 0.10 to 0.50)", 0.30, 0.10, 0.50),
        ("MD", "MD 2.5 (95% CI 1.0-4.0)", "MD 2.5 (95% CI 1.0 to 4.0)", 2.5, 1.0, 4.0),
    ],
)
def test_ci_separator_both_forms(etype, text_dash, text_to, val, lo, hi):
    for text in (text_dash, text_to):
        results = _run(text)
        match = [r for r in results if r["effectType"] == etype]
        assert match, f"{etype} not extracted from: {text}"
        r = match[0]
        assert r["value"] == val
        assert r["ciLo"] == lo and r["ciHi"] == hi


# --- F3: IRR abbreviation must extract (not only spelled-out forms) ---
def test_irr_abbreviation_extracts():
    results = _run("IRR 0.80 (95% CI 0.65-0.95)")
    match = [r for r in results if r["effectType"] == "IRR"]
    assert match, results
    assert match[0]["value"] == 0.80


def test_incidence_rate_ratio_spelled_out_still_works():
    results = _run("incidence rate ratio 0.80 (95% CI 0.65-0.95)")
    assert any(r["effectType"] == "IRR" for r in results)


# --- Negative / edge cases: must NOT extract ---
@pytest.mark.parametrize(
    "text",
    [
        "",                                            # empty
        "abc",                                         # too short
        "HR 0.77 (95% CI 0.96-0.61)",                  # lo > hi rejected
        "HR 999 (95% CI 500-2000)",                    # out of plausible range
        "The value 0.5 was noted (see figure 2).",     # no CI, no effect marker
        "5/100 had events. Later 10/200 developed disease.",  # events across sentence
    ],
)
def test_rejects_invalid_inputs(text):
    assert _run(text) == []
