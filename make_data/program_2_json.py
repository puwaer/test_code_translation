import os
import json
import random

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

def generate_json_from_folder(folder_path):
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
    total_langs = len(languages)
    
    if total_langs % 2 != 0:  # 奇数の場合
        # ランダムにシャッフル
        random.shuffle(languages)
        # 使用済み言語を追跡
        used_langs = set()
        temp_data = []
        
        # 2言語ずつのエントリを仮に作成
        for i in range(0, total_langs - 1, 2):
            entry = {"id": id_counter, "name": os.path.basename(folder_path)}
            entry[languages[i]] = lang_files[languages[i]]
            entry[languages[i + 1]] = lang_files[languages[i + 1]]
            used_langs.update([languages[i], languages[i + 1]])
            temp_data.append(entry)
            id_counter += 1
        
        # 3つ目のエントリを追加し、全言語をカバー
        remaining_langs = set(languages) - used_langs
        if remaining_langs:
            entry = {"id": id_counter, "name": os.path.basename(folder_path)}
            # 残りの言語を1つ選択
            lang1 = remaining_langs.pop()
            # 使用済みからランダムに1つ選択（ただし異なる言語）
            lang2 = random.choice([l for l in used_langs if l != lang1])
            entry[lang1] = lang_files[lang1]
            entry[lang2] = lang_files[lang2]
            temp_data.append(entry)
        
        json_data = temp_data[:3]  # 3エントリに制限
    
    else:  # 偶数の場合
        random.shuffle(languages)
        for i in range(0, total_langs, 2):
            entry = {"id": id_counter, "name": os.path.basename(folder_path)}
            entry[languages[i]] = lang_files[languages[i]]
            entry[languages[i + 1]] = lang_files[languages[i + 1]]
            json_data.append(entry)
            id_counter += 1
    
    # JSON ファイルとして保存
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    return json_data

# 使用例
folder_path = "./data/atcoder/code/004"  # 対象フォルダー
result = generate_json_from_folder(folder_path)
print(json.dumps(result, ensure_ascii=False, indent=2))