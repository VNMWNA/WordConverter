# WordConverter.py

結構な頻度で思うことなんですけど、word ファイルって開くのめんどくさくないですか？
ターミナルから内容を参照できないし、専用のアプリケーションを立ち上げないといけないし....
ということで、markdownに落としてくれるコンバーターを作りました。(ありがとうcloude. love you)
wordファイルのデータ文字列は簡単には読めませんが、マークダウン程度になれば比較的楽に読めます。嬉しいですね。

Word ファイル（`.docx`）を **Markdown** または **HTML** に変換するスクリプトです。
見出し・表・箇条書き・太字・画像などの書式をそのまま保持して変換します。

---

## 必要なもの

| ツール | 用途 | インストール方法 |
| :--- | :--- | :--- |
| Python 3.8 以上 | スクリプト本体の実行 | [python.org](https://www.python.org/) |
| pandoc | Word ファイルの変換エンジン | 下記参照 |

### pandoc のインストール

#### Mac（Homebrew）

```bash
brew install pandoc
```

#### Ubuntu / Debian

```bash
sudo apt install pandoc
```

#### Windows

[pandoc.org/installing](https://pandoc.org/installing.html) からインストーラーをダウンロードして実行。

インストール確認：

```bash
pandoc --version
```

---

## 使い方

### Markdown に変換する（デフォルト）

```bash
python3 WordConverter.py 資料.docx
```

→ `資料.md` が`資料.docx`と同じフォルダに生成されます。

### HTML に変換する

```bash
python3 WordConverter.py 資料.docx --html
```

→ `資料.html` が生成されます。画像は Base64 でファイル内に埋め込まれるため、1ファイルで完結します。

### 出力先・ファイル名を指定する

```bash
python3 WordConverter.py 資料.docx -o output/変換後.md
python3 WordConverter.py 資料.docx --html -o output/変換後.html
```

### ヘルプを確認する

```bash
python3 WordConverter.py --help
```

---

## オプション一覧

| オプション | 省略形 | 説明 |
| :--- | :--- | :--- |
| `--html` | なし | HTML 形式で出力（省略時は Markdown） |
| `--output <パス>` | `-o <パス>` | 出力ファイルのパスを指定 |
| `--help` | `-h` | ヘルプを表示 |

---

## 変換される要素

| Word の書式 | Markdown | HTML |
| :--- | :--- | :--- |
| 見出し（H1〜H6） | `#` `##` ... | `<h1>` `<h2>` ... |
| 表 | `\| --- \|` 形式 | `<table>` |
| 箇条書き | `- 項目` | `<ul><li>` |
| 番号付きリスト | `1. 項目` | `<ol><li>` |
| 太字 | `**テキスト**` | `<strong>` |
| イタリック | `_テキスト_` | `<em>` |
| リンク | `[text](url)` | `<a href="">` |
| 画像 | `![alt](path)` | Base64 インライン埋め込み |

---

## ファイル構成

```text
.
├── WordConverter.py   # 変換スクリプト本体
└── README.md          # このファイル
```

---

## よくあるエラー

**`pandoc: command not found`**
→ pandoc がインストールされていません。上記「pandoc のインストール」を参照してください。

**`[ERROR] ファイルが見つかりません`**
→ ファイルパスが間違っています。ファイル名のスペルとカレントディレクトリを確認してください。

**`[WARN] 非対応の拡張子かもしれません`**
→ `.docx` / `.doc` / `.odt` 以外のファイルを指定しています。変換自体は試みますが、結果が崩れる可能性があります。

**PowerShell で `.venv\Scripts\Activate.ps1` が実行できない**
→ 実行ポリシーの制限です。以下を管理者権限の PowerShell で一度だけ実行してください。

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
