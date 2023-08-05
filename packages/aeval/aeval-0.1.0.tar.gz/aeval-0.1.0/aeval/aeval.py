import ast
import random
import string
from typing import Any, Dict, Set, Type, Union


class DiscoverExposedAsync(ast.NodeVisitor):
    has_exposed_async: bool

    def __init__(self):
        self.has_exposed_async = False

    def __stop(*_):
        ...

    def __found(self, _):
        self.has_exposed_async = True

    visit_FunctionDef = __stop
    visit_AsyncFunctionDef = __stop
    visit_Await = __found
    visit_AsyncWith = __found
    visit_AsyncFor = __found


class DiscoverExposedNameStores(ast.NodeVisitor):
    names: Set[str]

    def __init__(self):
        self.names = set()


    def __add_fndef_name(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        self.names.add(node.name)

    def __add_import_name(self, node: Union[ast.Import, ast.ImportFrom]):
        for name in node.names:
            if name.asname:
                self.names.add(name.asname)
            else:
                self.names.add(name.name.split('.')[0])

    def visit_Name(self, node: ast.Name) -> Any:
        if isinstance(node.ctx, ast.Store):
            self.names.add(node.id)

    visit_Import = __add_import_name
    visit_ImportFrom = __add_import_name
    visit_FunctionDef = __add_fndef_name
    visit_AsyncFunctionDef = __add_fndef_name


def has_exposed_async(node: ast.AST) -> bool:
    visitor = DiscoverExposedAsync()
    visitor.visit(node)
    return visitor.has_exposed_async


def exposed_names_with_store(node: ast.AST) -> Set[str]:
    visitor = DiscoverExposedNameStores()
    visitor.visit(node)
    return visitor.names


async def aeval(code, globals, locals):
    node = ast.parse(code)
    if not node.body:
        return

    globals = globals if globals is not None else {}
    locals = locals if locals is not None else globals

    if has_exposed_async(node):
        thunk = _build_thunk(node, ast.AsyncFunctionDef, globals, locals)
        return await thunk()
    else:
        thunk = _build_thunk(node, ast.FunctionDef, globals, locals)
        return thunk()


_EMPTY_ARGS = ast.arguments(
    args=[],
    varargs=None,
    kwonlyargs=[],
    defaults=[],
    kw_defaults=[],
    posonlyargs=[],
)


def _build_thunk(node: ast.Module, fn_cls: Type, globals: Dict, locals: Dict):
    # Temporarily polluting the `locals` scope with the thunk function is not
    # ideal, but choosing an illegal name means that only very sneaky code will
    # be aware of it.
    thunkname = '-' + ''.join(random.sample(string.ascii_lowercase, 8))

    global_names = exposed_names_with_store(node)
    if global_names:
        node.body.insert(0, ast.Global(list(global_names)))

    if len(node.body) > 0 and isinstance(node.body[-1], ast.Expr):
        node.body[-1] = ast.Return(value=node.body[-1].value)

    mod = ast.parse('')
    mod.body=[
        fn_cls(
            name=thunkname,
            args=_EMPTY_ARGS,
            body=node.body,
            decorator_list=[],
            returns=None,
        )]
    ast.fix_missing_locations(mod)
    exec(compile(mod, '<string>', 'exec'), globals, locals)
    thunk = locals[thunkname]
    del locals[thunkname]
    return thunk


EXNEG_SIMPLE = ast.parse('''
for x in range(10):
    print(x)
''')

EXNEG_ASYNC_DEF = ast.parse('''
async def foo():
    await sleep(10)
''')

EXPOS_SIMPLE_AWAIT = ast.parse('''
await foo();
''')

EXPOS_ASSIGN_AWAIT = ast.parse('''
x = await foo();
''')

EXPOS_ASYNC_FOR = ast.parse('''
async for x in foo():
    print(x)
''')

EXPOS_ASYNC_WITH = ast.parse('''
async with foo() as f:
    print(f)
''')

EXPOS_AWAIT_IN_FOR = ast.parse('''
for x in range(10):
    await foo()
''')

EXPOS_AWAIT_IN_WITH = ast.parse('''
with foo():
    await bar()
''')
