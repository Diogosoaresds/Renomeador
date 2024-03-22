import os
import PyPDF2

def extrair_cnpj_nome(nome_arquivo):
    with open(nome_arquivo, 'rb') as arquivo_pdf:
        leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
        texto = ''
        for pagina in leitor_pdf.pages:
            texto += pagina.extract_text()
        linhas = texto.split('\n')
        if len(linhas) >= 5:
            dados_linha_5 = linhas[4]
            partes = dados_linha_5.split(' - ', 1)
            if len(partes) == 2:
                cnpj = partes[0].strip()
                nome_empresa = partes[1].strip()
                return cnpj, nome_empresa
    return None, None

def renomear_arquivos_com_cnpj_nome(diretorio):
    for nome_arquivo in os.listdir(diretorio):
        if nome_arquivo.endswith('.pdf'):
            caminho_completo = os.path.join(diretorio, nome_arquivo)
            cnpj, nome_empresa = extrair_cnpj_nome(caminho_completo)
            if cnpj and nome_empresa:
                # Substituindo o caractere ':' por um traço '-' no CNPJ
                cnpj_formatado = cnpj.replace(':', '').replace('.', '').replace('/', '').replace('-', '')
                novo_nome_arquivo = f"{nome_empresa} - {cnpj_formatado}.pdf"
                novo_caminho = os.path.join(diretorio, novo_nome_arquivo)
                os.rename(caminho_completo, novo_caminho)
                print(f"Arquivo renomeado: {nome_arquivo} -> {novo_nome_arquivo}")
            else:
                print(f"Não foi possível extrair CNPJ e nome da empresa do arquivo: {nome_arquivo}")

# Diretório onde estão os arquivos PDF
print("insira aqui o caminho onde os arquivos se encontram: ")
diretorio = input()
renomear_arquivos_com_cnpj_nome(diretorio)
print("Insira qualquer valor para encerrar o programa")
resposta = input()
