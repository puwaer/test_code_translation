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
    
    # 章ごとのディレクトリを走査
    for chap_dir in sorted(os.listdir(base_dir)):
        chap_path = os.path.join(base_dir, chap_dir)
        # `chapXX` または `final` のようなディレクトリのみを対象
        if not os.path.isdir(chap_path) or (not chap_dir.startswith('chap') and chap_dir != 'final'):
            continue
            
        # 各言語のディレクトリとファイルを取得
        lang_files = {}
        for lang, ext in languages.items():
            lang_dir = os.path.join(chap_path, lang)
            if os.path.exists(lang_dir):
                lang_files[lang] = {
                    f: os.path.join(lang_dir, f)
                    for f in os.listdir(lang_dir)
                    if f.endswith(ext) and 'answer_' in f  # 'answer_' を含むファイルのみ対象
                }
            else:
                lang_files[lang] = {}
        
        # 基準となる言語（最初の言語）でファイル番号を取得
        base_lang = list(languages.keys())[0]
        if not lang_files[base_lang]:
            continue
            
        # 同じ番号のファイルをペアリング
        for base_file in lang_files[base_lang]:
            # ファイル名から番号を抽出（例: answer_A01.cpp → A01, answer_B01.cpp → B01）
            file_parts = base_file.split('_')
            if len(file_parts) < 2:
                continue
            file_num = file_parts[1].replace(languages[base_lang], '')  # 拡張子を削除
            num = file_num[1:].zfill(3) if file_num.startswith(('A', 'B', 'C')) else file_num.zfill(3)
            
            # 2つの言語のコードを収集
            entry = {"id": id_counter, "name": f"{file_num[0]}{num}"}
            codes_found = 0
            
            for lang, ext in languages.items():
                expected_file = f'answer_{file_num}{ext}'
                if lang in lang_files and expected_file in lang_files[lang]:
                    with open(lang_files[lang][expected_file], 'r', encoding='utf-8') as f:
                        code = f.read()
                        entry[lang.capitalize()] = code
                        codes_found += 1
            
            # 2つの言語のコードが揃っている場合のみ追加
            if codes_found == 2:
                result.append(entry)
                id_counter += 1
    
    return result

def main():
    # ベースディレクトリを指定（codes または editorial）
    base_dirs = [
        #"C:/Users/y_50u/Documents/GitHub/test_code_translation/data/kyopro-tessoku-main/codes",
        "C:/Users/y_50u/Documents/GitHub/test_code_translation/data/kyopro-tessoku-main/editorial"
    ]
    
    # 使用する2つの言語を指定
    languages = {
        'cpp': '.cpp',
        'python': '.py'
        # 他の組み合わせ例: 'cpp': '.cpp', 'java': '.java'
    }
    
    # 出力JSONファイルのパス
    output_json_path = "kyopro_editorial_cpp_py.json"
    
    # すべてのベースディレクトリからデータを収集
    all_json_data = []
    for base_dir in base_dirs:
        json_data = create_json_pairs(base_dir, languages)
        all_json_data.extend(json_data)
    
    # JSONファイルに保存
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_json_data, f, ensure_ascii=False, indent=2)
    
    print(f"Created {output_json_path} with {len(all_json_data)} entries")

if __name__ == "__main__":
    main()