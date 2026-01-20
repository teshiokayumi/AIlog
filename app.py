import streamlit as st
import google.generativeai as genai
import os
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Page configuration
st.set_page_config(page_title="AI Log Manager", layout="wide")

# Sidebar
with st.sidebar:
    st.header("設定")
    
    # API Key Input
    api_key_env = os.getenv("GOOGLE_API_KEY")
    api_key = st.text_input("Google API Key", value=api_key_env if api_key_env else "", type="password").strip()

    # Model Selection
    st.markdown("### モデル設定")
    if st.button("🔄 利用可能なモデルを取得"):
        try:
            genai.configure(api_key=api_key)
            models = [m.name.replace("models/", "") for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
            st.session_state["available_models"] = models
            st.success(f"{len(models)} 個のモデルが見つかりました")
        except Exception as e:
            st.error(f"モデル取得失敗: {e}")

    default_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.5-flash-001", "gemini-1.5-pro", "gemini-pro"]
    model_options = st.session_state.get("available_models", default_models)
    
    # Ensure default options are included if fetch fails or is empty, but don't duplicate
    for dm in default_models:
        if dm not in model_options:
            model_options.append(dm)
            
    selected_model = st.selectbox("使用モデル", model_options, index=0)

    # Root Path Input
    default_path = "./my_ai_logs"
    root_path_input = st.text_input("保存先ルートフォルダ", value=default_path)

    # Open Folder Button
    if st.button("📂 保存先フォルダを開く"):
        try:
            abs_path = os.path.abspath(root_path_input)
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            os.startfile(abs_path)
            st.sidebar.success(f"開きました: {abs_path}")
        except Exception as e:
            st.sidebar.error(f"エラー: {e}")

    st.markdown("---")
    st.markdown("### 次回の起動コマンド")
    st.caption("次回はこのコマンドをコピーして実行するか、`run_app.bat`をダブルクリックしてください。")
    st.code("streamlit run app.py", language="bash")

# Main Area
st.title("AI Log Manager for NotebookLM")
st.caption("開発ログや対話履歴をGemini 2.0 Flashで自動整理・保存します")

input_text = st.text_area("ログ入力エリア", height=300, placeholder="ここにテキストを貼り付けてください...")

def save_log(api_key, root_path, text, model_name):
    if not api_key:
        st.error("API Keyを入力してください。")
        return
    
    if not text.strip():
        st.warning("テキストが空です。")
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = """
        あなたは優秀なAIアシスタントです。以下の入力テキストを分析し、指定されたJSON形式でのみ出力してください。
        Markdownコードブロックなどの装飾は不要です。純粋なJSON文字列のみを返してください。
        全ての値は日本語で出力してください（project_nameとcategoryは英語推奨）。

        入力テキスト:
        {text}

        出力JSONフォーマット:
        {{
            "project_name": "内容から推測されるプロジェクト名 (英語・アンダースコア推奨, 例: Medical_App)",
            "category": "内容の分類 (例: Spec, ErrorLog, Idea, Draft)",
            "title": "ファイル名に使える簡潔なタイトル (日本語可, スペースはアンダースコアに)",
            "summary": "内容の3行要約 (日本語)",
            "tags": ["タグ1", "タグ2"]
        }}
        """.format(text=text)

        with st.spinner(f"{model_name} が分析中..."):
            response = model.generate_content(prompt)
            # Remove markdown code blocks if present
            cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned_response)

        # Extract data
        project_name = data.get("project_name", "General")
        category = data.get("category", "Memo")
        title = data.get("title", "Untitled")
        summary = data.get("summary", "要約なし")
        tags = data.get("tags", [])
        
        # Format tags
        tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
        
        # Prepare file content
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        file_content = f"""---
project: {project_name}
category: {category}
tags: [{tags_str}]
created_at: {time_str}
---
# {title}

## AI要約
{summary}

## 本文
{text}
"""
        
        # Save file
        save_dir = Path(root_path) / project_name
        save_dir.mkdir(parents=True, exist_ok=True)
        
        file_name = f"{date_str}_{title}.md"
        # Sanitize filename (basic)
        file_name = "".join(c for c in file_name if c.isalnum() or c in (' ', '.', '_', '-')).strip()
        file_path = save_dir / file_name
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)
            
        st.success(f"保存完了: {file_path}")
        st.json(data) # Show the parsed data for verification

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        # Fallback save
        fallback_dir = Path(root_path) / "_Uncategorized"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.datetime.now()
        fallback_file = fallback_dir / f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_error_log.md"
        with open(fallback_file, "w", encoding="utf-8") as f:
            f.write(text)
        st.info(f"解析に失敗したため、原文をそのまま保存しました: {fallback_file}")

if st.button("保存・整理を実行"):
    save_log(api_key, root_path_input, input_text, selected_model)
