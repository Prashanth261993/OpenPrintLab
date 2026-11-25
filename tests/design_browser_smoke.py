"""Actual reviewed source, revision export and live viewer journey. Optional CAD."""

from functools import partial
from http.server import ThreadingHTTPServer
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from threading import Thread

from playwright.sync_api import sync_playwright

from tools.catalog import ROOT
from tools.designs import create_design, revise_design, review_digest
from tools.design_viewer import DesignHandler


def main():
    source = (ROOT / "examples/custom-designs/round-palette/source.py").read_text(encoding="utf-8")
    brief = json.loads((ROOT / "examples/custom-designs/round-palette/brief.json").read_text())
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        first = create_design("round-palette", brief, source, root)
        directory = Path(first["directory"])
        subprocess.run([sys.executable, str(directory / "source.py"), "--reviewed-sha256",
                        first["review_sha256"]], check=True, capture_output=True, cwd=ROOT)
        snapshot = {p.name: p.read_bytes() for p in (directory / "output").iterdir()}
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(DesignHandler, directory=str(root)))
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}/"
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={"width": 375, "height": 812})
                page.goto(base + "round-palette/")
                page.wait_for_function("document.querySelector('#reference').textContent === 'round-palette:r0001'")
                assert page.locator("#preview").is_visible()
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                with page.expect_download() as download:
                    page.get_by_role("link", name="model.stl", exact=True).click()
                assert Path(download.value.path()).read_bytes() == snapshot["model.stl"]
                second = revise_design("round-palette", root)
                d2 = Path(second["directory"])
                revised = json.loads((d2 / "brief.json").read_text())
                revised["parameters"]["diameter"] = 80
                revised["parameters"]["wells"] = 8
                revised["expected_dimensions_mm"] = [80, 80, 8]
                revised["acceptance"] = ["Outside diameter 80 mm and height 8 mm", "Eight blind circular wells of diameter 14 mm", "Base 2 mm and at least 2 mm material between wells"]
                (d2 / "brief.json").write_text(json.dumps(revised), encoding="utf-8")
                bad = subprocess.run([sys.executable, str(d2 / "source.py"), "--reviewed-sha256",
                                      first["review_sha256"]], capture_output=True, cwd=ROOT)
                assert bad.returncode != 0
                assert page.locator("#reference").inner_text() == "round-palette:r0001"
                subprocess.run([sys.executable, str(d2 / "source.py"), "--reviewed-sha256",
                                review_digest(d2)], check=True, capture_output=True, cwd=ROOT)
                page.wait_for_function("document.querySelector('#reference').textContent === 'round-palette:r0002'")
                assert page.locator("#preview").get_attribute("src").startswith("r0002/")
                assert snapshot == {p.name: p.read_bytes() for p in (directory / "output").iterdir()}
                assert hashlib.sha256((d2 / "output/model.stl").read_bytes()).hexdigest() != hashlib.sha256(snapshot["model.stl"]).hexdigest()
                assert page.request.get(base).status == 403
                assert page.request.get(base + "round-palette/.publish.lock").status == 403
                # A stale/corrupt current pointer must not masquerade as a refreshed design.
                current = root / "round-palette/current.json"
                pointer = json.loads(current.read_text())
                pointer["report_sha256"] = "0" * 64
                current.write_text(json.dumps(pointer))
                page.wait_for_function("document.querySelector('#status').textContent.includes('hash mismatch')")
                browser.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
    print("Custom design: actual source execution, dimension edit, immutable originals, live revision, downloads and stale-report refusal passed.")


if __name__ == "__main__":
    main()
