import json
import os
import requests
import sys
from urllib.parse import urlparse

def get_raw_url(url):
    """URLをrawファイルのURLに変換"""
    parsed_url = urlparse(url)
    
    # GitHubの場合
    if 'github.com' in url and '/blob/' in url:
        return url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    
    # GitLabの場合
    elif 'gitlab.com' in url and '/-/blob/' in url:
        raw_url = url.replace('/-/blob/', '/-/raw/')
        return raw_url
    
    # Gistの場合
    elif 'gist.github.com' in url:
        gist_id = parsed_url.path.split('/')[-1]
        return f"https://gist.githubusercontent.com/raw/{gist_id}"
    
    # その他の場合はそのまま返す
    return url

def has_valid_extension(url):
    """URLが有効なプログラムファイル拡張子を持つかチェック"""
    valid_extensions = {'.cpp', '.py', '.cr', '.go', '.rs', '.rb', '.kn'}
    path = urlparse(url).path
    return any(path.endswith(ext) for ext in valid_extensions)

def download_and_save(json_file_path, output_base_path="./"):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"エラー: {json_file_path} が見つかりません")
        return
    except json.JSONDecodeError:
        print("エラー: JSONファイルの形式が正しくありません")
        return

    for entry in data:
        problem_num = entry['problem']
        url = entry['url']
        
        # 有効な拡張子がない場合はスキップ
        if not has_valid_extension(url):
            print(f"スキップ: {url} は有効なプログラムファイル拡張子を持っていません")
            continue
        
        # raw URLに変換
        raw_url = get_raw_url(url)
        
        # 問題番号ごとのフォルダ作成（output_base_pathを使用）
        folder_name = os.path.join(output_base_path, f"problem_{problem_num}")
        os.makedirs(folder_name, exist_ok=True)
        
        # ファイル名を拡張子から決定
        parsed_url = urlparse(raw_url)
        path = parsed_url.path
        filename = os.path.basename(path)
        
        # 拡張子に基づいてファイル名を調整
        if not filename or '.' not in filename:
            filename = "code"
            if raw_url.endswith('.cpp'):
                filename += '.cpp'
            elif raw_url.endswith('.py'):
                filename += '.py'
            elif raw_url.endswith('.cr'):
                filename += '.cr'
            elif raw_url.endswith('.go'):
                filename += '.go'
            elif raw_url.endswith('.rs'):
                filename += '.rs'
            elif raw_url.endswith('.rb'):
                filename += '.rb'
            elif raw_url.endswith('.kn'):
                filename += '.kn'
            else:
                filename += '.txt'
        
        file_path = os.path.join(folder_name, filename)
        
        # ファイルのダウンロード
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(raw_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # テキストがプログラムコードであることを確認
            content = response.text
            if '<!DOCTYPE html>' not in content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"ダウンロード完了: {file_path}")
            else:
                print(f"スキップ: {url} はHTMLファイルです")
                
        except requests.RequestException as e:
            print(f"ダウンロード失敗 {url}: {str(e)}")

if __name__ == "__main__":
    json_file_path = "./data/atcoder/url_data/code_url_001-023.json"
    output_base_path = "./data/atcoder/code" 
    download_and_save(json_file_path, output_base_path)