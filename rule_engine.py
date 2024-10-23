import re
import operator

# AST Node class to represent rules
class ASTNode:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value     # For operand: condition like "age > 30"
        self.left = left       # Left child node (for operators)
        self.right = right     # Right child node (for operators)

# Function to tokenize rule strings
def tokenize(rule_string):
    token_pattern = r'(\bAND\b|\bOR\b|\bNOT\b|\(|\)|>|<|=|\w+|\'\w+\')'
    return re.findall(token_pattern, rule_string)

# Parse the token list into an AST
def parse(tokens):
    def parse_expression(index):
        stack = []
        while index < len(tokens):
            token = tokens[index]
            if token == '(':
                subtree, index = parse_expression(index + 1)
                stack.append(subtree)
            elif token == ')':
                return build_ast(stack), index
            elif token in ('AND', 'OR', 'NOT'):
                stack.append(token)
            else:
                condition = tokens[index:index + 3]  # e.g., ["age", ">", "30"]
                operand_node = ASTNode('operand', ' '.join(condition))
                stack.append(operand_node)
                index += 2  # Skip next two tokens
            index += 1
        return build_ast(stack), index

    def build_ast(components):
        if len(components) == 1:
            return components[0]
        
        left = components[0]
        index = 1
        while index < len(components) - 1:
            operator = components[index]
            right = components[index + 1]
            left = ASTNode('operator', operator, left, right)
            index += 2
        return left

    ast, _ = parse_expression(0)
    return ast

# Create a rule from a rule string
def create_rule(rule_string):
    tokens = tokenize(rule_string)
    return parse(tokens)

# Combine multiple AST rules
def combine_rules(rules):
    if len(rules) == 0:
        return None
    root = rules[0]
    for rule in rules[1:]:
        root = ASTNode('operator', 'AND', left=root, right=rule)
    return root

# Evaluate the rule against the provided data
def evaluate_rule(ast, data):
    if ast.type == 'operand':
        attribute, op, value = ast.value.split()
        value = int(value) if value.isdigit() else value.strip("'")
        attr_value = data.get(attribute)

        operators = {
            '>': operator.gt,
            '<': operator.lt,
            '=': operator.eq,
            '>=': operator.ge,
            '<=': operator.le
        }
        return operators[op](attr_value, value)
    
    elif ast.type == 'operator':
        if ast.value == 'NOT':
            return not evaluate_rule(ast.right, data)
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
    return False
