def eliminate_implication(expression):
    quantifiers = ""
    new_expression = ""
    skip = False
    for i in range(len(expression)):
        if skip:
            skip = False
            continue
        if expression[i] == '∃' or expression[i] == '∀':
            quantifiers += expression[i] + expression[i + 1]
            skip = True
        else:
            new_expression = expression[i:]
            break
    parts = new_expression.split("⇒ ")
    str1 = parts[0].strip()
    str2 = parts[1].strip()
    new_expression = quantifiers + "(~" + str1 + ') ∨ (' + str2 + ')'

    return new_expression


def apply_demorgan(expression):
    if '∧' in expression:
        parts = expression.split('∧')
        expression = '(~' + parts[0].strip() + ' ∨ (~' + parts[1].strip() + ')'

    elif '∨' in expression:
        parts = expression.split('∨')
        expression = '(~' + parts[0].strip() + ' ∧ (~' + parts[1].strip() + ')'
    return expression


def get_inner_part(idx, expression):
    stack = ['(']
    new_expression = ""
    while len(stack) != 0:
        # new_expression += expression[idx]
        if expression[idx] == '(':
            stack.append('(')
        elif expression[idx] == ')':
            stack.pop()
        new_expression += expression[idx]
        idx += 1
    return new_expression, idx


def move_negation_inward(sentence):
    """Apply DeMorgan's Law to move negation inward"""
    if "~(" in sentence:
        negation_index = sentence.index("~(")
        # closing_index = negation_index + sentence[negation_index:].index(")")
        inner_part, closing_index = get_inner_part(negation_index + 2, sentence)
        inner_part = apply_demorgan(inner_part)
        inner_part = move_negation_inward(inner_part)  # Recursively move inward
        return sentence[:negation_index] + inner_part + sentence[closing_index + 1:]
    return sentence


def remove_double_negation(expression):
    new_expression = expression.replace("~~", "")
    return new_expression


def replace_vars(idx, expression, new_variable):
    variable = expression[idx]
    new_expression = expression[idx:]
    expression = expression[0:idx]
    return expression + new_expression.replace(variable, new_variable)



def standrdize_variable_scope(expression):
    new_variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    variables = []
    counter = 0
    i = 0
    while i < len(expression):
        if(expression[i] == '∃' or expression[i] == '∀') and (expression[i+1] in variables) == 1:
            while new_variables[counter] in variables:
                counter += 1
            expression = replace_vars(i+1, expression, new_variables[counter])
        elif (expression[i] == '∃' or expression[i] == '∀') and (expression[i + 1] in variables) != 1:
            variables.append(expression[i+1])
        i += 1
    return expression


def prenex_form(expression):
    quantifiers = ""
    new_expression = ""
    skip = False
    for i in range(len(expression)):
        if skip:
            skip = False
            continue
        if expression[i] == '∃' or expression[i] == '∀':
            quantifiers += expression[i] + expression[i + 1]
            skip = True
        else:
            new_expression += expression[i]
    return quantifiers + new_expression


def skolemization(expression):
    if expression.find('∃') == -1:
        return expression
    i = 0
    count =1
    while i < len(expression):
        if expression[i] == '∃':
            expression = expression.replace(expression[i+1], "f"+str(count)+"(x)")
            count += 1
        i += 1
    return expression


def delete_universal_quantifiers(expression):
    idx = expression.find('∀')
    while idx != -1:
        expression = expression[:idx] + expression[idx+2:]
        idx = expression.find('∀')
    idx = expression.find('∃')
    while idx != -1:
        if expression[idx+1] == 'f':
            expression = expression[:idx] + expression[idx + 6:]
        else:
            expression = expression[:idx] + expression[idx + 2:]
        idx = expression.find('∃')

    return expression


expression = "∀x∀y(p(x) ∧ ~r(y)) ⇒  ∃xq(x)"
print("Original expression:", expression)
expression = eliminate_implication(expression)
print("Step 1(Eliminate implication):\n", expression)
expression = move_negation_inward(expression)
print("Step 2(Move negation inward (Demorgan Law))\n:", expression)
expression = remove_double_negation(expression)
print("Step 3(Remove double-not)\n:", expression)
expression = standrdize_variable_scope(expression)
print("Step 4(Standardize variable scope.)\n:", expression)
expression = prenex_form(expression)
print("Step 5(prenex form)\n:", expression)
expression = skolemization(expression)
print("Step 6(Skolemization)\n:", expression)
expression = delete_universal_quantifiers(expression)
print("Step 7(Eliminate universal quantifiers)\n:", expression)
