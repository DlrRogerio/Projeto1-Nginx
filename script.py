import requests
import time

def enviar_notificacao_discord(mensagem):
    webhook_url = 'https://discordapp.com/api/webhooks/coloque/aqui/sua/url/webhook'
    payload = {
        "content": mensagem
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Notificação enviada para o Discord com sucesso!")
        else:
            print(f"Falha ao enviar notificação para o Discord. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar notificação para o Discord: {e}")

def verificar_site(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            enviar_notificacao_discord(f'O site {url} está ONLINE.')
        else:
            enviar_notificacao_discord(f'O site {url} está OFFLINE. Status: {resposta.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'O site está OFFLINE. Erro {e}')
        enviar_notificacao_discord(f'O site {url} está OFFLINE. Erro: {e}')

url = 'http://localhost/'

while True:
    verificar_site(url)
    time.sleep(60)
