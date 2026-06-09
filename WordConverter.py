#!/usr/bin/env python3
"""
Word (.docx) → Markdown / HTML 変換スクリプト
使い方:
  python3 convert_docx.py input.docx              # → input.md
  python3 convert_docx.py input.docx --html       # → input.html
  python3 convert_docx.py input.docx -o out.md    # 出力ファイル名を指定
"""

import argparse
import subprocess
import sys
from pathlib import Path


def convert(input_path: Path, output_path: Path, fmt: str) -> None:
    """pandoc を使って変換する"""

    if fmt == "markdown":
        pandoc_fmt = "gfm"  # GitHub Flavored Markdown（表が綺麗に出る）
        extra_args = [
            "--wrap=none",           # 自動折り返しなし（読みやすい）
            "--markdown-headings=atx",  # ## 形式の見出し
        ]
    else:
        pandoc_fmt = "html5"
        extra_args = [
            "--standalone",          # <html>〜</html> まで含んだ完全なHTMLを生成
            "--embed-resources",     # 画像をBase64でインライン埋め込み
            "--metadata", "charset=UTF-8",
        ]

    cmd = [
        "pandoc",
        str(input_path),
        "-t", pandoc_fmt,
        "-o", str(output_path),
        *extra_args,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] pandoc 失敗:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    if result.stderr:
        # 警告があれば表示（エラーではない）
        print(f"[WARN] {result.stderr.strip()}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Word → Markdown/HTML 変換")
    parser.add_argument("input", type=Path, help=".docx ファイルのパス")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="出力ファイルのパス（省略時は同名で拡張子だけ変わる）")
    parser.add_argument("--html", action="store_true",
                        help="HTML形式で出力（デフォルトはMarkdown）")
    args = parser.parse_args()

    input_path = args.input.resolve()
    if not input_path.exists():
        print(f"[ERROR] ファイルが見つかりません: {input_path}", file=sys.stderr)
        sys.exit(1)
    if input_path.suffix.lower() not in (".docx", ".doc", ".odt"):
        print(f"[WARN] 非対応の拡張子かもしれません: {input_path.suffix}")

    fmt = "html" if args.html else "markdown"
    ext = ".html" if args.html else ".md"

    if args.output:
        output_path = args.output.resolve()
    else:
        output_path = input_path.with_suffix(ext)

    print(f"変換中: {input_path.name} → {output_path.name} ({fmt})")
    convert(input_path, output_path, fmt)
    print(f"完了しました: {output_path}")


if __name__ == "__main__":
    main()
