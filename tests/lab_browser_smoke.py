"""Verify the actual local template preview and download journey."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
from pathlib import Path
import tempfile
from threading import Thread

from playwright.sync_api import sync_playwright

from tools.catalog import ROOT
from tools.variants import create_variant


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        result = create_variant("rounded-organizer", "browser-desk-tray",
                                {"length": 120, "width": 80, "height": 18, "compartments": 3, "radius": 8}, root)
        create_variant("rounded-pen-rest", "browser-pen-rest", {}, root)
        create_variant("paper-card-stand", "browser-card-stand", {}, root)
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(root)))
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        screenshots = ROOT / "build" / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_page(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                base = f"http://127.0.0.1:{server.server_port}"
                page.goto(base, wait_until="networkidle")
                assert page.locator(".lab-card").count() == 3
                assert not page.locator("input,textarea").count()
                page.screenshot(path=str(screenshots / "template-lab.png"), full_page=True)
                page.get_by_role("link", name="Preview & downloads").first.click()
                page.goto(base + "/browser-desk-tray/", wait_until="networkidle")
                assert page.locator("img").evaluate("(image) => image.complete && image.naturalWidth > 0")
                assert page.get_by_text("Geometry checked only.", exact=True).is_visible()
                page.screenshot(path=str(screenshots / "custom-organizer.png"), full_page=True)
                for label, key in (("Download STL", "stl_sha256"), ("Download STEP", "step_sha256")):
                    with page.expect_download() as downloading:
                        page.get_by_role("link", name=label, exact=True).click()
                    data = Path(downloading.value.path()).read_bytes()
                    assert hashlib.sha256(data).hexdigest() == result["report"]["artifacts"][key]
                report_url = page.get_by_role("link", name="Variant passport", exact=True).get_attribute("href")
                response = page.request.get(base + "/browser-desk-tray/" + report_url)
                assert response.ok
                assert response.json()["passport"]["variant_id"] == result["report"]["passport"]["variant_id"]
                for width, height in ((375, 812), (812, 375), (1440, 1000)):
                    page.set_viewport_size({"width": width, "height": height})
                    for route in ("/", "/browser-desk-tray/", "/browser-card-stand/"):
                        page.goto(base + route, wait_until="networkidle")
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (width, route)
                page.goto(base + "/browser-desk-tray/")
                page.keyboard.press("Tab")
                assert page.get_by_role("link", name="Skip to content").evaluate("(element) => element === document.activeElement")
                assert not errors, errors
                browser.close()
            print("Template lab: actual geometry previews, STL/STEP hashes, passport, three families, keyboard and responsive layouts passed.")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    main()
