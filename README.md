## Projeto: Coletor de Vagas de Dados

### Descrição

Este projeto é uma ferramenta em **Python** e **Streamlit** para auxiliar na coleta manual e organização de informações de vagas de emprego. O objetivo é gerar um conjunto de dados estruturado em formato **JSON** para análises futuras.

---

### Funcionalidades

- **Coleta de Dados**: Adicione informações como título, empresa, senioridade e requisitos.
- **Campos Flexíveis**: Campos de lista podem ser preenchidos por linha ou com `;`.
- **Armazenamento em JSON**: O aplicativo gera e permite o download de um arquivo JSON.

---

### Como Rodar a Aplicação

1.  **Instale as dependências**. No terminal, execute:
    ```
    uv pip install streamlit
    ```

2.  **Execute o script**. Navegue até a pasta do arquivo `coletor_infos_vagas.py` e execute:
    ```
    uv run streamlit run coletor_infos_vagas.py
    ```
    A aplicação será aberta automaticamente no seu navegador.

---

### Hospedando Online

A URL para acesso ao aplicativo hospedado no streamlit é: `https://share.streamlit.io/`

### Próximos Passos

- Extrair e tokenizar o texto de requisitos para análise de similaridade.
- Avaliar inclusão de analises e dashboard a serem visualisados com os recursos do streamlit
- Buscar possíveis APIs a serem usadas para captura dos dados vagase o streamlit seria para visulisar e análises
- Avaliar opção de salvar arquivo gerado em um bucket - para poder evoluir o processo de análise de vagas em ambiente cloud
