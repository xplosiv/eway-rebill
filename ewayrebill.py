from suds.client import Client
from suds.sax.element import Element


class EwayRebill(object):
    def __init__(self, url, eway_id, username, password):

        self.client = Client(url)

        eway_header = self.client.factory.create("eWAYHeader")
        eway_header.eWAYCustomerID = eway_id
        eway_header.Username = username
        eway_header.Password = password

        self.client.set_options(soapheaders=eway_header)

        self.customer_fields = [
            'customerTitle',
            'customerFirstName',
            'customerLastName',
            'customerAddress',
            'customerSuburb',
            'customerState',
            'customerCompany',
            'customerPostCode',
            'customerCountry',
            'customerEmail',
            'customerFax',
            'customerPhone1',
            'customerPhone2',
            'customerRef',
            'customerJobDesc',
            'customerComments',
            'customerURL'
        ]

        self.payment_fields = [
            'RebillCustomerID',
            'RebillInvRef',
            'RebillInvDes',
            'RebillCCName',
            'RebillCCNumber',
            'RebillCCExpMonth',
            'RebillCCExpYear',
            'RebillInitAmt',
            'RebillInitDate',
            'RebillRecurAmt',
            'RebillStartDate',
            'RebillInterval',
            'RebillIntervalType',
            'RebillEndDate'
        ]

    '''
    Customer CRUD Methods
    '''
    def customer_add(self, params):
        return self._customer_action(None, params)

    def customer_edit(self, customer_id, params):
        return self._customer_action(customer_id, params)

    def customer_delete(self, customer_id):
        return self.client.service.DeleteRebillCustomer(RebillCustomerID=customer_id)

    def customer_get(self, customer_id):
        return self.client.service.QueryRebillCustomer(RebillCustomerID=customer_id)

    def _customer_action(self, customer_id, params={}):

        required = ['customerFirstName', 'customerLastName', 'customerEmail']

        for req in required:
            if req not in params:
                raise Exception("%s is a required field." % req)

        for field in self.customer_fields:
            if field not in params:
                params[field] = ''

        if customer_id:
            params['RebillCustomerID'] = customer_id
            return self.client.service.UpdateRebillCustomer(**params)
        else:
            return self.client.service.CreateRebillCustomer(**params)



    '''
    Payment CRUD Methods
    '''
    def payment_add(self, params):
        return self._payment_action(None, params)

    def payment_edit(self, rebill_id, params):
        return self._payment_action(rebill_id, params)

    def payment_delete(self, customer_id, rebill_id):
        return self.client.service.DeleteRebillEvent(RebillCustomerID=customer_id, RebillID=rebill_id)

    def payment_get(self, customer_id, rebill_id):
        return self.client.service.QueryRebillEvent(RebillCustomerID=customer_id, RebillID=rebill_id)

    def _payment_action(self, rebill_id=None, params={}):

        for field in self.payment_fields:
            if field not in params:
                raise Exception("%s is a required field." % field)

        if rebill_id:
            params['RebillID'] = rebill_id
            return self.client.service.UpdateRebillEvent(**params)
        else:
            return self.client.service.CreateRebillEvent(**params)


    '''
    Transaction Reporting Methods
    '''
    def transactions(self, customer_id, rebill_id, start_date=None, end_date=None, status=None):
        params = {
            'RebillCustomerID': customer_id,
            'RebillID': rebill_id,
            'startDate': start_date,
            'endDate': end_date,
            'status': status
        }
        return self.client.service.QueryTransactions(**params)

    def transaction_next(self, customer_id, rebill_id):
        return self.client.service.QueryNextTransaction(RebillCustomerID=customer_id, RebillID=rebill_id)
