import sympy

def sympify_interaction(i):
    mname = lambda s: s.replace(" ","_")
    
    if i.spec == "in:linear(f)->i":
        s = "%e*%s+%e" % (i.state.w,mname(i.name), i.state.bias)
    elif i.spec== "in:cat(c)->i":
        s = "categorical(x_%s)"%mname(i.name)

    elif i.spec=="cell:multiply(i,i)->i":
        s = "x0 * x1"
    elif i.spec=="cell:add(i,i)->i":
        s = "x0 + x1"
    elif i.spec=="cell:linear(i)->i":
        s = "%e*x0 + %f" %(i.state.w0, i.state.bias)
    elif i.spec=="cell:tanh(i)->i":
        s = "tanh(x0)"
    elif i.spec=="cell:inverse(i)->i":
        s = "1/x0"
    elif i.spec=="cell:log(i)->i":
        s = "log(x0)"
    elif i.spec=="cell:exp(i)->i":
        s = "exp(x0)"
    elif i.spec=="cell:sine(i)->i":
        s = "sin(x0)"
    elif i.spec=="cell:gaussian(i,i)->i":
        s = "exp(-(x0**2+x1**2))"
    elif i.spec=="cell:gaussian(i)->i":
        s = "exp(-(x0**2))"

    elif i.spec=="out:linear(i)->f":
        s = "%e*%e*x0+%e"%(i.state.scale, i.state.w, i.state.bias)
    elif i.spec=="out:lr(i)->b":
        s = "1/(1+exp(-(%e*x0+%e)))"%(i.state.w, i.state.bias)

    else:
        raise ValueError("Unsupported %s"%i.spec)
    return sympy.sympify(s)

def sympify_graph(g):
    exprs = [sympify_interaction(i) for i in g]
    for ix, i in enumerate(g):
        if len(i.sources)>0:
            exprs[ix] = exprs[ix].subs({"x0": exprs[i.sources[0]]})
        if len(i.sources)>1:
            exprs[ix] = exprs[ix].subs({"x1": exprs[i.sources[1]]})
    
    return exprs[-1]
        