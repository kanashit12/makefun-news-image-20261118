#!/usr/bin/env python3
"""make.fun news-image-20261118 entry.

Writes the front-page image summing up 18 November 2026's world news to
/output/entry.png. Deterministic, no network: it copies the image bundled in
this repository (news.png, built by compose.py in this repo).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "news.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
