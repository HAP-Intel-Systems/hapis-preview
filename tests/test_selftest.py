"""Public credibility test for the HAPIS Engine preview image.

Proves there is real ITU-R code behind the API: it calls the running
container's unauthenticated `/v1/selftest`, which computes a fixed set of
ITU-R reference cases with the real engine, and asserts every case reproduces
its published reference value within tolerance.

Run it:

    docker run -d -p 8000:8000 ghcr.io/hap-intel-systems/hapis-api:latest
    pip install pytest
    pytest -v

Point at a different host/port with HAPIS_BASE_URL (default http://localhost:8000).
No API key is needed — /v1/selftest is intentionally public.
"""
import json
import os
import urllib.request

BASE_URL = os.environ.get("HAPIS_BASE_URL", "http://localhost:8000")

EXPECTED_STANDARDS = {
    "ITU-R P.525-4", "ITU-R P.676-13", "ITU-R P.838-3",
    "ITU-R P.840-8", "ITU-R P.2108-1",
}


def _get_selftest():
    with urllib.request.urlopen(f"{BASE_URL}/v1/selftest", timeout=30) as resp:
        assert resp.status == 200, f"unexpected status {resp.status}"
        return json.load(resp)


def test_selftest_overall_pass():
    """The engine reproduces every published reference case within tolerance."""
    report = _get_selftest()
    assert report["overall"]["status"] == "pass", json.dumps(report, indent=2)
    assert report["overall"]["passed"] == report["overall"]["total"]


def test_selftest_covers_five_standards():
    """One real case per ITU-R standard is exercised."""
    report = _get_selftest()
    standards = {c["standard"] for c in report["cases"]}
    assert EXPECTED_STANDARDS <= standards


def test_every_case_reports_real_numbers_within_tolerance():
    """Each case exposes computed vs published reference, and they agree."""
    report = _get_selftest()
    for case in report["cases"]:
        assert {"computed", "reference", "delta", "tolerance"} <= case.keys()
        assert abs(case["delta"]) <= case["tolerance"], f"{case['id']} drifted: {case}"
