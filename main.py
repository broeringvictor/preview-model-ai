import streamlit as st # type: ignore

from view import ChatView
from controllers import ChatController
from model import ChatModel

def main():
    st.set_page_config(page_title='🍓 Chatbot', page_icon='🍓', layout='wide')
    chat_model = ChatModel()
    chat_controller = ChatController(chat_model)
    chat_view = ChatView(chat_controller, chat_model)

    # Correção aqui:
    chat_view.render_main_page()
    chat_view.render_sidebar()

if __name__ == '__main__':
    main()