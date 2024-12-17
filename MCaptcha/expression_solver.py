from PIL import Image
import pytesseract

class ExpressionEvaluator:
    def __init__(self):
        self.operators = set(['+', '-', '*', '/'])
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        self.steps = []

    def is_operator(self, c):
        return c in self.operators

    def apply_operator(self, a, b, operator):
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            return a / b
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def evaluate(self, expression):
        # converting the infix expression to postfix expression
        postfix = self.infix_to_postfix(expression)
        # evaluating the postfix expression
        result = self.evaluate_postfix(postfix)
        return result, self.steps

    def infix_to_postfix(self, expression):
        output = []
        stack = []
        tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()

        for token in tokens:
            if token.isnumeric():  
                output.append(float(token))
            elif token == '(':  
                stack.append(token)
            elif token == ')': 
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  
            elif self.is_operator(token): 
                while (stack and stack[-1] != '(' and
                       self.precedence[token] <= self.precedence[stack[-1]]):
                    output.append(stack.pop())
                stack.append(token)

        while stack:  
            output.append(stack.pop())

        return output

    def evaluate_postfix(self, expression):
        stack = []
        for token in expression:
            if isinstance(token, float):  
                stack.append(token)
            else:  
                b = stack.pop()  
                a = stack.pop()
                result = self.apply_operator(a, b, token)
                self.steps.append(f"{a} {token} {b} = {result}")  
                stack.append(result)  
        return stack[0]  

# using tesseract ocr to parse the string
def simulate_ocr(image_path):
    
    try:
        text = pytesseract.image_to_string(Image.open(image_path)).strip()
        return text
    except Exception as e:
        return f"Error in OCR: {e}"

# solving the function and returning step-by-step solution
def step_by_step_solution(exp):
    evaluator = ExpressionEvaluator()
    try:
        result, steps = evaluator.evaluate(exp)
        return result, steps
    except Exception as e:
        return None, [f"Error: {e}"]
