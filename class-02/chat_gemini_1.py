# from google import genai
# from google.genai import types
import google.generativeai as genai



genai.configure(api_key='GOOGLE_API_KEY')

model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("why is the sky is blue?")
# response = client.models.generate_content(
#     model='gemini-2.0-flash-001', contents='why is the sky is blue'
# )
print(response.text)
