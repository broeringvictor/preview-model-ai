import streamlit as st # type: ignore

from services.agent_service import AgentService


class ChatController:
    def __init__(self, model):
        self.model = model
        self.agent_service = AgentService() 
    def select_conversation(self, file_name):
        if file_name == '':
            self.model.set_messages([])
        else:
            messages = self.model.load_messages_from_file(file_name)
            self.model.set_messages(messages)
        self.model.set_current_conversation_file(file_name)

    def update_selected_model(self, model_name):
        self.model.set_selected_model(model_name)

    def update_api_key(self, api_key):
        self.model.set_api_key(api_key)



    def delete_conversation(self, file_name):
        success = self.model.delete_conversation_file(file_name)
        if not success:
            print(f"Falha ao excluir a conversa {file_name} pelo controller.")
        # A UI será atualizada pelo st.rerun() na View.

    def handle_user_prompt(self, prompt):
        if not self.model.get_api_key():
            st.error('Please add an API key in the settings tab.')
            return

        current_messages = self.model.get_messages()
        new_user_message = {'role': 'user', 'content': prompt}
        with st.chat_message(new_user_message['role']):
            st.markdown(new_user_message['content'])
        current_messages.append(new_user_message)

        with st.chat_message('assistant'):
            placeholder = st.empty()
            placeholder.markdown("▌")
            full_response = ''

            # This is the key part for agent replacement
            responses_generator = self.agent_service.get_agent_response(
                messages=current_messages,
                api_key=self.model.get_api_key(),
                model=self.model.get_selected_model(),
                stream=True
            )

            for response_chunk in responses_generator:
                full_response += response_chunk
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

        new_assistant_message = {'role': 'assistant', 'content': full_response}
        current_messages.append(new_assistant_message)

        self.model.set_messages(current_messages)
        self.model.save_conversation_messages(current_messages)