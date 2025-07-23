from markitdown import MarkItDown
from langchain_google_genai import ChatGoogleGenerativeAI
import os

md = MarkItDown()
result = md.convert("invoice.pdf")

llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-2.0-flash",
    max_output_tokens=2048,
    temperature=0,
)

question = "What is the total amount on this invoice?"
prompt = f"{result.text_content}\n\nQuestion: {question}"

answer = llm.invoke(prompt)
print("Response:", answer.content)