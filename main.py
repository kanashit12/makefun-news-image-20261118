"""make.fun entry: sum up 18 November 2026's world news in one image.

Writes the bundled front page (1024x1024 PNG, under 1 MiB) to
/output/entry.png. Deterministic, no network: it copies news.png
byte-for-byte, so two runs produce identical bytes.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out = Path("/output/entry.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "news.png", out)


if __name__ == "__main__":
    main()
