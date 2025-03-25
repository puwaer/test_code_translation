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


def combine_json_files(output_dir, combined_output_path):
    combined_data = []
    global_id = 1  # 全体で通し番号にするためのカウンタ
    
    # 001 から 080 までのファイルを読み込む
    for i in range(1, 81):
        folder_name = f"{i:03d}"
        json_path = os.path.join(output_dir, f"{folder_name}.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 各エントリの id を再割り当て
                for entry in data:
                    entry["id"] = global_id
                    combined_data.append(entry)
                    global_id += 1
        else:
            print(f"Warning: {json_path} does not exist.")
    
    # 統合ファイルを保存
    with open(combined_output_path, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    return combined_data

if __name__ == "__main__":
    base_path = "./data/atcoder/code"  # ベースディレクトリ
    output_dir = "./data/atcoder/code_data/problem"  # 個別JSONの出力先ディレクトリ
    combined_output_path = "./data/atcoder/code_data/data.json"  # 統合JSONのパス
    
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 001 から 080 までのフォルダーを処理
    for i in range(1, 81):
        folder_name = f"{i:03d}"  # 001, 002, ..., 080
        folder_path = os.path.join(base_path, folder_name)
        output_json_path = os.path.join(output_dir, f"{folder_name}.json")
        
        if os.path.exists(folder_path):
            result = generate_json_from_folder(folder_path, output_json_path)
            print(f"Processed {folder_name}:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Folder {folder_name} does not exist.")
    
    # 全てのJSONファイルを統合
    combined_result = combine_json_files(output_dir, combined_output_path)
    print(f"\nCombined all JSON files into {combined_output_path}:")
    print(json.dumps(combined_result, ensure_ascii=False, indent=2))