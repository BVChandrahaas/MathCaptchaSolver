import random
from PIL import Image, ImageDraw, ImageFont

# defining the possible mathematical operators
OPERATORS = ['+', '-', '*', '/']

# generating a random number based on the difficulty level
def generate_number(difficulty):
    if difficulty == 'easy':
        return random.randint(1, 10)
    elif difficulty == 'medium':
        return random.randint(1, 50)
    else:  # hard
        return random.randint(1, 100)

# generating a random operator for the expression
def generate_operator():
    return random.choice(OPERATORS)

# generating a mathematical expression using above functions
def generate_expression(difficulty, num_operators):
    expression = str(generate_number(difficulty))
    for _ in range(num_operators):
        operator = generate_operator()
        expression += f" {operator} {generate_number(difficulty)}"
    return expression

# generating and saving the CAPTCHA image
def generate_captcha_image(expression, image_path="static/captcha.png"):
    img = Image.new("RGB", (400, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 35)
    draw.text((10, 30), expression, fill=(0, 0, 0), font=font)
    img.save(image_path)
