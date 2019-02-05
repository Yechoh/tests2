def to_cnf_relop(a,op,b):
    global temp_ands
    queue=[(a,op,b)]
    while queue!=[]:
        (a,op,b)=queue.pop(0)
        if op in ["and","or","->","<->"]:
            queue+=[a,b]
        elif op =="not":
            queue.append(a)
        elif op in [">","<",">=","<="]:
            (aa,aop,ab)=a
            temp_ands=[]
            queue+=to_relop((a,op,b))
        queue.pop(0)

def constant(a):
    return type(a)==str and a.isdigit()

def variable(a):
    return type(a)==str and not a.isdigit()

def reverse(op):
    pass

temp_ands=[]

def to_relop((a,op,b),left):
    global temp_ands
    if left:
        (b,op,a)=to_relop((b,reverse(op),a),False)
        op=reverse(op)
    if constant(a) or variable(a):
        return (a,op,b)
    (aa,aop,ab)=a
    if aop in ["+","*"]:
        (aa,op,b)=to_relop((aa,op,b),False)
        (ab,op,b)=to_relop((ab,op,b),False)
        return ((aa,aop,ab),op,b)
    elif aop=="-":
        (aa,op,ab) = to_relop((aa,op,ab),True)
        return (aa,op,(b,"+",ab))
    elif aop=="/":
        temp_ands.append(to_relop((ab,"==","0"),False))
        (aa, op, ab) = to_relop((aa, op, ab), True)
        return (aa,op,(b,"*",ab))
    elif aop=="%":
        
