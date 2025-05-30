import pickle
import re
from pathlib import Path
from unidecode import unidecode
import streamlit as st

class ChatModel:
    def __init__(self):
        self.config_folder = Path(__file__).parent / 'configurations'
        self.config_folder.mkdir(exist_ok=True)
        self.messages_folder = Path(__file__).parent / 'messages'
        self.messages_folder.mkdir(exist_ok=True)
        self.filename_cache = {}

        self._initialize_session_state()

    def _initialize_session_state(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'current_conversation_file' not in st.session_state:
            st.session_state.current_conversation_file = ''
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = 'o4-mini-2025-04-16'
        if 'api_key' not in st.session_state:
            st.session_state.api_key = self._load_api_key()

    def get_messages(self):
        return st.session_state.messages

    def set_messages(self, messages):
        st.session_state.messages = messages

    def get_current_conversation_file(self):
        return st.session_state.current_conversation_file

    def set_current_conversation_file(self, file_name):
        st.session_state.current_conversation_file = file_name

    def get_selected_model(self):
        return st.session_state.selected_model

    def set_selected_model(self, model_name):
        st.session_state.selected_model = model_name

    def get_api_key(self):
        return st.session_state.api_key

    def set_api_key(self, key):
        st.session_state.api_key = key
        self._save_api_key(key)

    def convert_to_file_name(self, conversation_name):
        file_name = unidecode(conversation_name)
        file_name = re.sub(r'\W+', '', file_name).lower()
        return file_name

    def convert_from_file_name(self, file_name):
        if file_name not in self.filename_cache:
            conversation_name = self.load_messages_from_file(file_name, key='conversation_name')
            self.filename_cache[file_name] = conversation_name
        return self.filename_cache[file_name]

    def _get_conversation_name_from_messages(self, messages):
        for message in messages:
            if message['role'] == 'user':
                return message['content'][:30]
        return ''

    def save_conversation_messages(self, messages):
        if not messages:
            return False
        conversation_name = self._get_conversation_name_from_messages(messages)
        file_name = self.convert_to_file_name(conversation_name)
        data_to_save = {
            'conversation_name': conversation_name,
            'file_name': file_name,
            'messages': messages
        }
        with open(self.messages_folder / file_name, 'wb') as f:
            pickle.dump(data_to_save, f)
        return True

    def load_messages_from_file(self, file_name, key='messages'):
        with open(self.messages_folder / file_name, 'rb') as f:
            data = pickle.load(f)
        return data[key]

    def load_current_messages(self):
        current_messages = st.session_state.messages
        if not current_messages:
            return []

        conversation_name = self._get_conversation_name_from_messages(current_messages)
        file_name = self.convert_to_file_name(conversation_name)

        if (self.messages_folder / file_name).exists():
            with open(self.messages_folder / file_name, 'rb') as f:
                data = pickle.load(f)
            return data['messages']
        else:
            return [] # This case might happen if a new conversation is started but not yet saved.
        
    def delete_conversation_file(self, file_name_to_delete):
        try:
            file_path = self.messages_folder / file_name_to_delete
            if file_path.is_file():
                file_path.unlink()  # Exclui o arquivo

                if file_name_to_delete in self.filename_cache:
                    del self.filename_cache[file_name_to_delete]

                if st.session_state.get('current_conversation_file') == file_name_to_delete:
                    st.session_state.current_conversation_file = ''
                    st.session_state.messages = [] 
                return True
            else:
                print(f"Arquivo de conversa não encontrado para exclusão: {file_path}")
                return False
        except Exception as e:
            print(f"Erro ao excluir o arquivo da conversa {file_path}: {e}")
            return False

    def list_conversations(self):
        conversations = list(self.messages_folder.glob('*'))
        conversations.sort(key=lambda item: item.stat().st_mtime_ns, reverse=True)
        return [c.stem for c in conversations]

    def _save_api_key(self, key):
        with open(self.config_folder / 'api_key', 'wb') as f:
            pickle.dump(key, f)

    def _load_api_key(self):
        api_key_file = self.config_folder / 'api_key'
        if api_key_file.exists():
            with open(api_key_file, 'rb') as f:
                return pickle.load(f)
        else:
            return ''