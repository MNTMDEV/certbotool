import json
from certbotool.core.rest import RestRequest
from certbotool.dns.dns import DnsExecutable


class Dnspod(DnsExecutable):
    _dnspod_header = {
        "User-Agent": "certbotool-dnspod/1.0.0 (admin@mntmdev.com)"
    }

    def description(self):
        return "DNSPOD auth tool."

    def auth(self, data):
        self.clean(data)
        key = data['params']['key']
        request = RestRequest("https://dnsapi.cn/Record.Create")
        data_post = {
            "login_token": key,
            "format": "json",
            "domain": data['domain'],
            "sub_domain": self.join_verify_prefix(data['subdomain']),
            "record_type": "TXT",
            "value": data['verify'],
            "record_line": "默认"
        }
        text = request.doPost(data_post, self._dnspod_header)
        json_data = json.loads(text)
        code = int(json_data['status']['code'])
        if code == 1:
            self.print_success("Create DNS record success.")
        elif code == 104:
            self.print_error(
                "DNS record exists. Please delete this record first.")
        else:
            self.print_error("Unknown status code:%d" % code)

    def query_subdomain_id(self, data):
        key = data['params']['key']
        request = RestRequest("https://dnsapi.cn/Record.List")
        data_post = {
            "login_token": key,
            "format": "json",
            "domain": data['domain'],
            "sub_domain": self.join_verify_prefix(data['subdomain']),
            "record_type": "TXT"
        }
        text = request.doPost(data_post, self._dnspod_header)
        json_data = json.loads(text)
        records = json_data.get('records', [])
        if len(records) == 0:
            return None
        else:
            return records[0]['id']

    def clean(self, data):
        key = data['params']['key']
        subdomain_id = self.query_subdomain_id(data)
        request = RestRequest("https://dnsapi.cn/Record.Remove")
        data_post = {
            "login_token": key,
            "format": "json",
            "domain": data['domain'],
            "record_id": subdomain_id
        }
        text = request.doPost(data_post, self._dnspod_header)
        json_data = json.loads(text)
        code = int(json_data['status']['code'])
        if code == 1:
            self.print_success("Delete DNS record success.")
        elif code == 8:
            self.print_success("DNS record does not exist.Ignored...")
        else:
            self.print_error("Unknown status code:%d" % code)

    def get_master_domain(self, params, subdomain):
        key = params['key']
        request = RestRequest("https://dnsapi.cn/Domain.List")
        data_post = {
            "login_token": key,
            "format": "json"
        }
        text = request.doPost(data_post, self._dnspod_header)
        json_data = json.loads(text)
        domains = json_data.get('domains', [])
        for domain_json in domains:
            domain = domain_json.get('name')
            if subdomain.endswith(domain):
                return domain
        return None
