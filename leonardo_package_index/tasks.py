from __future__ import absolute_import

from celery import shared_task
from django.core import management
from leonardo.decorators import catch_result


@shared_task
@catch_result
def update_all_packages():
    management.call_command('update_all_packages')
    return {'result': 'Update packages OK'}
