import argparse
import os

from certbotool.core.executable import Executable
from apscheduler.schedulers.blocking import BlockingScheduler

from certbotool.core.userconf import UserConfig

# Renew command does not require hook script
CERTBOT_RENEW_CMD = "certbot renew"


class CrondExecutable(Executable):
    _config = {
        "log_directory": "/var/log/certbotool",
        "post_renew": "echo Success."
    }

    def job(self):
        os.system(CERTBOT_RENEW_CMD)
        os.system(self._config['post_renew'])

    def parse(self):
        parser = argparse.ArgumentParser(
            description='Certbot automatic renewal daemon.')
        parser.add_argument(
            '-f', '--force', action='store_true', help='Force renew certificate once and quit.')
        parser.add_argument(
            '-c', '--config', help='Configuration file path.')
        self._args = parser.parse_args()
        config_path = self._args.config
        if not config_path == None:
            self._config = UserConfig.parse(config_path)

    def execute(self):
        if self._args.force:
            self.job()
        else:
            scheduler = BlockingScheduler(timezone='Asia/Shanghai')
            scheduler.add_job(self.job, 'cron', day_of_week='0',
                              hour='0', minute='0', id='renewal')
            scheduler.start()
