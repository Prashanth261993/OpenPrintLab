"""Serve only local variant bundles; no AI, upload or printer endpoints."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil

from tools.catalog import ROOT
from tools.variants import DEFAULT_OUTPUT, check_variant_root, render_index


def seed_examples(directory, *, refresh_curated=False):
    directory = Path(directory)
    check_variant_root(directory)
    directory.mkdir(parents=True, exist_ok=True)
    examples = ROOT / "examples" / "template-lab"
    if examples.is_dir():
        for source in sorted(examples.iterdir()):
            if source.is_dir() and (source / "report.json").is_file():
                target = directory / source.name
                if not target.exists():
                    shutil.copytree(source, target)
                elif refresh_curated:
                    if target.is_symlink():
                        raise ValueError("Curated site examples must not use symlinks")
                    shutil.copytree(source, target, dirs_exist_ok=True)
    render_index(directory)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--directory", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    seed_examples(args.directory)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(SimpleHTTPRequestHandler, directory=str(args.directory)))
    print(f"Template lab: http://127.0.0.1:{server.server_port}/ (viewer only; stop with Ctrl+C)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
