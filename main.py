import requests
import time
import json
import os


class TelegramBot:
    def __init__(self):
        token = '5826503992:AAFO64pWMTDFqgY1KQ72pBgqG1Sebem9mCE'
        self.url_base = f'https://api.telegram.org/bot{token}/'
    # Iniciar o bot

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_mensagens(update_id)
            mensagens = atualizacao['result']
            if mensagens:
                for mensagem in mensagens:
                    update_id = mensagem['update_id']
                    chat_id = mensagem['message']['from']['id']
                    eh_primeira_mensagem = mensagem['message']['message_id'] == 1
                    resposta = self.criar_resposta(
                        mensagem, eh_primeira_mensagem)
                    self.responder(resposta, chat_id)
    # Obter mensagens

    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)
    # Criar uma resposta

    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        mensagem = mensagem['message']['text']
        if eh_primeira_mensagem == True or mensagem.lower() == 'atendimento':
            return f'''Olá bem vindo a nosso consultorio. Digite o número para ter atendimento desejado{os.linesep}1 - Massagem{os.linesep}2 - Acuputura{os.linesep}3 - Fisioterapia'''
        if mensagem == '1':
            return f'''Massagem{os.linesep}Confirmar consulta(s/n)'''
        if mensagem == '2':
            return f'''Acuputura{os.linesep}Confirmar consulta(s/n)'''
        if mensagem == '3':
            return f'''Fisioterapia{os.linesep}Confirmar consulta(s/n)'''

        if mensagem.lower() in ('s', 'sim'):
            return '''consulta foi marcada com sucesso!\n Observação, atendimento por ondem de chegada'''
        else:
            return 'Gostaria de acessar o atendimento? Digite "atendimento"'
    # Responder

    def responder(self, resposta, chat_id):
        # enviar
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)


bot = TelegramBot()
bot.Iniciar()
