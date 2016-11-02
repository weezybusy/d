#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import pathlib
#import tests
#import unittest

class Task(object):

    def __init__(self, id_, text, status='unfinished'):
        self.id_ = id_
        self.text = text
        self.status = status

    def get_id(self):
        return self.id_

    def get_text(self):
        return self.text

    def get_status(self):
        return self.status

    def set_id(self, id_):
        self.id_ = id_

    def set_text(self, text):
        self.text = text

    def set_status(self, status):
        self.status = status


class Tasklist(object):

    ids = [i for i in range(1, 100)]
    num_of_tasks = 0

    def __init__(self):
        self.tasks = {}
        self.limit = 99

    def get_tasks(self):
        return self.tasks

    def pop_id(self, id_):
        self.ids.remove(id_)


    def add(self, id_, text, status='unfinished'):
        if self.num_of_tasks <= self.limit:
            task = Task(id_, text, status)
            self.tasks[task.id_] = task
            self.num_of_tasks += 1

    def change(self, id_):
        if id_ in self.tasks:
            text = input('task: ')
            self.tasks[id_].set_text(text)

    def finish(self, id_):
        if id_ in self.tasks:
            self.tasks[id_].set_status('finished')

    def finish_all(self):
        temp_dict = self.tasks.copy()
        for k in temp_dict:
            self.tasks[k].set_status('finished')

    def list_all(self):
        if self.num_of_tasks == 0:
            print('\nNo tasks')
        else:
            for k in self.tasks.keys():
                print('{:2}. [{}] {}'.format(self.tasks[k].get_id(),
                    'X' if self.tasks[k].get_status() == 'finished' else ' ',
                    self.tasks[k].get_text()))
        print('')

    def remove(self, id_):
        if id_ in self.tasks:
            self.tasks.pop(id_)
            self.num_of_tasks -= 1

    def remove_all(self):
        self.tasks.clear()
        self.num_of_tasks = 0

    def unfinish(self, id_):
        if id_ in self.tasks:
            self.tasks[id_].set_status('unfinished')

    def unfinish_all(self):
        temp_dict = self.tasks.copy()
        for k in temp_dict:
            self.tasks[k].set_status('unfinished')


#def write_tasks(tasks, taskfile):
#    ''' Writes tasks to file '''
#    if taskfile.exists():
#        try:
#            with taskfile.open('w') as f:
#                data = {}
#                for k in tasks:
#                    data[tasks[k].get_id()] = {
#                        'id':tasks[k].get_id(),
#                        'text': tasks[k].get_text(),
#                        'status': tasks[k].get_status()
#                    }
#                json.dump(data, f, ensure_ascii=False, indent=2)
#                f.write('\n')
#        except IOError as e:
#            print(e)
#    else:
#        print('No such file')


def read_tasks(tasks, taskfile):
    if taskfile.exists():
        if taskfile.stat().st_size > 0:
            try:
                with taskfile.open('r') as f:
                    try:
                        data = json.load(f)
                        for k in data:
                            id_ = data[k]['id']
                            tasks.pop_id(id_)
                            text = data[k]['text']
                            status = data[k]['status']
                            tasks.add(id_, text, status)
                    except ValueError:
                        pass
            except IOError as e:
                print(e)
    else:
        print('Task list doesn\'t exist yet. ' \
              'Run program with -i option to create it.')


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', dest='add',
            help='add TASK to tasklist', metavar='TASK')
    parser.add_argument('-c', '--change', dest='change', type=int,
            help='change task with specified ID', metavar='ID')
    parser.add_argument('-f', '--finish', dest='finish', type=int,
            help='mark task with specified ID as finished', metavar='ID')
    parser.add_argument('-F', '--finish-all', dest='finish_all',
            action='store_true', help='mark all tasks as finished')
    parser.add_argument('-i', '--init', dest='init', action='store_true',
            help='create tasks file')
    parser.add_argument('-p', '--path', dest='path', metavar='PATH',
            help='set PATH to tasklist')
    parser.add_argument('-r', '--remove', dest='remove', type=int,
            help='remove task with specified ID', metavar='ID')
    parser.add_argument('-R', '--remove-all', dest='remove_all',
            action='store_true', help='remove all tasks')
    parser.add_argument('-u', '--unfinish', dest='unfinish', type=int,
            help='mark task with specified ID as unfinished', metavar='ID')
    parser.add_argument('-U', '--unfinish-all', dest='unfinish_all',
            action='store_true', help='mark all tasks as unfinished')
    parser.add_argument('-v', '--version', action='version',
            version='do 0.1')
    return parser


if __name__ == '__main__':
    tasks = Tasklist()
    args = get_parser().parse_args()
    taskfile = pathlib.Path().resolve().joinpath('todo.json')

    if args.init:
        if taskfile.exists():
            print('Task list already exists')
        else:
            try:
                taskfile.touch()
                print('Task list created successfully')
            except IOError as e:
                print(e)

    read_tasks(tasks, taskfile)

    #if args.add:
    #    id_ = tasks.ids[0]
    #    tasks.ids.remove(id_)
    #    tasks.add(id_, args.add)
    #    tasks.list_all()
    #    tasks.write_tasks(tasks.get_tasks(), path)
    #elif args.change:
    #    tasks.change(args.change)
    #    tasks.list_all()
    #    tasks.write_tasks(tasks.get_tasks(), path)
    #elif args.finish:
    #    tasks.finish(args.finish)
    #    tasks.list_all()
    #    tasks.write_tasks(tasks.get_tasks(), path)
    #elif args.finish_all:
    #    tasks.finish_all()
    #    tasks.list_all()
    #    tasks.write_tasks(tasks.get_tasks(), path)
    #elif args.remove:
    #    tasks.remove(args.remove)
    #    tasks.ids.append(args.remove)
    #    tasks.list_all()
    #    tasks.write_tasks(tasks.get_tasks(), path)
    #elif args.remove_all:
    #    tasks.remove_all()
    #    tasks.list_all()
    #    tasks.write_tasks(tasks.get_tasks(), path)
    #elif args.unfinish:
    #    tasks.unfinish(args.unfinish)
    #    tasks.list_all()
    #    tasks.write_tasks(tasks.get_tasks(), path)
    #elif args.unfinish_all:
    #    tasks.unfinish_all()
    #    tasks.list_all()
    #    tasks.write_tasks(tasks.get_tasks(), path)
    #else:
    #    tasks.list_all()

    #unittest.main()
