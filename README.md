# AI Log Manager for NotebookLM

Gemini 2.0 Flash を活用して、開発ログやアイデアメモを自動で整理・保存する Streamlit アプリです。
Google ドライブなどの同期フォルダに保存することで、**NotebookLM のソースとして直接活用可能な「自分専用のナレッジベース」を自動構築します。**
<img width="1920" height="878" alt="AI-Log-Manager-01-20-2026_02_25_PM" src="https://github.com/user-attachments/assets/aaddef5c-1d06-41c6-9ce4-7f3cde804d1f" />

## 🚀 特徴

* **AIによる自動整理**: テキストを投げ込むだけで、Gemini が「プロジェクト分類」「タグ付け」「タイトル生成」「要約」を自動で行います。
* **NotebookLM 最適化**: NotebookLM が読み込みやすい Markdown 形式で、プロジェクトごとのフォルダに構造化して保存します。
* **Gemini 2.0 Flash 対応**: 高速かつ高精度な最新モデルを使用（設定で変更可能）。
* **簡単起動**: `run_app.bat` をダブルクリックするだけで起動できます。

## 🛠️ 技術スタック

* Python 3.10+
* Streamlit
* Google Generative AI SDK (Gemini API)

## 📦 インストールと設定

### 1. リポジトリのクローン
```bash
git clone [(https://github.com/teshiokayumi/AIlog)
cd AIlog

```

### 2. 依存ライブラリのインストール

```bash
pip install -r requirements.txt

```

### 3. 環境変数の設定

リポジトリに含まれている `.env.sample` ファイルをコピーして、ファイル名を `.env` に変更してください。

```bash
cp .env.sample .env

```

`.env` ファイルを開き、ご自身の Google API Key を入力します。
（APIキーは [Google AI Studio](https://aistudio.google.com/app/apikey) から取得できます）

```text
GOOGLE_API_KEY=your_api_key_here

```

## ▶️ 使い方

### Windows の場合

フォルダ内の `run_app.bat` をダブルクリックするだけで起動します。

### コマンドラインから起動する場合

```bash
streamlit run app.py

```
<img width="1920" height="878" alt="AI-Log-Manager-01-20-2026_01_30_PM" src="https://github.com/user-attachments/assets/b717a01d-9744-404c-9e80-e21d5700f341" />

起動後、ブラウザでアプリが開きます。

1. サイドバーで「保存先ルートフォルダ」を指定します（Googleドライブのフォルダ推奨）。
2. テキストエリアにログやメモを入力します。
3. 「保存・整理を実行」ボタンを押すと、AIが自動でフォルダを作成し、Markdownファイルを保存します。

### 更新
サイドバーにあるモデルを先に選んで実行することで、エラーをなくしました。

## ⚠️ 注意事項

* このアプリは Google Gemini API を使用します。APIの利用料金や制限については Google のドキュメントをご確認ください（無料枠の範囲内でも十分動作します）。
* 生成された Markdown ファイルはローカル（または指定したクラウドストレージ）に保存されます。

## License

MIT License
