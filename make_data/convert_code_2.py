import os
import json
from pathlib import Path

def escape_code(code):
    """コード文字列をJSON用にエスケープする"""
    return code.replace('\n', '\\n').replace('"', '\\"')

def create_json_pairs(base_dir, languages=None):
    if languages is None:
        languages = {
            'cpp': '.cpp',
            'python': '.py'
        }  # デフォルトで2つの言語（C++とPython）
    
    # 言語が2つであることを確認
    if len(languages) != 2:
        raise ValueError("Exactly 2 languages must be specified.")
    
    result = []
    id_counter = 1
    
    # 各言語のディレクトリからファイルを取得
    lang_files = {}
    for lang, ext in languages.items():
        lang_dir = os.path.join(base_dir, lang)
        if os.path.exists(lang_dir):
            # 再帰的に全ファイルを検索
            lang_files[lang] = {}
            for root, _, files in os.walk(lang_dir):
                for f in files:
                    if f.endswith(ext):
                        # 拡張子を除いたファイル名をキーとして保存
                        base_name = f.rsplit('.', 1)[0]  # 拡張子を削除
                        lang_files[lang][base_name] = os.path.join(root, f)
        else:
            lang_files[lang] = {}
    
    # 基準となる言語（最初の言語）でファイル名を取得
    base_lang = list(languages.keys())[0]
    if not lang_files[base_lang]:
        return result
    
    # 同じ名前のファイルをペアリング
    for base_name in lang_files[base_lang]:
        # ファイル名をそのまま使用（番号の抽出や整形はしない）
        entry = {"id": id_counter, "name": base_name}
        codes_found = 0
        
        for lang, ext in languages.items():
            if base_name in lang_files[lang]:
                with open(lang_files[lang][base_name], 'r', encoding='utf-8') as f:
                    code = f.read()
                    entry[lang.capitalize()] = code
                    codes_found += 1
        
        # 2つの言語のコードが揃っている場合のみ追加
        if codes_found == 2:
            result.append(entry)
            id_counter += 1
    
    return result

def main():
    # ベースディレクトリを指定
    base_dir = "C:/Users/y_50u/Documents/GitHub/test_code_translation/data/kyopro-tessoku-main/codes"
    
    # 使用する2つの言語を指定
    languages = {
        #'cpp': '.cpp',
        'python': '.py',
        'java': '.java'
        # 他の組み合わせ例: 'cpp': '.cpp', 'java': '.java'
    }
    
    # 出力JSONファイルのパス
    output_json_path = "kyopro_codes_py_java.json"
    
    # ディレクトリ存在チェック
    if not os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} not found.")
        return
    
    # JSONデータを作成
    json_data = create_json_pairs(base_dir, languages)
    
    # JSONファイルに保存
    if json_data:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"Created {output_json_path} with {len(json_data)} entries")
    else:
        print("No data collected.")

if __name__ == "__main__":
    main()