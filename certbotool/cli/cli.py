import argparse
import importlib
import os
import sys
from certbotool.core.executable import Executable
from certbotool.core.userconf import UserConfig
from certbotool.dns.dns import DnsExecutable


class CliExecutable(Executable):
    _cert_acquire_prefix = 'certbot certonly --manual --preferred-challenges dns-01'
    _acme_server_opt = '--server https://acme-v02.api.letsencrypt.org/directory'

    def parse(self):
        parser = argparse.ArgumentParser(
            description='Certbot CLI tool.')
        cmd_parser = parser.add_subparsers(dest='cmd', help="Command Options")

        # DNS interface adapter
        dns_parser = cmd_parser.add_parser(
            'dns', help='DNS auth and clean function.')
        dns_parser.add_argument(
            '-c', '--config', help='Certbot dns hook configuration name.')
        dns_parser.add_argument(
            '-d', '--clean', action='store_true', help='Run certbot dns clean hook.')

        # Certificate
        cert_parser = cmd_parser.add_parser(
            'cert', help='New certificate request function.')
        cert_parser.add_argument(
            '-c', '--config', help='Certbot dns hook configuration name.')
        cert_parser.add_argument(
            '-d', '--domain', help='Your domain name.')

        # Configuration
        conf_parser = cmd_parser.add_parser(
            'conf', help='Configuration manager.')

        self._args = parser.parse_args()

    def read_config(self, config_name):
        if config_name == None:
            print("Configuration name is required.")
            sys.exit(1)
        self._config_path = "/etc/certbotool/conf.d/%s.json" % config_name
        self._config = UserConfig.parse(self._config_path)

    def dns(self):
        self.read_config(self._args.config)
        module_name = self._config['module']
        clz_name = self._config['class']
        m = importlib.import_module(module_name)
        clz = getattr(m, clz_name)
        params = self._config['params']
        clean = self._args.clean
        instance:DnsExecutable = clz()
        instance.execute(params, clean)

    def cert(self):
        self.read_config(self._args.config)
        domain = self._args.domain
        if domain == None:
            print("Domain name is required.")
            sys.exit(1)
        acquire_hook = 'certbotool dns -c %s' % self._args.config
        clean_hook = '%s -d' % acquire_hook
        cmd = '%s -d %s %s --manual-auth-hook "%s" --manual-cleanup-hook "%s"' % (
            self._cert_acquire_prefix, domain, self._acme_server_opt, acquire_hook, clean_hook)
        os.system(cmd)

    def conf(self):
        pass

    def execute(self):
        if self._args.cmd == 'dns':
            self.dns()
        elif self._args.cmd == 'cert':
            self.cert()
        elif self._args.cmd == 'conf':
            self.conf()
        else:
            print("Unknown option.")
