import json

def normalize_keys(data):
    for item in data:
        if "Cpp" in item:
            item["C++"] = item.pop("Cpp")
    return data

if __name__ == "__main__":
    input_filename = "./data/train_data/base_train_data/multilingual_train_and_kyopro.json"    
    output_filename = "./data/train_data/base_train_data/multilingual_train_and_kyopro.json"    
    
    # ファイルの読み込み
    with open(input_filename, "r", encoding="utf-8") as infile:
        data = json.load(infile)
    
    # キーの統一
    normalized_data = normalize_keys(data)
    
    # ファイルの書き出し
    with open(output_filename, "w", encoding="utf-8") as outfile:
        json.dump(normalized_data, outfile, indent=2, ensure_ascii=False)
    
    print(f"Processed data saved to {output_filename}")