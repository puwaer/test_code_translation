import json
import subprocess
import os

def execute_code(code, language):
    """指定されたコードを言語に応じて実行し、結果を返す"""
    try:
        if language == "Python":
            with open("temp.py", "w") as f:
                f.write(code)
            result = subprocess.run(["python", "temp.py"], capture_output=True, text=True, timeout=5)
            os.remove("temp.py")
        
        elif language == "C":
            with open("temp.c", "w") as f:
                f.write(code)
            subprocess.run(["gcc", "temp.c", "-o", "temp"], check=True)
            result = subprocess.run(["./temp"], capture_output=True, text=True, timeout=5)
            os.remove("temp.c")
            os.remove("temp")
        
        elif language == "C++":
            with open("temp.cpp", "w") as f:
                f.write(code)
            subprocess.run(["g++", "temp.cpp", "-o", "temp"], check=True)
            result = subprocess.run(["./temp"], capture_output=True, text=True, timeout=5)
            os.remove("temp.cpp")
            os.remove("temp")
        
        elif language == "VB":
            with open("temp.vb", "w") as f:
                f.write(code)
            result = subprocess.run(["vbnc", "temp.vb"], capture_output=True, text=True, timeout=5)
            os.remove("temp.vb")
        
        elif language == "GO":
            with open("temp.go", "w") as f:
                f.write(code)
            result = subprocess.run(["go", "run", "temp.go"], capture_output=True, text=True, timeout=5)
            os.remove("temp.go")
        
        elif language == "PHP":
            with open("temp.php", "w") as f:
                f.write(code)
            result = subprocess.run(["php", "temp.php"], capture_output=True, text=True, timeout=5)
            os.remove("temp.php")
        
        elif language == "Java":
            with open("Temp.java", "w") as f:
                f.write(code)
            subprocess.run(["javac", "Temp.java"], check=True)
            result = subprocess.run(["java", "Temp"], capture_output=True, text=True, timeout=5)
            os.remove("Temp.java")
            os.remove("Temp.class")
        
        elif language == "C#":
            with open("temp.cs", "w") as f:
                f.write(code)
            subprocess.run(["csc", "temp.cs"], check=True)
            result = subprocess.run(["temp.exe"], capture_output=True, text=True, timeout=5)
            os.remove("temp.cs")
            os.remove("temp.exe")
        
        else:
            return "Unsupported language"

        return {
            "output": result.stdout,
            "error": result.stderr if result.stderr else None,
            "return_code": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    except Exception as e:
        return {"error": str(e)}

def process_json(input_file, output_file):
    # JSONファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 結果を格納するリスト
    results = []
    
    # 各エントリを処理
    for entry in data:
        code = entry["output"]
        language = entry["output_language"]
        
        # コードを実行
        execution_result = execute_code(code, language)
        
        # 結果を整形
        result_entry = {
            "id": entry["id"],
            "language": language,
            "input_code": code,
            "execution_result": execution_result
        }
        results.append(result_entry)
    
    # 結果をJSONファイルに書き込む
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

# 使用例
if __name__ == "__main__":
    input_file = "./data/benchmark_data/multilingual_test_prompt_300.json"  # 入力JSONファイル名
    output_file = "./benchmark_result/output.json"  # 出力JSONファイル名
    process_json(input_file, output_file)
    print(f"Results have been written to {output_file}")