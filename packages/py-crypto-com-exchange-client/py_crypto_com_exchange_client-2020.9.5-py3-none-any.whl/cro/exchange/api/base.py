class BaseCryptoComClient(object):

    def __init__(self, is_sandbox=True):
        self._root_url = f'https://uat-api.3ona.co/v2/' if is_sandbox else 'https://api.crypto.com/v2/'
