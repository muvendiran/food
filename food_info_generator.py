import streamlit as st
from transformers import pipeline

# Load the pre-trained model for text generation
generator = pipeline("text-generation", model="gpt2")

def extract_info(generated_text, start, end, default="N/A"):
    """
    Extract information from the generated text between the specified start and end delimiters.
    """
    try:
        return generated_text.split(start)[1].split(end)[0].strip()
    except IndexError:
        return default

def generate_food_info(food_name):
    """
    Generate food information based on the given food name.
    """
    # Generate food information based on the given food name
    prompt = f"Food name: {food_name}\nIngredients:"
    generated_text = generator(prompt, max_length=200, num_return_sequences=1, temperature=0.7)[0]['generated_text']
    
    # Extract relevant information from the generated text
    info = {}
    info["ingredients"] = extract_info(generated_text, "Ingredients:", "Preparation time:")
    info["prep_time"] = extract_info(generated_text, "Preparation time:", "Cooking time:")
    info["cook_time"] = extract_info(generated_text, "Cooking time:", "Flavor profile:")
    info["flavor_profile"] = extract_info(generated_text, "Flavor profile:", "Course:")
    info["course"] = extract_info(generated_text, "Course:", "", "N/A")
    
    return info

def main():
    st.title("Indian Food Information Generator")
    
    # Input field for the food name
    food_name = st.text_input("Enter the name of the food:")
    
    # Button to generate food information
    if st.button("Generate"):
        if food_name:
            # Generate food information
            food_info = generate_food_info(food_name)
            
            # Display food information
            st.subheader("Food Information:")
            st.write("Name:", food_name)
            st.write("Ingredients:", food_info["ingredients"])
        

if __name__ == "__main__":
    main()
