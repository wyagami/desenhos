import streamlit as st
from together import Together
import requests
from PIL import Image
from io import BytesIO


with st.sidebar:
    st.sidebar.header("Desenhos para Colorir")
    st.sidebar.write("""
                                         
    - Caso tenha alguma idéia para publicarmos, envie uma mensagem para: 11-990000425 (Willian)
    - Contribua com qualquer valor para mantermos a pagina no ar. PIX (wpyagami@gmail.com)
    """)


# Título da aplicação
st.title("Gerador de Desenhos para Colorir")

# Campo para inserir a chave de API
APIK = st.secrets["together"]

# Campo para inserir o tema do desenho
tema = st.text_input("Tema do Desenho (ex: um pássaro voando entre nuvens):")

# Botão para gerar o desenho
if st.button("Gerar Desenho"):
    # Verifica se a chave de API e o tema foram fornecidos
    if APIK and tema:
        # Prompt ajustado para gerar um desenho em preto e branco adequado para colorir
        prompt = f"Crie uma imagem de desenho em preto e branco, com linhas finas e contornos bem definidos, adequada para ser colorida. O desenho deve representar {tema}. Certifique-se de que as áreas a serem pintadas sejam claras e distintas, facilitando o processo de colorir. O plano de fundo deve ser branco."
        
        try:
            # Inicializa o cliente da API com a chave fornecida
            client = Together(api_key=APIK)
            
            # Gera a imagem usando a API do Together
            response = client.images.generate(
                prompt=prompt,
                model="black-forest-labs/FLUX.1-schnell-Free",
                steps=4,
                width=1024,
                height=768,
                n=1
            )
            
            # Obtém a URL da imagem gerada e faz o download
            imurl = response.data[0].url
            my_res = requests.get(imurl)
            my_img = Image.open(BytesIO(my_res.content))
            
            # Exibe a imagem na interface
            st.image(my_img, caption="Desenho Gerado")
            
            # Campo para inserir o nome do arquivo PDF (opcional)
            savename = st.text_input("Nome do arquivo PDF (ex: desenho.pdf):", value="desenho.pdf")
            
            # Converte a imagem para PDF em memória
            pdf_bytes = BytesIO()
            my_img.save(pdf_bytes, format='PDF')
            pdf_bytes.seek(0)
            
            # Botão para baixar o PDF diretamente
            st.download_button(
                label="Baixar Desenho em PDF",
                data=pdf_bytes,
                file_name=savename if savename else "desenho.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            # Exibe mensagens de erro em caso de falha
            st.error(f"Ocorreu um erro: {e}")
            st.info("Verifique se sua chave de API é válida em https://api.together.ai/settings/api-keys")
    else:
        st.warning("Por favor, forneça a chave de API e o tema do desenho.")