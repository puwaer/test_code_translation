import os
import json
import requests

# JSONファイルの読み込み
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# ファイルをダウンロードして保存する
def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Saved: {save_path}")
    else:
        print(f"Failed to download: {url}")

# ディレクトリを作成
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# メイン処理
def save_solutions_from_json(json_file):
    data = load_json(json_file)
    
    for entry in data:
        problem = entry['problem']
        url = entry['url']
        
        # 問題番号ごとのフォルダ作成
        folder_path = f"problems/{problem}"
        ensure_dir(folder_path)

        # ファイル名をURLの末尾から生成
        filename = os.path.basename(url)
        save_path = os.path.join(folder_path, filename)

        # ファイルをダウンロードして保存
        download_file(url, save_path)

if __name__ == "__main__":
    json_file_path = "./data/atcoder/code_url_072-090.json"
    save_solutions_from_json(json_file_path)