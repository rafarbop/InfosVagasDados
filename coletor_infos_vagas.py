import streamlit as st
import json
import os
from datetime import datetime

# --- Configurações Iniciais ---
st.set_page_config(layout="wide")

# --- Título e Descrição do Projeto ---
st.title('Projeto: Coletor de Vagas de Dados')
st.markdown("""
Uma ferramenta para coletar e estruturar manualmente informações de vagas de emprego.
Carregue um arquivo JSON, adicione novas vagas e faça o download do arquivo atualizado.
""")

# --- Funções de Lógica ---
def split_field(text):
    """Normaliza campos de texto para listas, usando ; ou quebra de linha."""
    if not text:
        return []
    text = text.replace(';', '\n')
    return [item.strip() for item in text.splitlines() if item.strip()]

def reset_to_step1():
    """Reseta o estado para a etapa inicial de preenchimento do formulário."""
    st.session_state['vaga_temp'] = None
    st.session_state['campos_personalizados'] = 0
    st.rerun()
    
# --- Sidebar ---
st.sidebar.header("Configuração de Dados")

if 'dados_vagas' not in st.session_state:
    st.session_state['dados_vagas'] = None
    st.session_state['nome_arquivo'] = ''
if 'campos_personalizados' not in st.session_state:
    st.session_state['campos_personalizados'] = 0
if 'vaga_temp' not in st.session_state:
    st.session_state['vaga_temp'] = None

# Lógica de upload/início do zero
if st.session_state['dados_vagas'] is None:
    start_from_scratch = st.sidebar.checkbox("Iniciar com um arquivo vazio")
    st.sidebar.markdown("---")
    if start_from_scratch:
        if st.sidebar.button("Começar"):
            st.session_state['dados_vagas'] = []
            st.rerun()
    else:
        uploaded_file = st.sidebar.file_uploader("1. Carregar Arquivo JSON", type="json")
        if uploaded_file is not None:
            try:
                dados_carregados = json.load(uploaded_file)
                if isinstance(dados_carregados, list):
                    st.session_state['dados_vagas'] = dados_carregados
                    st.session_state['nome_arquivo'] = uploaded_file.name
                    st.sidebar.success(f"Arquivo '{uploaded_file.name}' carregado!")
                    st.rerun()
                else:
                    st.sidebar.error("Formato JSON inválido.")
            except json.JSONDecodeError:
                st.sidebar.error("Erro de leitura: Arquivo não é um JSON válido.")
else:
    st.sidebar.subheader("Status do Arquivo")
    st.sidebar.metric(label="Vagas Atualmente no Arquivo", value=len(st.session_state['dados_vagas']))

    if len(st.session_state['dados_vagas']) > 0:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Baixar Arquivo")
        data_atual = datetime.now().strftime("%Y%m%d")
        default_filename = f"infos_vagas_dados_{data_atual}.json"
        download_filename = st.sidebar.text_input("Nome do arquivo para download:", value=default_filename)
        json_para_download = json.dumps(st.session_state['dados_vagas'], indent=4, ensure_ascii=False).encode('utf-8')
        st.sidebar.download_button(
            label="Baixar Arquivo JSON Atualizado", data=json_para_download, file_name=download_filename, mime="application/json"
        )
    else:
        st.sidebar.info("Adicione vagas para habilitar o download.")

    st.sidebar.markdown("---")
    if st.sidebar.button("Limpar Dados (recomeçar)"):
        st.session_state['dados_vagas'] = None
        st.session_state['nome_arquivo'] = ''
        st.session_state['campos_personalizados'] = 0
        st.session_state['vaga_temp'] = None
        st.rerun()

# --- Conteúdo Principal (Fluxo em Etapas) ---
if st.session_state['dados_vagas'] is None:
    st.info("Para começar, use a barra lateral para carregar um arquivo JSON ou inicie com um arquivo vazio.")
