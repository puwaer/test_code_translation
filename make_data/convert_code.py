import os
import json

# フォルダパスを指定
base_path = "C:/Users/y_50u/Documents/GitHub/test_code_translation/data/kyopro-tessoku-main/editorial"
output_file = "code_pairs.json"

# 結果を格納するリスト
code_pairs = []
id_counter = 1

# 各章ごとに探索
for root, dirs, files in os.walk(base_path):
    cpp_files = [f for f in files if f.endswith(".cpp")]
    python_files = [f for f in files if f.endswith(".py")]

    # C++とPythonのファイルをペアにする
    for cpp_file in cpp_files:
        base_name = os.path.splitext(cpp_file)[0]
        corresponding_py = f"{base_name}.py"

        if corresponding_py in python_files:
            with open(os.path.join(root, cpp_file), "r", encoding="utf-8") as cpp_code:
                cpp_content = cpp_code.read()
            with open(os.path.join(root, corresponding_py), "r", encoding="utf-8") as py_code:
                py_content = py_code.read()

            # JSONデータを追加
            code_pairs.append({
                "id": id_counter,
                "name": base_name,
                "C++": cpp_content,
                "Python": py_content
            })
            id_counter += 1

# JSONファイルに書き出し
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(code_pairs, json_file, ensure_ascii=False, indent=2)

print(f"{output_file} に書き出しました")
