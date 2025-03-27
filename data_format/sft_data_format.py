import json

def detect_languages(item):
    """JSONアイテムから存在する言語ペアを検出"""
    supported_languages = ["C", "C++", "PHP", "Java", "Python", "C#", "Go", "VB", "JavaScript", "TypeScript", "Ruby", "Swift", "Kotlin", "Rust", "Dart", "Cpp"]
    languages = [lang for lang in supported_languages if lang in item]
    if len(languages) != 2:
        raise ValueError(f"Expected exactly 2 languages, but found {len(languages)}: {languages}")
    return languages[0], languages[1]  # 最初の言語をinput、2番目をoutputと仮定

def transform_json(input_data):
    id = 1
    result = []
    for item in input_data:
        try:
            input_lang, output_lang = detect_languages(item)
            new_item = {
                "id": str(id),
                "input": f"Translate {input_lang} to {output_lang}:{item[input_lang]}\nDo not return anything including notes and the like except for one translated {output_lang} code.",
                "output": item[output_lang],
                "input_language": input_lang,
                "output_language": output_lang
            }
            result.append(new_item)
            id += 1
        except ValueError as e:
            print(f"Skipping item due to error: {e}, item: {item}")
            continue
    return result

if __name__ == "__main__":
    input_filename = "./data/train_data/base_train_data/multilingual_train_and_kyopro.json"    
    output_filename = "./data/train_data/format_train_data/multilingual_train_and_kyopro_sft.json"  
    #input_filename = "./data/benchmark_data/multilingual_test_fix.json"    
    #output_filename = "./data/benchmark_data/multilingual_test_prompt.json"  
    
    # 入力ファイルの読み込み
    with open(input_filename, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    try:
        # JSONデータの変換
        transformed_data = transform_json(input_data)
        
        # 出力ファイルへの書き込み
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, indent=2, ensure_ascii=False)
        print("Conversion completed successfully")
    except ValueError as e:
        print(f"Error: {e}")
        print("Problematic input data:", json.dumps(input_data, indent=2, ensure_ascii=False))


