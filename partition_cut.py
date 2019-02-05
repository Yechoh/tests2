def cut(exp,vars): #vars is een dict van varname naar range
    for clause in exp:
        vars1=vars.copy()
        for (a,op,b) in clause:
            cut2((a,op,b),vars1)

def cut2((a,op,b),vars):
    if type(a)==str and type(b)==str:
        perpetrate((a,op,b),vars)
    elif type(b)==str:
        (aa,aop,ab)=a
        if aop in ["+"]:
            part_plus(aa,ab,op,b)

def part_plus(aa,ab,op,b):
    if b.isdigit():
        if ab.isdigit():
            if aa.isdigit():
                return


def reverse(op):
    if op == ">":
        return "<"
    if op == "<":
        return ">"
    if op == "=":
        return "="
    print("error")


def perpetrate((a,op,b),vars):
    if a.isdigit():
        if b.isdigit():
            return
        else:
            adjust((b,reverse(op),a),vars)
    else:
        if b.isdigit():
            adjust((a,op,b),vars)
        else:
            perp((a,op,b),vars)

def adjust((a,op,b),vars):
    (low, high) = vars[a]
    if op == ">":
        vars[a] = (max(low, b - 1), high)
    elif op == "<":
        vars[a] = (low, min(b, high))
    elif op == "=":
        vars[a] = (b, b + 1)
    else:
        print("error")

def perp((a,op,b),vars):
    (alow,ahigh)=vars[a]
    (blow,bhigh)=vars[b]
    if op == ">":
        vars[a]=(max(alow,blow+1),ahigh)
        vars[b]=(blow,min(ahigh,bhigh))
    elif op=="<":
        vars[a]=(alow,min(ahigh,bhigh))
        vars[b]=(max(alow+1,blow),bhigh)
    elif op=="=":
        vars[a]=(max(alow,blow),min(ahigh,bhigh))
        vars[b]=vars[a]
    else:
        print("error")
