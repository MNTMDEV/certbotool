from abc import abstractmethod
import os
import sys
import time

class DnsExecutable():
    _acme_prefix = '_acme-challenge'

    def print_error(self, content):
        print("\033[31m[ERROR] %s\033[0m" % content)

    def print_success(self, content):
        print("\033[32m[SUCCESS] %s\033[0m" % content)

    @abstractmethod
    def description(self):
        return "DNS auth tool template."

    @abstractmethod
    def auth(self, data):
        pass

    @abstractmethod
    def clean(self, data):
        pass

    @abstractmethod
    def get_master_domain(self, params, subdomain):
        pass

    # def parse(self):
    #     parser = argparse.ArgumentParser(
    #         description=self.description())
    #     parser.add_argument(
    #         '-c', '--config', help='Certbot dns hook configuration file.')
    #     parser.add_argument(
    #         '-d', '--clean', action='store_true', help='Run certbot dns clean hook.')
    #     self._args = parser.parse_args()

    def __init__(self) -> None:
        pass

    def error_and_exit(self, str):
        print(str)
        sys.exit(1)

    def get_subdomain_prefix(self, domain, subdomain):
        length = len(domain)
        sub_length = len(subdomain)
        prefix = subdomain[0:sub_length-length]
        if prefix.endswith('.'):
            prefix = prefix[0:len(prefix)-1]
        return prefix

    def join_verify_prefix(self, domain):
        if domain == '':
            return self._acme_prefix
        else:
            return self._acme_prefix+'.'+domain

    def execute(self,params,clean):
        subdomain = os.environ.get('CERTBOT_DOMAIN')
        verify = os.environ.get('CERTBOT_VALIDATION')
        # config = self._args.config
        # if config == None:
        #     self.error_and_exit("Configuration file path is required.")
        if subdomain == None:
            self.error_and_exit(
                "Can not acquire $CERTBOT_DOMAIN envirionment variable.")
        if verify == None:
            self.error_and_exit(
                "Can not acquire $CERTBOT_VALIDATION envirionment variable.")

        # json_data = UserConfig.parse(config)
        # params = json_data.get('params')
        if params == None:
            self.error_and_exit(
                "Configuration file does not declare parameters.")

        domain = self.get_master_domain(params, subdomain)
        if domain == None:
            self.error_and_exit("Can not find the master domain.")

        prefix = self.get_subdomain_prefix(domain, subdomain)
        data = {
            "params": params,
            "domain": domain,
            "subdomain": prefix,
            "verify": verify
        }
        if not clean:
            self.auth(data)
            time.sleep(30)
        else:
            self.clean(data)
