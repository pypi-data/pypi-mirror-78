from .model import Model

class OneClickConfig(Model):

    def _accepted_params(self):
        return [
            'configId',
            'shortNumber',
            'merchantId',
            'serviceCode',
            'businessModel',
            'recurring',
            'redirectUrl',
            'onlineText',
            'offlineText',
            'age',
            'isRestricted',
            'invoiceText',
            'price',
            'timeout',
            'created',
            'lastModified',
        ]
