

# this has to be in a seperate file, as the import from _ast interferes with
# defintions/imports in oitnb

import sys

# for _package/pon parsing
from _ast import *  # NOQA
from ast import parse

if sys.version_info >= (3, 8):
    from ast import Str, Num, Bytes, NameConstant  # NOQA

def literal_eval(node_or_string):
    """
    Safely evaluate an expression node or a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, bytes, numbers, tuples, lists, dicts,
    sets, booleans, and None.
    """
    _safe_names = {'None': None, 'True': True, 'False': False}
    if isinstance(node_or_string, str):
        node_or_string = parse(node_or_string, mode='eval')
    if isinstance(node_or_string, Expression):
        node_or_string = node_or_string.body
    else:
        raise TypeError("only string or AST nodes supported")

    def _convert(node):
        if isinstance(node, Str):
            if sys.version_info < (3,):
                return node.s.decode('utf-8')
            return node.s
        elif isinstance(node, Bytes):
            return node.s
        elif isinstance(node, Num):
            return node.n
        elif isinstance(node, Tuple):
            return tuple(map(_convert, node.elts))
        elif isinstance(node, List):
            return list(map(_convert, node.elts))
        elif isinstance(node, Set):
            return set(map(_convert, node.elts))
        elif isinstance(node, Dict):
            return dict((_convert(k), _convert(v)) for k, v
                        in zip(node.keys, node.values))
        elif isinstance(node, NameConstant):
            return node.value
        elif sys.version_info < (3, 4) and isinstance(node, Name):
            if node.id in _safe_names:
                return _safe_names[node.id]
        elif isinstance(node, UnaryOp) and \
             isinstance(node.op, (UAdd, USub)) and \
             isinstance(node.operand, (Num, UnaryOp, BinOp)):  # NOQA
            operand = _convert(node.operand)
            if isinstance(node.op, UAdd):
                return + operand
            else:
                return - operand
        elif isinstance(node, BinOp) and \
             isinstance(node.op, (Add, Sub)) and \
             isinstance(node.right, (Num, UnaryOp, BinOp)) and \
             isinstance(node.left, (Num, UnaryOp, BinOp)):  # NOQA
            left = _convert(node.left)
            right = _convert(node.right)
            if isinstance(node.op, Add):
                return left + right
            else:
                return left - right
        elif isinstance(node, Call):
            func_id = getattr(node.func, 'id', None)
            if func_id == 'dict':
                return dict((k.arg, _convert(k.value)) for k in node.keywords)
            elif func_id == 'set':
                return set(_convert(node.args[0]))
            elif func_id == 'date':
                return datetime.date(*[_convert(k) for k in node.args])
            elif func_id == 'datetime':
                return datetime.datetime(*[_convert(k) for k in node.args])
        err = SyntaxError('malformed node or string: ' + repr(node))
        err.filename = '<string>'
        err.lineno = node.lineno
        err.offset = node.col_offset
        err.text = repr(node)
        err.node = node
        raise err

    return _convert(node_or_string)


# parses python ( "= dict( )" ) or ( "= {" )
def _package_data_parser(path):
    data = {}
    with path.open(encoding='utf-8') as fp:
        parsing = False
        lines = []
        for line in fp.readlines():
            if line.startswith(u'_package_data'):
                if 'dict(' in line:
                    parsing = 'python'
                    lines.append(u'dict(\n')
                elif line.endswith(u'= {\n'):
                    parsing = 'python'
                    lines.append(u'{\n')
                else:
                    raise NotImplementedError
                continue
            if not parsing:
                continue
            if parsing == 'python':
                if line.startswith(u')') or line.startswith(u'}'):
                    lines.append(line)
                    try:
                        data = literal_eval(u''.join(lines))
                    except SyntaxError as e:
                        context = 2
                        from_line = e.lineno - (context + 1)
                        to_line = e.lineno + (context - 1)
                        w = len(str(to_line))
                        for index, line in enumerate(lines):
                            if from_line <= index <= to_line:
                                print(u"{0:{1}}: {2}".format(index, w, line).encode('utf-8'),
                                      end=u'')
                                if index == e.lineno - 1:
                                    print(u"{0:{1}}  {2}^--- {3}".format(
                                        u' ', w, u' ' * e.offset, e.node))
                        raise
                    break
                lines.append(line)
            else:
                raise NotImplementedError
    return data
