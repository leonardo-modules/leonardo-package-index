import logging
import logging.config

from django.core.management.base import NoArgsCommand

from django.core import management

logger = logging.getLogger(__name__)


class Command(NoArgsCommand):

    help = "Updates all the packages in the system"

    def handle(self, *args, **options):
        try:
            management.call_command('package_updater')
        except Exception as e:
            logger.exception(e)
        try:
            management.call_command('repo_updater')
        except Exception as e:
            logger.exception(e)