else:
    # --- Etapa 1: Preencher o Formulário ---
    if st.session_state['vaga_temp'] is None:
        st.header("1. Preencha a Vaga")
        with st.form(key='vaga_form_step1'):
            col1, col2 = st.columns(2)
            with col1:
                titulo = st.text_input('Título da Vaga')
                empresa = st.text_input('Empresa')
            with col2:
                senioridade_opcoes = ["Estágio", "Junior", "Pleno", "Senior", "Arquiteto", "Outro/Não Informado"]
                senioridade_selecionada = st.selectbox("Senioridade", senioridade_opcoes)
                
                # Otimização da lógica de senioridade
                if senioridade_selecionada == "Outro/Não Informado":
                    senioridade_input = st.text_input('Especifique a Senioridade:')
                else:
                    senioridade_input = None
                
                forma_trabalho_opcoes = ["Presencial", "Híbrida", "Remoto", "Não Informado"]
                forma_trabalho = st.selectbox("Forma de Trabalho", forma_trabalho_opcoes)
            
            cidade_trabalho = st.text_input('Cidade de Trabalho')
            url_vaga = st.text_input('URL da Vaga')
            
            st.markdown("---")
            tab1, tab2 = st.tabs(["Informações da Vaga", "HTML da Vaga"])
            
            with tab1:
                st.markdown("Separe os itens por linha ou use `;`")
                requisitos = st.text_area('Requisitos')
                responsabilidades = st.text_area('Responsabilidades')
                beneficios = st.text_area('Benefícios')
            with tab2:
                html_vaga = st.text_area('Cole o HTML completo da vaga aqui:', height=300)

            submit_button = st.form_submit_button(label='Confirmar Dados')

        if submit_button:
            if not titulo and not empresa:
                st.warning("Preencha ao menos o título ou a empresa para adicionar a vaga.")
            else:
                final_senioridade = senioridade_selecionada if senioridade_selecionada != "Outro/Não Informado" else senioridade_input
                st.session_state['vaga_temp'] = {
                    'titulo': titulo,
                    'empresa': empresa,
                    'senioridade': final_senioridade,
                    'cidade_trabalho': cidade_trabalho,
                    'forma_trabalho': forma_trabalho,
                    'url_vaga': url_vaga,
                    'requisitos': split_field(requisitos),
                    'responsabilidades': split_field(responsabilidades),
                    'beneficios': split_field(beneficios),
                    'html_vaga': html_vaga
                }
                st.rerun()

    # --- Etapa 2: Visualizar e Adicionar Campos Personalizados ---
    elif st.session_state['vaga_temp'] is not None:
        st.header("2. Visualizar e Adicionar Campos")
        
        with st.expander("Pré-visualização do JSON da Vaga"):
            st.json(st.session_state['vaga_temp'])
        
        st.markdown("---")
        st.subheader("Adicionar Campos Personalizados")
        if st.button("Adicionar Mais um Campo"):
            st.session_state['campos_personalizados'] += 1
            st.rerun()

        with st.form(key="custom_fields_form"):
            for i in range(st.session_state['campos_personalizados']):
                col_key, col_value = st.columns(2)
                with col_key:
                    st.text_input(f"Nome do Campo {i+1}", key=f"key_{i}")
                with col_value:
                    st.text_input(f"Valor do Campo {i+1}", key=f"value_{i}")
            
            submit_custom = st.form_submit_button("Confirmar Campos Personalizados")

        if submit_custom:
            for i in range(st.session_state['campos_personalizados']):
                chave = st.session_state.get(f"key_{i}")
                valor = st.session_state.get(f"value_{i}")
                if chave and valor is not None:
                    st.session_state['vaga_temp'][chave] = valor
            st.rerun()


        st.markdown("---")

        # --- Etapa 3: Adicionar ao Arquivo Principal ---
        col_add_vaga_arquivo, col_back_btn = st.columns([1, 1])
        with col_add_vaga_arquivo:
            if st.button("Adicionar Vaga ao Arquivo Principal"):
                st.session_state['dados_vagas'].append(st.session_state['vaga_temp'])
                st.success("Vaga adicionada com sucesso ao arquivo!")
                reset_to_step1()
        with col_back_btn:
            if st.button("Voltar ao Formulário"):
                st.session_state['vaga_temp'] = None
                st.rerun()