import streamlit as st


class ChatView:
    def __init__(self, controller, model):
        self.controller = controller
        self.model = model


    def render_main_page(self): 
        st.header('🍓 Preview Model', divider=True)

        messages = self.model.load_current_messages()
        
       
        with st.container():
            
            if not messages:
                if not st.session_state.get('current_conversation_file'):
                    st.info("👋 Bem-vindo! Selecione uma conversa na barra lateral ou comece uma nova. Digite sua mensagem abaixo para interagir.")
                else:
                    st.info("Esta conversa está vazia. Digite sua mensagem abaixo para adicionar as primeiras interações.")
            else:
                for message in messages:
                    with st.chat_message(message['role']):
                        st.markdown(message['content'])

        user_prompt = st.chat_input('Digite sua mensagem aqui...')
        if user_prompt:
            self.controller.handle_user_prompt(user_prompt)

    def render_sidebar(self): 

        with st.sidebar:
            tab_conversations, tab_settings = st.tabs(['🗣️ Conversas', '⚙️ Configurações'])
        

        with tab_conversations:
            self._render_conversations_tab() 
        
        with tab_settings:
            self._render_settings_tab() 

    def _render_conversations_tab(self):

        if st.button('➕ Nova Conversa',
                   on_click=self.controller.select_conversation,
                   args=('',), # Argumento para nova conversa
                   use_container_width=True,
                   key="new_conversation_button"): # Chave para robustez

            pass

        st.markdown("---") 

        conversations = self.model.list_conversations()
        
        if not conversations:
            st.caption("Nenhuma conversa anterior encontrada.")
        else:

            for file_name in conversations:
                try:
                    conversation_name_full = self.model.convert_from_file_name(file_name).capitalize()
                    # Ajuste no truncamento para acomodar ícones e evitar quebra de layout
                    display_name = (conversation_name_full[:22] + '...') if len(conversation_name_full) > 25 else conversation_name_full
                    
                    is_active = (file_name == self.model.get_current_conversation_file())
                    
                    col_name, col_delete = st.columns([0.8, 0.2]) # Proporção para nome e botão de exclusão

                    with col_name:
                        icon = "▶️" if is_active else ""
                        button_label = f"{icon}{display_name}"
                        button_type = "primary" if is_active else "secondary"

                        # Botão para selecionar a conversa
                        if st.button(button_label,
                                   on_click=self.controller.select_conversation,
                                   args=(file_name,),
                                   disabled=is_active,
                                   use_container_width=True,
                                   type=button_type,
                                   key=f"conv_btn_{file_name}"):
                            pass # Lógica no callback
                    
                    with col_delete:
                        # Popover para confirmação de exclusão
                        with st.popover("🗑️", help="Excluir esta conversa", use_container_width=True):
                            st.markdown(f"**Excluir '{display_name}'?**")
                            st.caption("Esta ação não pode ser desfeita.")
                            if st.button("Confirmar Exclusão", 
                                         type="primary", 
                                         use_container_width=True, 
                                         key=f"confirm_delete_btn_{file_name}"):
                                self.controller.delete_conversation(file_name)
                                st.toast(f"Conversa '{display_name}' excluída.", icon="🗑️")
                                st.rerun() # Atualiza a UI imediatamente
                except Exception as e:
                    st.error(f"Erro ao renderizar item de conversa.")
                    # Logar o erro para depuração no backend é uma boa prática
                    print(f"Erro ao renderizar item da lista de conversas {file_name}: {e}")


    def _render_settings_tab(self): # Corrigida a indentação
        st.subheader("🔧 Configuração do Modelo")
        
        current_model_in_state = self.model.get_selected_model()
        # Usar uma chave única para o text_input pode ajudar o Streamlit a gerenciar melhor o estado
        new_model_name_input = st.text_input(
            'Nome do Modelo:',
            value=current_model_in_state,
            placeholder="ex: gpt-4o, gpt-3.5-turbo",
            help="Insira o identificador exato do modelo que deseja usar (ex: gpt-4o).",
            key="model_name_input"
        )

        cleaned_new_model_name = new_model_name_input.strip()
        # Evita chamadas desnecessárias ao controller se o valor não mudou
        if cleaned_new_model_name and cleaned_new_model_name != current_model_in_state:
            self.controller.update_selected_model(cleaned_new_model_name)
            st.toast(f"Modelo atualizado para: {cleaned_new_model_name}", icon="🤖")

        st.markdown("---") # Divisor visual

        st.subheader("🔑 Configuração da Chave API")
        current_api_key = self.model.get_api_key()
        
        api_key_input = st.text_input(
            'Chave da API (API Key):',
            value=current_api_key,
            type="password", # Importante para ocultar a chave
            placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Sua chave de API é armazenada localmente e não será compartilhada.",
            key="api_key_input"
        )

        cleaned_api_key = api_key_input.strip()
        # Evita chamadas desnecessárias ao controller
        if cleaned_api_key != current_api_key:
            if cleaned_api_key: # Se uma nova chave foi inserida (não vazia)
                self.controller.update_api_key(cleaned_api_key)
                st.toast('Chave da API salva!', icon="✅")
            else: # Se a chave foi apagada
                self.controller.update_api_key('')
                st.toast('Chave da API removida.', icon="ℹ️")
