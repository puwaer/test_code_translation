import tree_sitter
from tree_sitter import Language, Parser
import tree_sitter_java

print("tree-sitter path:", tree_sitter.__file__)
try:
    print("tree-sitter version:", tree_sitter.__version__)
except AttributeError:
    print("tree-sitter version: Not available")
parser = Parser()
print("Has set_language:", hasattr(parser, 'set_language'))

# さらに詳細な確認
java_language = Language(tree_sitter_java.language())
try:
    parser.set_language(java_language)
    print("set_language worked successfully!")
except AttributeError as e:
    print("set_language failed:", str(e))