"""Read-only loopback viewer for custom design revisions; no code execution. MIT."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from tools.designs import DEFAULT_DESIGNS, _safe_path


class DesignHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        relative = unquote(urlsplit(self.path).path).lstrip("/")
        parts = Path(relative).parts
        if "\\" in relative or ".." in parts or any(p.startswith(".") for p in parts):
            self.send_error(403)
            return None
        root = Path(self.directory).resolve()
        path = root / relative
        if not path.resolve().is_relative_to(root) or any(p.is_symlink() for p in (path, *path.parents)):
            self.send_error(403)
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(403, "Directory listing disabled; open /DESIGN-ID/")
        return None

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=DEFAULT_DESIGNS)
    parser.add_argument("--port", type=int, default=8767)
    args = parser.parse_args()
    root = _safe_path(args.directory)
    root.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(DesignHandler, directory=str(root)))
    print(f"Custom design viewer: http://127.0.0.1:{server.server_port}/DESIGN-ID/ (read only)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
