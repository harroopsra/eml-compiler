import sympy as sp
from sympy import tan, sin, cos, log, exp, pi, E, Integer, Symbol, Rational, sympify, Pow, Add, Mul


class avg(sp.Function):
    """(x + y) / 2"""
    nargs = 2

class hypot(sp.Function):
    """sqrt(x^2 + y^2)"""
    nargs = 2

class sigma(sp.Function):
    """Logistic sigmoid"""
    nargs = 1

class square(sp.Function):
    nargs = 1

class inv(sp.Function):

    nargs = 1

def eml(a,b): return f"EML[{a},{b}]"
def eml_exp(x): return eml(x,"1")
def eml_e(): return eml("1","1")
def eml_ln(x): return eml("1",eml_exp(eml("1",x)))
def eml_sub(x,y): return eml(eml_ln(x),eml_exp(y))
def eml_zero(): return eml_ln("1")
def eml_neg(x): return eml_sub(eml_ln("1"),x)
def eml_add(x,y): return eml_sub(x,eml_neg(y))
def eml_inv(x): return eml_exp(eml_neg(eml_ln(x)))
def eml_mult(x,y): return eml_exp(eml_add(eml_ln(x),eml_ln(y)))
def eml_square(x): return eml_mult(x,x)
def eml_divide(x,y): return eml_mult(x,eml_inv(y))
def eml_one(): return "1"
def eml_two(): return eml_add("1", "1")
def eml_half(x): return eml_divide(x,eml_two())
def eml_avg(x,y): return eml_half(eml_add(x,y))
def eml_root(x): return eml_exp(eml_half(eml_ln(x)))
def eml_pow(x,y): return eml_exp(eml_mult(y, eml_ln(x)))
def eml_logarithm(x,y): return eml_divide(eml_ln(y),eml_ln(x)) 
def eml_pi(): return eml_root(eml_neg(eml_square(eml_ln(eml_neg(eml_one())))))
def eml_hypot(x,y): return eml_root(eml_add(eml_square(x),eml_square(y)))
def eml_sigmoid(x): return eml_inv(eml(eml_neg(x),eml_exp(eml_neg(eml_one()))))



def parse_math_expr(math_expr_string:str):
    math_expr_string = math_expr_string.strip()
    math_expr_string = math_expr_string.replace("[","(")
    math_expr_string = math_expr_string.replace("]",")")
    math_expr_string = math_expr_string.replace("^","**")

    local_dict = {
        'hypot': hypot,
        'avg': avg,
        'sigma': sigma,
        'exp':exp,
        'inv':inv,
        'square':square,
        'ln':log,
        'log':log,
        'pi':pi,
        'e':E
    }
    
    return sympify(math_expr_string,locals=local_dict)

def convert_to_eml(sympy_expr):

    if isinstance(sympy_expr, Symbol):
        return str(sympy_expr)

    if isinstance(sympy_expr, Integer):
        return eml_int(int(sympy_expr))
    if isinstance(sympy_expr, Rational):
        p, q = sympy_expr.p, sympy_expr.q
        top = eml_int(p)
        bottom = eml_int(q)
        return eml_divide(top,bottom)
    
    f = getattr(sympy_expr, 'func', None)
    
    if f is log:
        if len(sympy_expr.args) == 2:
            return eml_logarithm(convert_to_eml(sympy_expr.args[0]),convert_to_eml(sympy_expr.args[1]))
        return eml_ln(convert_to_eml(sympy_expr.args[0]))
    if f is exp:
        return eml_exp(convert_to_eml(sympy_expr.args[0]))

    if sympy_expr== E:
        return eml_e()
    if sympy_expr== pi:
        return eml_pi()

    if isinstance(sympy_expr, Pow):
        base, power = sympy_expr.as_base_exp()
        return eml_pow(convert_to_eml(base), convert_to_eml(power))
    
    if isinstance(sympy_expr, Mul):
        facs = list(sympy_expr.args)
        acc = convert_to_eml(facs[0])
        for g in facs[1:]:
            acc = eml_mult(acc, convert_to_eml(g))
        return acc

    if isinstance(sympy_expr, Add):
        terms = list(sympy_expr.args)
        acc = convert_to_eml(terms[0])
        for t in terms[1:]:
            acc = eml_add(acc, convert_to_eml(t))
        return acc

    if isinstance(sympy_expr, square):
        return eml_square(convert_to_eml(sympy_expr.args[0]))

    if isinstance(sympy_expr, inv):
        return eml_inv(convert_to_eml(sympy_expr.args[0]))

    if isinstance(sympy_expr, avg):
        return eml_avg(convert_to_eml(sympy_expr.args[0]), convert_to_eml(sympy_expr.args[1]))
    if isinstance(sympy_expr, hypot):
        return eml_hypot(convert_to_eml(sympy_expr.args[0]), convert_to_eml(sympy_expr.args[1]))
    if isinstance(sympy_expr, sigma):
        return eml_sigmoid(convert_to_eml(sympy_expr.args[0]))
    
    raise NotImplementedError(f"No EML rule for: {sympy_expr} (type {type(sympy_expr)})")

def eml_compile_from_string(s: str):
    expr = parse_math_expr(s)
    if callable(expr) or not hasattr(expr, "rewrite"):
        raise TypeError(
            f"Input did not parse as a symbolic expression: {s!r}. "
            "If you mean a function of x, write Sqrt[x] rather than Sqrt."
        )
    return convert_to_eml(expr)

def eml_int(n):
    if n==0: return eml_zero()
    if n==1: return eml_one()
    if n<0: return eml_neg(eml_int(-n))
    return eml_add(eml_int(n-1),eml_one()) 


def eml_calculate(x,y):
    return exp(x)-log(y)

if __name__ == "__main__":
    # Test: should produce valid EML strings
    tests = [
        "1",
        "2",
        "3",
        "x",
        "exp(x)",
        "ln(x)",
        "x + y",
        "x * y",
        "x^2",
        "avg(x,y)",
        "hypot(x,y)",
        "sigma(x)",
        "pi",
        "e",
    ]
    
    for t in tests:
        try:
            parsed = parse_math_expr(t)
            eml_str = convert_to_eml(parsed)
            print(f"{t:15} -> {eml_str[:80]}{'...' if len(eml_str)>80 else ''}")
        except Exception as e:
            print(f"{t:15} -> ERROR: {e}")

