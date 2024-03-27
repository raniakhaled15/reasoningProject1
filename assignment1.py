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
            new_expression += expression[i]
    idx = new_expression.find("⇒ ")
    while idx != -1:
        str1 = quantifiers + "~("
        str1 += new_expression[:idx]
        str2 = new_expression[idx + 1:]
        new_expression = str1 + '∨' + str2
        idx = new_expression.find("⇒ ")
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


def delete_universal_quantifiers(expression):
    expression = expression.replace("∀x", "")
    expression = expression.replace("∀y", "")
    expression = expression.replace("∀z", "")
    expression = expression.replace("∃x", "")
    expression = expression.replace("∃y", "")
    expression = expression.replace("∃z", "")
    return expression


expression = "∀x∀y(p(x) ∧ ~r(y)) ⇒  ∃zq(z)"
print("Original expression:", expression)
expression = eliminate_implication(expression)
print("Step 1 and 5(Eliminate implication):\n", expression)
expression = move_negation_inward(expression)
print("Step 2(Move negation inward (Demorgan Law))\n:", expression)
expression = remove_double_negation(expression)
print("Step 3(Remove double-not)\n:", expression)
expression = delete_universal_quantifiers(expression)
print("Step 7(Eliminate universal quantifiers)\n:", expression)
