from __future__ import absolute_import

from celery import shared_task
from django.core import management


@shared_task
def update_all_packages():
    management.call_command('update_all_packages', interactive=False)
    return {'result': 'Update packages OK'}
