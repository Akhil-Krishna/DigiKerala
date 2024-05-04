import google.generativeai as genai
#rom prediction import personality_traits

genai.configure(api_key="AIzaSyCdjmY7jiH7U_Z7JBfgu-omA2rd3S7sG2g")
# proceed here for api key  https://makersuite.google.com/app/apikey

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
)

def chat(query):
    for _ in range(3):  # Retry up to 3 times
        try:
            response = model.generate_content([query])
            return response.text
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
    return "Sorry, I'm unable to assist at the moment."

def say(text):
    print(f"Luna: {text}")

def takeCommand():
    try:
        query = input("Enter details : ") + "select and display the number corresponding to the correct option from 1. Police Department 2. Telecommunication 3. National Informatics Centre 4. Consumer Cell 5. Local Administration"

        return query
    except Exception as e:
        return "Some Error Occurred. Sorry from Luna"

if __name__ == '__main__':
    query = takeCommand()
    response = chat(query)
    for i in response:
        if i.isdigit():
            deptnum=int(i)
    print(f"Luna: Department number : {deptnum} and response is {response}")
