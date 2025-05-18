import google.generativeai as genai
#from google.colab import userdata
from dotenv import load_dotenv
import os
load_dotenv()

# Получаем API-ключ из секретов Colab
api_key =  os.getenv("GOOGLE_API_KEY")

# Настройка библиотеки genai
genai.configure(api_key=api_key)

# Далее ваш код...

# List all available models
for m in genai.list_models():
  # Print models that support the generateContent method
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)