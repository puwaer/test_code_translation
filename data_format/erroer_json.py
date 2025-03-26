import json

def create_json_array(input_file, output_file):
    # 入力ファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as f:
        # 各行を読み込んでリストに変換
        lines = f.readlines()
        # 各行をJSONオブジェクトとしてパース
        data = [json.loads(line.strip()) for line in lines if line.strip()]
    
    # 新しいJSONファイルを書き込む
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

# 使用例
if __name__ == "__main__":
    input_filename = "./data/backup_data/multilingual_valid.json"    # 入力ファイル名
    output_filename = "./data/backup_data/test.json"  # 出力ファイル名
    
    try:
        create_json_array(input_filename, output_filename)
        print(f"Successfully converted {input_filename} to {output_filename}")
    except FileNotFoundError:
        print("Input file not found!")
    except json.JSONDecodeError:
        print("Error decoding JSON!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")