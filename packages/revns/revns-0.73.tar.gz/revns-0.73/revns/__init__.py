import requests
__version__ = '0.73'
DEV = 'DEV'
STG = 'STG'
PROD = 'PROD'
HOST = 'https://notification.revtel-api.com/v2'
STG_HOST = 'https://notification-stg.revtel-api.com/v2'
DEV_HOST = 'https://notification-dev.revtel-api.com/v2'


class BaseNotification:
    target_type = 'mobile'
    publish_path = ''

    def __init__(self, api_key, instance=None, stage='DEV'):
        if stage not in ['PROD', 'STG', 'DEV']:
            raise ValueError('stage should be in [PROD, STG, DEV]')
        self.instance = instance
        self.api_key = api_key
        self.stage = stage

    def get_host(self):
        if self.stage == PROD:
            return HOST
        elif self.stage == STG:
            return STG_HOST
        else:
            return DEV_HOST

    def build_request_payload(self, *args, **kwargs):
        raise NotImplementedError

    def get_url(self, *args, **kwargs):
        raise NotImplementedError

    def _build_headers(self):
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def _post(self, url, data):
        resp = requests.post(url, headers=self._build_headers(), json=data)
        return resp

    def build_title(self):
        raise NotImplementedError

    def build_body(self):
        raise NotImplementedError

    def build_target(self):
        raise NotImplementedError

    def build_data(self):
        raise NotImplementedError

    def publish(self, *args, **kwargs):
        url = self.get_url(*args, **kwargs)
        payload = self.build_request_payload(*args, **kwargs)
        try:
            resp = self._post(url, data=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(e)
            return None


class MobileNotification(BaseNotification):
    target_type = 'mobile'
    dest = 'user'

    def get_url(self, target=None, **kwargs):
        if target == None:
            target = self.build_target()
        host = self.get_host()
        return f'{host}/notification/publish/{self.dest}/{target}'

    def build_request_payload(self, target=None, title=None, body=None, data=None):
        if title == None:
            title = self.build_title()
        if body == None:
            body = self.build_body()
        if data == None:
            data = self.build_data()
        body = {
            'subject': title,
            'title': title,
            'body': body,
            'data': data
        }
        return body


class EmailNotification(BaseNotification):
    target_type = 'email'
    sender_name = 'default'

    def get_url(self, **kwargs):
        host = self.get_host()
        return f'{host}/email/extra/send/{self.sender_name}'

    def build_request_payload(self, target=None, title=None, body=None):
        if not target:
            target = self.build_target()
        if not title:
            title = self.build_title()
        if not body:
            body = self.build_body()

        payload = {
            'html': body,
            'subject': title,
            'to': target
        }
        return payload


class TemplatedEmailNotification(EmailNotification):
    def get_url(self, **kwargs):
        host = self.get_host()
        return f'{host}/email/send/{self.sender_name}'

    def build_request_payload(self, target=None, data=None):
        if not target:
            target = self.build_target()
        if not data:
            data = self.build_data()

        payload = {
            'to': target,
            'data': data
        }
        return payload


class SmsNotification(BaseNotification):
    def get_url(self, **kwargs):
        host = self.get_host()
        return f'{host}/sms/send'

    def build_request_payload(self, target=None, title=None, body=None):
        if not target:
            target = self.build_target()
        if not title:
            title = self.build_title()
        if not body:
            body = self.build_body()

        payload = {
            'message': body,
            'subject': title,
            'phone': target
        }
        return payload
