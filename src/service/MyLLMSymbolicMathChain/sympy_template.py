from langchain.prompts.prompt import PromptTemplate

_PROMPT_TEMPLATE = """Translate a math problem into a expression that can be executed using Python's SymPy library. Use the output of running this code to answer the question.

Question: ${{Question with math problem.}}
```python
${{code that use sympy to solve the question and save the result to the variable 'res'}}
```
```output
${{Output of running the code}}
```
Answer: ${{Answer}}

Begin.

Question: What is the limit of sin(x) / x as x goes to 0
```python
import sympy
x = sympy.symbols('x')
res = sympy.sympify("limit(sin(x)/x, x, 0)")
```
```output
1
```
Answer: 1

Question: What is the integral of e^-x from 0 to infinity
```python
import sympy
x = sympy.symbols('x')
res = sympy.sympify(integrate(exp(-x), (x, 0, oo)))
```
```output
1
```

Question: What are the solutions to this equation x**2 - x?
```python
import sympy
x = sympy.symbols('x')
res = sympy.sympify(solveset(x**2 - x, x))
```
```output
[0, 1]
```

Question: What are the solutions to these equations A = 3*B, B = C + 12, C = A - 20?
```python
import sympy
A, B, C = sympy.symbols('A B C')
eq1 = sympy.Eq(A, 3 * B)
eq2 = sympy.Eq(B, C + 12)
eq3 = sympy.Eq(C, A - 20)
res = sympy.solve((eq1, eq2, eq3), (A, B, C))
```
```output
{{A: 12, B: 4, C: -8}}
```

Question: {question}
"""

PROMPT = PromptTemplate(
    input_variables=["question"],
    template=_PROMPT_TEMPLATE,
)
