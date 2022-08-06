import json
from certbotool.dns.dns import DnsExecutable
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainsRequest import DescribeDomainsRequest
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest


class Aliyun(DnsExecutable):

    def description(self):
        return "Aliyun DNS auth tool."

    def query_record(self, data):
        client = AcsClient(data['params']['key_id'],
                           data['params']['key_secret'], 'cn-hangzhou')
        request = DescribeSubDomainRecordsRequest()
        sub = self.join_verify_prefix(data['subdomain'])
        if sub != '':
            sub += '.'
        full_sub = sub + data['domain']
        request.set_DomainName(data['domain'])
        request.set_SubDomain(full_sub)
        request.set_Type('TXT')
        response = client.do_action_with_exception(request)
        json_data = json.loads(response)
        records = json_data['DomainRecords']['Record']
        if len(records) == 0:
            return None
        else:
            record = records[0]
            return record['RecordId']

    def auth(self, data):
        self.clean(data)
        sub = self.join_verify_prefix(data['subdomain'])
        client = AcsClient(data['params']['key_id'],
                           data['params']['key_secret'], 'cn-hangzhou')
        request = AddDomainRecordRequest()
        request.set_DomainName(data['domain'])
        request.set_RR(sub)
        request.set_Type('TXT')
        request.set_Value(data['verify'])
        try:
            client.do_action_with_exception(request)
            self.print_success("Create DNS record success.")
        except Exception as e:
            self.print_error(e.message)

    def clean(self, data):
        record_id = self.query_record(data)
        if record_id == None:
            self.print_success("DNS record does not exist.Ignored...")
            return
        client = AcsClient(data['params']['key_id'],
                           data['params']['key_secret'], 'cn-hangzhou')
        request = DeleteDomainRecordRequest()
        request.set_RecordId(record_id)
        try:
            client.do_action_with_exception(request)
            self.print_success("Delete DNS record success.")
        except Exception as e:
            self.print_error(e.message)

    def get_master_domain(self, params, subdomain):
        client = AcsClient(
            params['key_id'], params['key_secret'], 'cn-hangzhou')
        request = DescribeDomainsRequest()
        response = client.do_action_with_exception(request)
        json_data = json.loads(response)
        for domain_json in json_data['Domains']['Domain']:
            domain = domain_json['DomainName']
            if subdomain.endswith(domain):
                return domain
        return None
