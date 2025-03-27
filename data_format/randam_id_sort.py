import json
import random

def randam_id_sort_json(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("入力データがリスト形式ではありません")

    random.shuffle(data)

    # IDを1から順に振り直し、最後の2つのキーの順序をランダムに入れ替える
    for i, entry in enumerate(data, 1):
        if not isinstance(entry, dict):
            raise ValueError(f"エントリ {i} が辞書形式ではありません: {entry}")
        entry['id'] = i
        keys = list(entry.keys())
        lang_keys = keys[2:]  # "id" と "name" の後ろ
        if len(lang_keys) >= 2:
            last_two = lang_keys[-2:]
            key_value_pairs = {key: entry[key] for key in last_two}
            random.shuffle(last_two)
            for key in last_two:
                entry.pop(key)  
            for key in last_two:
                entry[key] = key_value_pairs[key]  

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"処理が完了しました。結果を {output_filename} に保存しました。")

if __name__ == "__main__":
    input_filename = "./data/train_data/base_train_data/kyopro_codes_cpp_java.json"    
    output_filename = "./data/train_data/base_train_data/test.json"  
    randam_id_sort_json(input_filename, output_filename)


