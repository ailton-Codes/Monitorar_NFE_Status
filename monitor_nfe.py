# Instalar as bibliotecas necessárias
# pip install schedule
# pip install beautifulsoup4
# pip install requests
# pip install pandas

import os  # Biblioteca para manipular o sistema de arquivos e diretórios
import requests  # Biblioteca para fazer requisições HTTP
from bs4 import BeautifulSoup  # Biblioteca para parsear HTML e XML
import pandas as pd  # Biblioteca para manipulação de dados em DataFrames
import schedule  # Biblioteca para agendar tarefas
import time  # Biblioteca para trabalhar com tempo e pausas
from datetime import datetime, timedelta  # Biblioteca para trabalhar com datas e horários
import logging  # Biblioteca para criar logs de eventos

# Configuração do sistema de logs para armazenar informações e erros
logging.basicConfig(
    level=logging.INFO,  # Define o nível de detalhe dos logs (pode ser DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define o formato da mensagem de log
    filename='logfile.log',  # Nome do arquivo onde os logs serão salvos
    filemode='a'  # Modo de abertura do arquivo (a = append, ou seja, adiciona novas mensagens no final do arquivo)
)

# Lista para armazenar os dados que serão coletados ao longo do tempo
todos_dados = []

# Função que mapeia o status das imagens para valores numéricos
def map_status(img):
    """Mapeia o status da imagem para um valor numérico."""
    if img == 'bola_verde_P.png':  # Se a imagem é verde, o serviço está OK
        return 2
    elif img == 'bola_amarela_P.png':  # Se a imagem é amarela, o serviço está com atenção
        return 1
    elif img == 'bola_vermelha_P.png':  # Se a imagem é vermelha, o serviço está com problemas
        return 0
    return None  # Se a imagem não é reconhecida, retorna None

# Função que faz a extração dos dados da página da NFE e processa esses dados
def extrair_dados():
    """Função para extrair e processar os dados."""
    url = "http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx?versao=0.00&tipoConteudo=P2c98tUpxrI="
    session = requests.Session()  # Cria uma sessão para fazer as requisições HTTP
    
    try:
        response = session.get(url)  # Faz a requisição à página
        response.raise_for_status()  # Verifica se houve algum erro na requisição (ex: página não encontrada)
        logging.info("Requisição bem-sucedida.")  # Loga que a requisição foi bem-sucedida
        
        soup = BeautifulSoup(response.content, 'html.parser')  # Converte o conteúdo da página em um objeto BeautifulSoup
        tabela = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_gdvDisponibilidade2'})  # Encontra a tabela específica na página
        linhas = tabela.find_all('tr')  # Extrai todas as linhas da tabela

        for linha in linhas[1:]:  # Ignora a primeira linha, que é o cabeçalho da tabela
            colunas = linha.find_all('td')  # Extrai todas as colunas de uma linha
            autorizador = colunas[0].text.strip()  # Extrai o nome do autorizador (primeira coluna)
            autorizacao4_img = colunas[1].find('img')['src'].split('/')[-1]  # Extrai o status da autorização (segunda coluna)
            status_servico_img = colunas[5].find('img')['src'].split('/')[-1]  # Extrai o status do serviço (sexta coluna)
            autorizacao4 = map_status(autorizacao4_img)  # Converte o status da autorização para um número
            status_servico = map_status(status_servico_img)  # Converte o status do serviço para um número
            # Armazena os dados em um dicionário e adiciona à lista
            todos_dados.append({
                'Timestamp': datetime.now(),
                'Autorizador': autorizador,
                'Autorizacao4': autorizacao4,
                'Status Serviço': status_servico
            })
        
        logging.info(f"Dados coletados às {datetime.now().strftime('%H:%M:%S')}")  # Loga o horário em que os dados foram coletados
        verificar_problemas()  # Chama a função para verificar se há algum problema nos serviços

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao fazer requisição: {e}")  # Loga um erro caso a requisição falhe
    
    except Exception as e:
        logging.critical(f"Erro inesperado: {e}")  # Loga um erro inesperado

# Função que verifica se algum serviço não está OK (ou seja, se não está verde)
def verificar_problemas():
    """Função para verificar se algum serviço está com problemas (não verde)."""
    # Filtra os dados para encontrar serviços que não estão OK
    problemas = [dado for dado in todos_dados if dado['Autorizacao4'] != 2 or dado['Status Serviço'] != 2]
    
    if problemas:  # Se houver algum serviço com problema
        logging.warning("Serviços com problemas encontrados.")  # Loga um aviso
        print("\nServiços com problemas:")  # Exibe a mensagem no console
        for problema in problemas:  # Para cada serviço com problema
            autorizador = problema['Autorizador']
            status_autorizacao4 = "OK" if problema['Autorizacao4'] == 2 else "Problema"
            status_servico = "OK" if problema['Status Serviço'] == 2 else "Problema"
            # Exibe no console o autorizador e o status do serviço
            print(f"- {autorizador}: Autorizacao4 = {status_autorizacao4}, Status Serviço = {status_servico}")
            logging.info(f"Problema identificado em {autorizador}: Autorizacao4 = {status_autorizacao4}, Status Serviço = {status_servico}")
    else:
        logging.info("Todos os serviços estão funcionando corretamente.")  # Loga que todos os serviços estão OK
        print("\nTodos os serviços estão funcionando corretamente.")  # Exibe a mensagem no console

# Função que será executada em intervalos de tempo definidos
def job():
    """Função agendada para ser executada a cada intervalo."""
    extrair_dados()  # Chama a função para extrair e processar os dados

# Função para salvar os dados coletados em um arquivo CSV
def salvar_csv():
    """Função para salvar os dados coletados em um arquivo CSV."""
    df = pd.DataFrame(todos_dados)  # Converte a lista de dados em um DataFrame
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")  # Cria uma string de timestamp para o nome do arquivo
    diretorio = os.path.dirname(os.path.abspath(__file__))  # Define o diretório onde o arquivo Python está
    nome_arquivo = os.path.join(diretorio, f"status_servicos_{timestamp_str}.csv")  # Cria o caminho completo para o arquivo
    
    try:
        df.to_csv(nome_arquivo, index=False)  # Salva o DataFrame em um arquivo CSV
        logging.info(f"Dados salvos em '{nome_arquivo}'")  # Loga que o arquivo foi salvo com sucesso
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo CSV: {e}")  # Loga um erro caso o salvamento falhe

# Define o tempo total de execução do script (neste caso, 8 horas)
tempo_final = datetime.now() + timedelta(hours=8)

# Agenda a execução do job a cada 30 minutos
schedule.every(30).minutes.do(job)

# Mantém o script rodando até o tempo final
while datetime.now() < tempo_final:
    schedule.run_pending()  # Executa as tarefas agendadas
    time.sleep(1)  # Pausa por 1 segundo antes de verificar novamente

# Salva os dados coletados em um CSV após o término do período de coleta
salvar_csv()
