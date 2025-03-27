データ形式
jsonl
{"source": "Translate Python to Java: print('Hello')", "target": "System.out.println(\"Hello\");", "prediction": "System.out.println(\"Hello\");"}
{"source": "Translate Python to Java: x = 10", "target": "int x = 10;", "prediction": "int x = 10;"}
{"source": "Translate Python to Java: if x > 0: print('Positive')", "target": "if (x > 0) { System.out.println(\"Positive\"); }", "prediction": "if (x > 0) { System.out.println(\"Positive\"); }"}



実行例
python run_score.py --input_file ./benchmark_data/test_data.jsonl --source_names Python --target_names Java --codebleu
python run_score.py --input_file ./benchmark_data/test_data.json --source_names Python --target_names Java --codebleu

言語を指定する場合
--source_names Python → Python からの変換のみ評価


複数言語を指定する場合
python run_score.py --input_file test_data.jsonl --source_names Python,C++ --target_names Java,C#

全言語の評価を行う場合
python run_score.py --input_file ./benchmark_data/test_data.jsonl --codebleu

pip install tree-sitter tree-sitter-java tree-sitter-python



pip install tree-sitter==0.23.2 tree-sitter-java==0.23.5 tree-sitter-python==0.23.6