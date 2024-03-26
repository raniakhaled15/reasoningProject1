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


expression = "∀x∀y∃z(p(x)  ~r(y)) ⇒  q(z)"
print("Original expression:", expression)
print("Step 1(Eliminate implication):", eliminate_implication(expression))
