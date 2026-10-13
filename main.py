from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from compiler_v7 import eml_compile_from_string
import random

# Broad Categories: Integers, Trig functions, Polynomials, e, pi, exp(x), ln(x), Symbols


def interleave_expressions(list_1, list_2):
    return "".join(item for pair in zip(list_1, list_2) for item in pair) + list_1[-1]

def generate_wolfram_string():
    atoms = ["e","i","pi","1","x","y"]
    functions = ["square({})", "(inv{})", "exp({})", "ln({})", "sqrt({})"]
    operators = ["+", "-", "*", "/", "^"]
    terms = 3
    expressions= []
    operations = []
    for i in range(terms):
        component = random.choice(atoms+functions)
        if component in atoms:
            expressions.append(component)
        elif component in functions:
            pick_atom = random.choice(atoms)
            component = component.format(pick_atom)
            expressions.append(component)
        if i != terms-1:
            operation = random.choice(operators)
            operations.append(operation)
    
    final_exp = interleave_expressions(expressions,operations)

    return final_exp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local testing, '*' allows all. In production, use specific URLs.
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/expressions")
async def generate_expressions(count:int):
    reply = {}
    for i in range(count):
        expression = generate_wolfram_string()
        eml_version = eml_compile_from_string(expression)
        reply[expression] = eml_version
    return reply