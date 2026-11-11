from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

from tools.catalog import load_catalog
from tools.site import build_site


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


class SiteTests(unittest.TestCase):
    def test_all_generated_local_links_and_fragments_resolve(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build_site(root)
            pages = {}
            for path in root.rglob("*.html"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("%%", text)
                parser = Links()
                parser.feed(text)
                pages[path.resolve()] = parser
            self.assertEqual(len(pages), 12)
            for path, parser in pages.items():
                for link in parser.links:
                    url = urlsplit(link)
                    if url.scheme or url.netloc:
                        continue
                    target = (path.parent / unquote(url.path)).resolve() if url.path else path
                    if target.is_dir():
                        target = target / "index.html"
                    self.assertTrue(target.is_relative_to(root.resolve()), link)
                    self.assertTrue(target.is_file(), f"{path.name}: {link}")
                    if url.fragment and target in pages:
                        self.assertIn(url.fragment, pages[target].ids, f"{path.name}: {link}")
            for model in load_catalog()["models"]:
                for suffix in (".stl", ".svg", ".report.json", ".scad", ".source.zip"):
                    self.assertGreater((root / "downloads" / f"{model['id']}{suffix}").stat().st_size, 50)


if __name__ == "__main__":
    unittest.main()
