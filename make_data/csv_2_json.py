import csv
import json
import re
import sys
import os

def convert_csv_to_json(file_path):
    # 結果を格納するリスト
    result = []
    
    # 問題番号を保持する変数
    current_problem = None
    
    try:
        # ファイルを開いて読み込み
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 行ごとに処理
        for line in lines:
            # 問題番号を検出（「問題 001」などの形式）
            problem_match = re.match(r'問題 (\d+)', line.strip())
            if problem_match:
                current_problem = problem_match.group(1)
                continue
                
            # データ行をカンマで分割
            fields = line.strip().split(',')
            
            # URLが含まれている行のみ処理（3番目のフィールドがリンク）
            if len(fields) >= 3 and fields[2].startswith('http'):
                entry = {
                    "problem": current_problem,
                    "url": fields[2]
                }
                result.append(entry)
                
        return result
    
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {str(e)}")
        sys.exit(1)

def main():

    csv_file_path = "./data/atcoder/code_url_072-090.csv"
    
    # ファイルの存在確認
    if not os.path.exists(csv_file_path):
        print(f"エラー: ファイル '{csv_file_path}' が見つかりません")
        sys.exit(1)
    
    # 変換実行
    result = convert_csv_to_json(csv_file_path)
    
    # JSON形式で出力（整形済み）
    json_output = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_output)
    
    # ファイルに保存（output.jsonとして）
    output_file = 'code_url_072-090.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_output)
    print(f"\n結果を '{output_file}' に保存しました")

if __name__ == "__main__":
    main()