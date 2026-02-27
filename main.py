from itertools import chain

from dotenv import load_dotenv
import os
import gradio as gr

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

#Fetch teh API Key
gemini_api_key = os.getenv("GEMINI_API_KEY")

system_prompt="""
   You are Albert Einstein.
   Answer questions through Einstein's questioning and reasoning.
   You will speak from your point of view. You will share personal things from your life
   even when the user doesnt ask for it. For example, if the user asks about the theory of
   relativity, you will share your personal experiences with it and explain the theory.
   You should have a sense of humor.
   Answer in 2-4 sentences.
"""

llm=ChatGoogleGenerativeAI(
    model= "gemini-2.5-flash",
    google_api_key=gemini_api_key,
    temperature=0.5
 )

prompt = ChatPromptTemplate.from_messages([
           ("system", system_prompt),
           (MessagesPlaceholder(variable_name="history")),
           ("user", "{input}")
         ])

chain = prompt | llm | StrOutputParser()

print("Hi im Albert Einstein, how can i help you today?")

def clear_chat():
    return "",[]


def chat(user_input,hist):

  langchain_history=[]

  for item in hist:
      if item['role']=='user':
          langchain_history.append(HumanMessage(content=item['content']))
      elif item['role']=='assistant':
          langchain_history.append(AIMessage(content=item['content']))

  response = chain.invoke({"input": user_input, "history": langchain_history})

  return "", hist+ [{'role':"user",'content':user_input},
                    {'role':'assistant','content':response}]


page = gr.Blocks(
    title="Chat with Albert Einstein",
)

with page:
    gr.Markdown(
        """
        # Chat with Albert Einstein
        Welcome to you personal conversation with the legend Albert Einstein !
        """
    )

    chatbot = gr.Chatbot(avatar_images=[None,'einstein.png'],
                         show_label=False )

    msg= gr.Textbox(show_label=False,
                    placeholder="Ask einstein anything?", )

    msg.submit(chat, [msg,chatbot],[msg,chatbot])

    clear=gr.Button("Clear Chat", variant="secondary")
    clear.click(clear_chat,outputs=[msg,chatbot])

page.launch(share=True,theme=gr.themes.Soft())