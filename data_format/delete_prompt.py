import re
import json

def extract_code(text: str) -> str:
    text = re.sub(r"^.*?:", "", text)
    text = re.sub(r"\nDo not return.*", "", text)
    return text.strip()  # 余計な空白があれば削除

def process_json(input_filename: str, output_filename: str) -> None:
    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for entry in data:
        entry["input"] = extract_code(entry["input"])
    
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    input_filename = "./data/benchmark_data/multilingual_test_prompt_300.json"
    output_filename = "./data/benchmark_data/multilingual_test_300.json"
    process_json(input_filename, output_filename)
