# Copyright (c) Microsoft Corporation. 
# Licensed under the MIT license.

from evaluator.CodeBLEU.parser import DFG_python, DFG_java, DFG_ruby, DFG_go, DFG_php, DFG_javascript, DFG_csharp
from evaluator.CodeBLEU.parser import (remove_comments_and_docstrings,
                                       tree_to_token_index,
                                       index_to_code_token,
                                       tree_to_variable_index)
from tree_sitter import Language, Parser
import tree_sitter_java  # Java用モジュール
import tree_sitter_python  # Python用モジュール
import os

root_dir = os.path.dirname(__file__)
dfg_function = {
    'python': DFG_python,
    'java': DFG_java,
    'ruby': DFG_ruby,
    'go': DFG_go,
    'php': DFG_php,
    'javascript': DFG_javascript,
    'c_sharp': DFG_csharp,
}

def calc_syntax_match(references, candidate, lang):
    return corpus_syntax_match([references], [candidate], lang)

def corpus_syntax_match(references, candidates, lang):
    # 言語に応じたLanguageオブジェクトを選択
    if lang == 'java':
        JAVA_LANGUAGE = Language(tree_sitter_java.language())
    elif lang == 'python':
        JAVA_LANGUAGE = Language(tree_sitter_python.language())
    else:
        raise ValueError(f"Unsupported language: {lang}")

    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)  # 最新APIを使用
    match_count = 0
    total_count = 0

    for i in range(len(candidates)):
        references_sample = references[i]
        candidate = candidates[i]
        for reference in references_sample:
            try:
                candidate = remove_comments_and_docstrings(candidate, lang)
            except:
                pass
            try:
                reference = remove_comments_and_docstrings(reference, lang)
            except:
                pass

            candidate_tree = parser.parse(bytes(candidate, 'utf8')).root_node
            reference_tree = parser.parse(bytes(reference, 'utf8')).root_node

            def get_all_sub_trees(root_node):
                node_stack = []
                sub_tree_list = []
                depth = 1
                node_stack.append([root_node, depth])
                while len(node_stack) != 0:
                    cur_node, cur_depth = node_stack.pop()
                    # S式の代わりに type と text を使用
                    node_repr = f"{cur_node.type}({cur_node.text.decode('utf8') if cur_node.text else ''})"
                    sub_tree_list.append([node_repr, cur_depth])
                    for child_node in cur_node.children:
                        if len(child_node.children) != 0:
                            depth = cur_depth + 1
                            node_stack.append([child_node, depth])
                return sub_tree_list

            cand_sub_trees = [x[0] for x in get_all_sub_trees(candidate_tree)]
            ref_sub_trees = get_all_sub_trees(reference_tree)

            for sub_tree, depth in ref_sub_trees:
                if sub_tree in cand_sub_trees:
                    match_count += 1
            total_count += len(ref_sub_trees)

    score = match_count / total_count if total_count > 0 else 0
    return score