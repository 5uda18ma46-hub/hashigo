#!/usr/bin/env python3
"""index.html を直したら、コミットする前にこれを走らせる。

    python3 bump_version.py

やること: `index.html` の `APP_VERSION` を今日の日付ベースの新しい値にして、
`version.json` に同じ値を書く。

なぜ要るか: アプリはホーム画面に追加して使うので、こちらが直しても端末が
古い画面を持ち続けることがある。アプリは起動時に `version.json` を見て、
自分の `APP_VERSION` と違えば「新しいバージョンがあります」と出す。

**この2つがずれると壊れる。**
- version.json のほうが新しい → 更新の知らせが消えない
- index.html のほうが新しい → 新しい版が出ても気づけない
だから手で書き換えず、必ずこのスクリプトを通すこと。
"""

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"
VER = ROOT / "version.json"
JST = timezone(timedelta(hours=9))
PATTERN = re.compile(r"(const APP_VERSION = ')([^']+)(';)")


def main():
    html = HTML.read_text()
    m = PATTERN.search(html)
    if not m:
        print("index.html に APP_VERSION が見つかりません。")
        return 1
    current = m.group(2)

    today = datetime.now(JST).strftime("%Y-%m-%d")
    n = 1
    if current.startswith(today + "."):
        try:
            n = int(current.split(".")[-1]) + 1
        except ValueError:
            n = 2
    new = f"{today}.{n}"

    HTML.write_text(PATTERN.sub(rf"\g<1>{new}\g<3>", html))
    VER.write_text(json.dumps({
        "version": new,
        "_comment": "index.html の APP_VERSION と必ず同じ値にする。bump_version.py が両方を書き換える。",
    }, ensure_ascii=False, indent=2) + "\n")

    print(f"{current} → {new}")
    print("index.html と version.json を更新しました。このままコミットしてください。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
