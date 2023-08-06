from divinegift import logger, version
from mailer import Mailer, Message
import requests
from deprecation import deprecated
from email.header import Header


class Sender:
    def __init__(self):
        self.email_connector = None
        self.zabbix_agent = None

    def send_mail(self, msg: str, subject: str, TO: list, CC: list = None, BCC: list = None,
               FROM: str = '', HOST: str = '', PORT=0, USE_TLS=False,
               usr='', pwd='',
               charset: str = 'utf-8', IS_HTML: bool = True, attachments: object = None, mimetype: str = None):
        """
        Sending email
        :param msg: Message body
        :param subject: Message subject
        :param TO: List of recipients
        :param CC: List of copy recipients
        :param BCC: List of shadow copy recipients
        :param FROM: Sender email
        :param HOST: smtp server
        :param usr: user
        :param pwd: password
        :param charset: Encoding charset
        :param IS_HTML: Will it be HTML or plain text
        :param attachments: Attachments
        :param mimetype: Mimetipe of attachments
        :return:
        """
        message = Message(From=FROM,
                          To=TO,
                          Cc=CC,
                          Bcc=BCC,
                          charset=charset)
        message.Subject = Header(subject.encode('utf-8'), 'UTF-8').encode()
        if IS_HTML:
            message.Html = msg
        else:
            message.Body = msg
        if attachments:
            if type(attachments) == list:
                for file in attachments:
                    try:
                        message.attach(file, mimetype=mimetype, charset=charset)
                    except Exception as ex:
                        logger.log_err(f'Could not attach file: {file}')
            elif type(attachments) == str:
                try:
                    message.attach(attachments)
                except Exception as ex:
                    logger.log_err(f'Could not attach file: {attachments}')
            else:
                logger.log_warning('There is incorrect type of variable attachments')

        if self.email_connector is None:
            self.email_connector = Mailer(HOST, PORT, USE_TLS, usr=usr, pwd=pwd)
        try:
            self.email_connector.send(message)
        except Exception as ex:
            logger.log_err('Error while sending email')
            self.email_connector = None

    def send_telegram(self, message: str, chat_id: int = 161680036):
        """
            Send a telegram message
            :param message: Message
            :param chat_id: Id of chat where msg will be sent
            :param subject: Subject of message
            :return: None
            """
        URL = 'https://api.telegram.org/bot'  # URL на который отправляется запрос
        TOKEN = '456941934:AAGZMmXJE4VyLagIkVY7qMG0doASxU7f8ac'  # токен вашего бота, полученный от @BotFather
        data = {'chat_id': chat_id, 'text': message}

        try:
            requests.post(URL + TOKEN + '/sendMessage', data=data)  # запрос на отправку сообщения
        except:
            logger.log_err('Send message error')

    def send_slack(self, message: str, webhook: str = None, channel: str = 'aims_integrations',
                   username: str = 'aims_notifier',
                   icon_url: str = None):
        """
        Send message to slack
        :param message: Message
        :param webhook: WebHook URL to sending
        :return: None
        """
        if not webhook:
            webhook = 'https://mattermost.s7.aero/hooks/71ra7afrgjytfq4j5wm4o6x6jo'
        data = {
            'text': message,
            'username': username,
            'channel': channel,
        }
        if icon_url:
            data.update({'icon_url': icon_url})
        try:
            requests.post(webhook, json=data, headers={'content-type': 'application/json'})
        except:
            logger.log_err('Send message error')

    def send_zabbix(self, host, key, value, **server_conf):
        from divinegift import zabbix_agent
        if self.zabbix_agent is None:
            self.zabbix_agent = zabbix_agent.ZabbixAgent(**server_conf)
        try:
            self.zabbix_agent.send(host, key, value)
        except:
            logger.log_err('Error was occured while sending status to zabbix')


@deprecated(deprecated_in='1.3.16', current_version=version, details='Use class Connection instead')
def send_email(msg: str, subject: str, TO: list, CC: list = None, BCC: list = None, 
               FROM: str = '', HOST: str = '', PORT=0, USE_TLS=False, usr='', pwd='',
               charset: str = 'utf-8', IS_HTML: bool = True, attachments: object = None, mimetype: str = None):
    sender = Sender()
    sender.send_mail(msg, subject, TO, CC, BCC, FROM, HOST, PORT, USE_TLS, usr, pwd, charset, IS_HTML, attachments, mimetype)


@deprecated(deprecated_in='1.3.16', current_version=version, details='Use class Connection instead')
def send_telegram(message: str, chat_id: int = 161680036, subject: str = None):
    sender = Sender()
    sender.send_telegram(message, chat_id)


@deprecated(deprecated_in='1.3.16', current_version=version, details='Use class Connection instead')
def send_slack(message: str, webhook: str = None, channel: str = 'aims_integrations', username: str = 'aims_notifier',
               icon_url: str = None):
    sender = Sender()
    sender.send_slack(message, webhook, channel, username, icon_url)


"""
def auth_vk(login, password):
    # Авторизоваться как человек
    vk = vk_api.VkApi(login=login, password=password)
    vk.auth()
    # Авторизоваться как сообщество
    #vk = vk_api.VkApi(token='a94dd2ef02952a0606fd37f2d1fb11b2d456c034c7671c2b3fab8c3f660474062b9e253c78597d9248469')

    return vk


def send_vk(vk, message, chat_id='8636128', mode='private'):
    #vk = auth_vk()
    if mode == 'private':
        vk.method('messages.send', {'user_id': chat_id, 'message': message})
    elif mode == 'chat':
        vk.method('messages.send', {'peer_id': chat_id, 'message': message})
    elif mode == 'group':
        vk.method('messages.send', {'user_ids': chat_id, 'message': message})
"""

if __name__ == '__main__':
    pass
