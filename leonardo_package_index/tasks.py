from __future__ import absolute_import

from celery import shared_task
from django.core import management
from leonardo.decorators import catch_result
from django.apps import apps
from django.utils import six

from .models import Package

CounterWidget = apps.get_model('web', 'CounterWidget')


def update_counter_modules():
    '''Package counter'''

    counter = CounterWidget.objects.get(label__icontains='modules')
    counter.number = Package.objects.count()
    counter.save()
    return counter.number


def update_counter_downloads():
    '''Update downloads'''
    counter = CounterWidget.objects.get(label__icontains='downloads')
    counter.number = reduce(lambda x, y: x + y,
                            [p.total_downloads
                             for p in Package.objects.all()])
    counter.save()
    return counter.number


def update_counter_stars():
    '''Update stars'''
    counter = CounterWidget.objects.get(label__icontains='stars')
    counter.number = reduce(lambda x, y: x + y,
                            [p.repo_watchers
                             for p in Package.objects.all()])
    counter.save()
    return counter.number


def update_counter_forks():
    '''Update forks'''
    counter = CounterWidget.objects.get(label__icontains='forks')
    counter.number = reduce(lambda x, y: x + y,
                            [p.repo_forks
                             for p in Package.objects.all()])
    counter.save()

    return counter.number


def update_counter_participants():
    '''Update participants'''
    counter = CounterWidget.objects.get(label__icontains='participants')
    counter.number = reduce(lambda x, y: x + y,
                            [len(p.participants.split(','))
                             for p in Package.objects.all()])
    counter.save()

    return counter.number

COUNTERS_CONFIG = {
    'modules': update_counter_modules,
    'downloads': update_counter_downloads,
    'stars': update_counter_stars,
    'forks': update_counter_forks,
    'participants': update_counter_participants,
}


@shared_task
@catch_result
def update_counters():

    result = []

    for counter, update_fn in six.iteritems(COUNTERS_CONFIG):

        try:
            res = update_fn()
        except Exception as e:
            result.append({counter: str(e)})
        else:
            result.append({counter: res})

    return {'result': result}


@shared_task
@catch_result
def update_all_packages():
    management.call_command('update_all_packages')
    return {'result': 'Update packages OK'}
