"""End-to-end static site checks; server and browser are always closed."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

from tools.catalog import ROOT, build_model
from tools.site import build_site


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    build_site()
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT / "site")))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    screenshots = Path(os.environ.get("OPENPRINTLAB_SCREENSHOTS", ROOT / "build" / "screenshots"))
    screenshots.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base, wait_until="networkidle")
            assert page.locator(".model-card:visible").count() == 4
            page.screenshot(path=str(screenshots / "desktop.png"), full_page=True)
            page.get_by_label("Search the collection").fill("tray")
            assert page.locator(".model-card:visible").count() == 1
            page.get_by_role("button", name="Clear filters").click()
            page.get_by_label("Category", exact=True).select_option("Learning")
            assert page.locator(".model-card:visible").count() == 1
            assert "Layer staircase" in page.locator(".model-card:visible").inner_text()
            page.get_by_label("Search the collection").fill("nonexistent")
            assert page.locator("#empty-state").is_visible()
            page.reload()
            assert page.locator("#empty-state").is_visible()
            page.get_by_role("button", name="Clear filters").click()
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.id") == "category"
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.id") == "clear"
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.tagName") == "A"
            page.goto(base + "/models/pocket-tray.html")
            with page.expect_download() as download:
                page.get_by_role("link", name="Download STL").click()
            assert download.value.suggested_filename == "pocket-tray.stl"
            assert Path(download.value.path()).read_bytes() == build_model("pocket-tray")[0]
            assert page.get_by_role("link", name="Editable source ZIP").get_attribute("href").endswith(".source.zip")
            for width, height in ((375, 812), (812, 375), (768, 1024), (1440, 1000)):
                page.set_viewport_size({"width": width, "height": height})
                for route in ("/", "/beginner.html", "/create.html", "/reuse.html", "/models/parts-palette.html"):
                    page.goto(base + route, wait_until="networkidle")
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (width, route)
                    assert page.locator("h1").is_visible()
                if width == 375:
                    page.goto(base)
                    page.screenshot(path=str(screenshots / "mobile.png"), full_page=True)
                    page.add_style_tag(content="html { font-size: 200%; } body { font-size: 200%; }")
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            no_js = browser.new_context(java_script_enabled=False)
            plain = no_js.new_page()
            plain.goto(base)
            assert plain.locator(".model-card").count() == 4
            plain.get_by_role("link", name="View Pocket tray", exact=True).click()
            assert plain.get_by_role("link", name="Download STL").is_visible()
            plain.goto(base)
            plain.get_by_role("link", name="Patterns & diagnostics").click()
            assert plain.locator("#fastener-selection").is_visible()
            assert plain.locator("#material-service-envelope").is_visible()
            assert plain.locator("#geometry-design-review").is_visible()
            no_js.close()
            context.close()
            browser.close()
        print("Browser: search, category, empty/reset, URL state, keyboard, downloads, guides, responsive layouts and no-JS fallback passed.")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
