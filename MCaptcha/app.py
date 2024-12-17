import streamlit as st
from captcha_generator import generate_expression, generate_captcha_image
from expression_solver import simulate_ocr, step_by_step_solution

# Title
st.title("Mathematical CAPTCHA Solver")
st.write("CAPTCHA system with OCR-based solving and step-by-step solutions.")

# select difficulty and number of operators
difficulty = st.selectbox("Select Difficulty:", ["easy", "medium", "hard"])
num_operators = st.slider("Number of Operators:", 1, 5, 2)

# Generate CAPTCHA button
if st.button("Generate CAPTCHA"):
    # Step 1: Generate expression
    expression = generate_expression(difficulty, num_operators)
    st.session_state["expression"] = expression  # Store the original expression

    # Step 2: Generate CAPTCHA image
    image_path = "static/captcha.png"
    generate_captcha_image(expression, image_path)
    st.session_state["image_path"] = image_path

    # Step 3: Simulate OCR
    ocr_parsed = simulate_ocr(image_path)
    st.session_state["ocr_parsed"] = ocr_parsed

    # Solve expression for comparison
    result, steps = step_by_step_solution(ocr_parsed)
    st.session_state["correct_result"] = result

    # Display CAPTCHA image
    st.image(image_path, caption="Solve this CAPTCHA", use_container_width=False)

# User input for validation
if "correct_result" in st.session_state:
    user_answer = st.text_input("Enter your answer:")

    if st.button("Submit Answer"):
        try:
            user_input = float(user_answer)
            # Use the original expression for step-by-step solution
            correct_result, steps = step_by_step_solution(st.session_state["expression"])

            if abs(user_input - correct_result) < 1e-6:  # Allow minor precision errors
                st.success("✅ Correct Answer!")
                st.write("### Step-by-Step Solution:")
                for step in steps:
                    st.write(step)
            else:
                st.error("❌ Incorrect Answer! Generating a new CAPTCHA.")
                st.session_state.pop("correct_result", None)  # Reset state
        except ValueError:
            st.error("❌ Invalid input. Please enter a numeric value.")