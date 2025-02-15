import streamlit as st
import os
import google.generativeai as genai
from fpdf import FPDF
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Recipe Generation Functionality
prompt = """You are a recipe generator. Given a list of available ingredients and the number of people to serve, generate a detailed, step-by-step recipe. The recipe should include clear instructions, approximate quantities, and cooking tips when applicable.

Ingredients: {ingredients}
Number of People: {num_people}

Recipe:"""

def generate_recipe(ingredients, num_people):
    model = genai.GenerativeModel("gemini-pro")
    full_prompt = prompt.format(ingredients=ingredients, num_people=num_people)
    response = model.generate_content(full_prompt)
    return response.text

def generate_pdf(recipe, ingredients, num_people):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt=f"Recipe for {num_people} People", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Ingredients: {ingredients}\n\n{recipe}")
    pdf_output_path = "recipe.pdf"
    pdf.output(pdf_output_path)
    return pdf_output_path

def recipe_generator_app():
    st.subheader("🍳 Recipe Generator")
    ingredients = st.text_input("Enter the ingredients you have (comma separated):")
    num_people = st.number_input("Enter number of people to serve:", min_value=1, step=1, value=1)

    if st.button("Generate Recipe"):
        if ingredients.strip():
            recipe = generate_recipe(ingredients, num_people)
            st.write(recipe)
            st.session_state['recipe'] = recipe
            st.session_state['ingredients'] = ingredients
            st.session_state['num_people'] = num_people
        else:
            st.warning("Please enter the ingredients you have.")

    if st.button("Download Recipe as PDF"):
        if 'recipe' in st.session_state:
            pdf_file = generate_pdf(
                st.session_state['recipe'],
                st.session_state['ingredients'],
                st.session_state['num_people']
            )
            with open(pdf_file, "rb") as file:
                st.download_button("Download PDF", file, file_name="recipe.pdf")
        else:
            st.warning("Generate a recipe first.")

# Ensure the Streamlit app runs
if __name__ == "__main__":
    st.set_page_config(page_title="Recipe Generator")
    st.title("🍳 Recipe Generator")
    recipe_generator_app()
