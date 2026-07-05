from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv 
from langgraph.checkpoint.memory import MemorySaver
from langchain_openrouter import ChatOpenRouter
from langgraph.graph.message import add_messages


load_dotenv()


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatOpenRouter(
    model= 'poolside/laguna-xs-2.1:free'
)



def chat_node(state:ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}


check_pointer = MemorySaver()


graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatboat = graph.compile(checkpointer=check_pointer)

