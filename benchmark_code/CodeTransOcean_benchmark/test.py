from tree_sitter import Language, Parser
import tree_sitter_java

parser = Parser()
java_language = Language(tree_sitter_java.language())
parser.set_language(java_language)
print("set_language worked successfully!")


