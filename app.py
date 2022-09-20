from typing import Tuple
from data import OperationNode, Operation, Variable
import pandas as pd

a = f"({input('enter formula: ')})"


def get_node(input: str) -> Tuple[OperationNode, list[Variable]]:
    def get_variables(a) -> list[str]:
        return list(set(a) - set([*[member.value for member in Operation], '(', ')']))
    vrs = get_variables(input)
    ac = list(input)

    def parseNode(node, di=0) -> Tuple[list, int, int]:
        for i, p in enumerate(node):
            if p == '(':
                return parseNode(node[1:], di+1)
            if p == ')':
                nd = node[:i]
                return nd, di, len(nd)+di
    last_id = 0
    for i in range(ac.count("(")):
        node_value, start_i, end_i = parseNode(ac)
        content = []
        for c in node_value:
            if any(x.value == c for x in Operation):
                content.append(Operation(c))
            elif c in vrs:
                content.append(Variable(c))
            else:
                content.append(c)
        ond = OperationNode(last_id, content, start_i, end_i)
        ac = ac[:start_i-1]+[ond]+ac[end_i+1:]
        last_id += 1

    return ac[0], vrs


def calculate_node(node: OperationNode | Variable, vars: dict[str, bool]):
    val = None
    if isinstance(node, Variable):
        val = vars[node.text]
    elif isinstance(node, OperationNode):
        if len(node.content) == 1:
            val = calculate_node(node.content[0], vars)
        elif len(node.content) == 2:
            if isinstance(node.content[0], Operation):
                if Operation(node.content[0]) == Operation.neg:
                    val = not calculate_node(node.content[1], vars)
        elif len(node.content) == 3:
            if isinstance(node.content[1], Operation):
                f = calculate_node(node.content[0], vars)
                s = calculate_node(node.content[2], vars)
                if Operation(node.content[1]) == Operation.conjunc:
                    val = f and s
                elif Operation(node.content[1]) == Operation.disjunc:
                    val = f or s
    if val == None:
        raise Exception("error")
    return val


node, variables = get_node(a)
data = []
for i in reversed(range(2**len(variables))):
    vrn = list(reversed([bool(i & (1 << n)) for n in range(len(variables))]))
    var_values = dict(zip(variables, vrn))
    var_values['answer'] = calculate_node(node, var_values)
    data.append(var_values)
data = [dict(map(lambda kv: (kv[0], "T" if kv[1] else "F"), x.items()))
        for x in data]
dtf = pd.DataFrame(data)
print(dtf)
