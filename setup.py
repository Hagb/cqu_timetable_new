#!/usr/bin/env python
# coding: utf-8
from setuptools import setup

setup(
    name='cqu_timetable_new',
    version='0.3.2.5',
    author='weearc',
    author_email='qby19981121@gmail.com',
    license='agpl-3.0',
    url='https://github.com/weearc/cqu_timetable_new',
    description=u'translate xlsx or timetable to ics',
    packages=['cqu_timetable_new'],
    install_requires=['icalendar', 'openpyxl', 'configparser'],
    keywords=['cqu','ics','iCalendar','timetable']
)
