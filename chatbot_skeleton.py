import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: ciao \n\nAI: Hi there! How can I help you today?\nHuman: Do you speak italian?\n\nAI: I do not speak Italian, but I can translate it for you if you'd like.\nHuman: Yes, i'd like translation\n",
  temperature=0.84,
  max_tokens=250,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)

print(response)