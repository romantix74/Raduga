# -*- coding: utf-8 -*-

from celery import task

from celery import Celery

#app = Celery('tasks', ) #broker='amqp://guest@localhost//')
#@task()
@task
def add(x, y):
    print "ddddddddddddddddddddddddddd"
    return x + y
