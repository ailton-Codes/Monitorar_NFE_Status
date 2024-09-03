# Monitoramento de Serviços de Nota Fiscal Eletrônica (NFE)

## Projeto de Monitoramento Automático dos Serviços NFE

**Elaborado por:**  
Ailton Daniel Ferreira de Lima

**Data de Criação:**  
Agosto de 2024

---

## Descrição do Projeto

Este projeto visa criar uma solução automatizada para monitorar e registrar o status dos serviços de emissão de Nota Fiscal Eletrônica (NFE) oferecidos pela Secretaria da Fazenda. Através de um script em Python, os dados são coletados regularmente, verificados quanto à disponibilidade dos serviços, e armazenados para análise posterior. O sistema notifica automaticamente quando algum serviço apresenta problemas.

---

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python 3.7+
- **Bibliotecas:**
  - requests
  - BeautifulSoup
  - pandas
  - schedule

---

## Objetivo

O objetivo principal deste projeto é fornecer uma ferramenta eficiente e confiável para empresas e administradores de sistemas que dependem dos serviços de NFE, permitindo a identificação rápida de falhas e auxiliando na tomada de decisões.

---

## 1. Visão Geral do Projeto

Este projeto tem como objetivo monitorar a disponibilidade dos serviços de emissão de Nota Fiscal Eletrônica (NFE) oferecidos pelo site da Secretaria da Fazenda. O script desenvolvido realiza consultas regulares ao site, extrai dados relevantes sobre o status dos serviços e armazena essas informações em um arquivo CSV. Além disso, o script identifica e reporta quaisquer problemas nos serviços, facilitando a gestão e o diagnóstico de falhas.

---

## 2. Pré-requisitos

Antes de executar o script, certifique-se de que o ambiente de desenvolvimento está configurado com as seguintes ferramentas e bibliotecas:

- Python 3.7 ou superior
- Bibliotecas Python:
  - requests
  - beautifulsoup4
  - pandas
  - schedule

Para instalar as bibliotecas necessárias, utilize o seguinte comando:

`pip install requests beautifulsoup4 pandas schedule`

---

## 3. Instalação

1. Clone este repositório: `https://github.com/https-ailton-dev/Monitorar_NFE_Status.git` ou `git@github.com:https-ailton-dev/Monitorar_NFE_Status.git`
2. Navegue até o diretório do projeto.

---

## 4. Uso
Para executar o script, basta rodar o seguinte comando:

`python monitor_nfe.py`

O script será executado por um período de 8 horas, realizando consultas ao site da NFE a cada 30 minutos. Ao final, os dados coletados serão salvos em um arquivo CSV na pasta Downloads do usuário.

---

## 5. Estrutura do Código
`map_status(img)`: Converte o status das imagens (verde, amarelo, vermelho) em valores numéricos.
`extrair_dados()`: Faz a requisição ao site, extrai os dados necessários e os armazena em uma lista.
`verificar_problemas()`: Verifica se algum serviço está com problemas e reporta na tela.
`job()`: Função agendada para coletar dados em intervalos regulares.
`salvar_csv()`: Salva os dados coletados em um arquivo CSV.
`schedule.run_pending()`: Executa as tarefas agendadas.

---

## 6. Funcionalidades
**Monitoramento Automático:** O script consulta o site da NFE e verifica o status dos serviços automaticamente em intervalos regulares.
**Relatório de Problemas:** O script identifica e reporta quaisquer problemas encontrados nos serviços monitorados.
**Armazenamento de Dados:** Os dados coletados são armazenados em um arquivo CSV, facilitando a análise posterior.

---

## 7. Limitações Conhecidas
**Intervalo de Tempo:** O script está configurado para rodar por 8 horas. Para um monitoramento mais prolongado, ajustes manuais são necessários.
**Resiliência:** Caso o site da NFE esteja fora do ar ou inacessível, o script não tentará reconectar automaticamente após a falha.

---

## 8. Possíveis Melhorias
**Aprimoramento de Erros:** Melhorar o tratamento de erros para incluir tentativas de reconexão em caso de falhas temporárias.
**Monitoramento Prolongado:** Adaptar o script para funcionar por períodos mais longos ou indefinidamente, com opções de configuração de tempo.

---

## 9. Conclusão
Este projeto oferece uma solução prática para monitorar o status dos serviços de NFE. Com ele, é possível detectar rapidamente falhas nos serviços, o que pode auxiliar na tomada de decisões dentro de empresas que dependem da emissão de notas fiscais.

---

## 10. Dados Obtidos
**Data de Teste:** 31/08/2024

**Período de Teste:** 8 horas
**Intervalo de Extração de Dados:** A cada 30 minutos
**Número de Salvamentos:** 15

**Observações Durante o Período de Teste:**

- Nenhuma variação foi detectada no sistema de NFE durante o período de teste.
- O monitoramento ocorreu conforme o esperado, com os dados sendo coletados e salvos regularmente.