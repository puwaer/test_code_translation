import os
import json
import random
import itertools

# 拡張子とプログラミング言語のマッピング
EXT_TO_LANG = {
    '.cpp': 'C++',
    '.py': 'Python',
    '.go': 'Go',
    '.rs': 'Rust',
    '.cr': 'Crystal',
    '.kn': 'Kuin',
    '.rb': 'Ruby',
    '.cc': 'C++',
    '.cs': 'C#',
    '.swift': 'Swift'
}

def generate_json_from_folder(folder_path, output_json_path):
    # フォルダー内のファイル一覧を取得
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # 言語とファイル内容を対応付ける辞書
    lang_files = {}
    for file in files:
        ext = os.path.splitext(file)[1]  # 拡張子を取得
        if ext in EXT_TO_LANG:
            lang = EXT_TO_LANG[ext]
            try:
                with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                    content = f.read()  # ファイルの中身を読み込む
            except Exception as e:
                content = f"{lang} のコード"  # 読み込み失敗時は仮のプレースホルダー
            lang_files[lang] = content

    # JSON データの構築
    json_data = []
    id_counter = 1
    languages = list(lang_files.keys())

    # すべての言語ペアの組み合わせを作成
    for lang1, lang2 in itertools.combinations(languages, 2):
        entry = {"id": id_counter, "name": os.path.basename(folder_path)}
        entry[lang1] = lang_files[lang1]
        entry[lang2] = lang_files[lang2]
        json_data.append(entry)
        id_counter += 1

    # JSON ファイルとして保存
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    return json_data

if __name__ == "__main__":
    input_folder_path = "./data/atcoder/code/004"  
    output_json_path = "output.json"  
    result = generate_json_from_folder(input_folder_path, output_json_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
