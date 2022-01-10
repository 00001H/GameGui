"""The modified AST literal_eval.
Internal module and subject to change.
Allows a few more operations(namely,addition,subtraction,multiplication,division and
floor divisions)."""
from _ast import *
from ast import parse,dump
def literal_eval(node_or_string):
    if isinstance(node_or_string, str):
        node_or_string = parse(node_or_string, mode='eval')
    if isinstance(node_or_string, Expression):
        node_or_string = node_or_string.body
    def _raise_malformed_node(node):
        raise ValueError(f'malformed node or string: {dump(node)}')
    def _convert_num(node):
        if not isinstance(node, Constant) or type(node.value) not in (int, float, complex):
            _raise_malformed_node(node)
        return node.value
    def _convert_signed_num(node):
        if isinstance(node, UnaryOp) and isinstance(node.op, (UAdd, USub)):
            operand = _convert_num(node.operand)
            if isinstance(node.op, UAdd):
                return + operand
            else:
                return - operand
        return _convert_num(node)
    def _convert(node):
        if isinstance(node, Constant):
            return node.value
        elif isinstance(node, Tuple):
            return tuple(map(_convert, node.elts))
        elif isinstance(node, List):
            return list(map(_convert, node.elts))
        elif isinstance(node, Set):
            return set(map(_convert, node.elts))
        elif isinstance(node, Dict):
            if len(node.keys) != len(node.values):
                _raise_malformed_node(node)
            return dict(zip(map(_convert, node.keys),
                            map(_convert, node.values)))
        elif isinstance(node, BinOp) and isinstance(node.op, (Add,Sub,Mult,Div,FloorDiv)):
            left = _convert(node.left)
            right = _convert(node.right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float, complex)):
                if isinstance(node.op,Add):
                    return left + right
                elif isinstance(node.op,Sub):
                    return left - right
                elif isinstance(node.op,Mult):
                    return left * right
                elif isinstance(node.op,Div):
                    return left / right
                return left // right
        return _convert_signed_num(node)
    return _convert(node_or_string)
