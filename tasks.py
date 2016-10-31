#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import pathlib

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

    def __init__(self, name='tasklist', tasksdir='.'):
        self.name = name
        self.tasksdir = tasksdir
        self.tasks = {}
        self.limit = 99

    def get_name(self):
        return self.name

    def get_tasks(self):
        return self.tasks

    def get_tasksdir(self):
        return self.tasksdir

    def set_name(self, name):
        self.name = name

    def set_tasksdir(self, tasksdir):
        self.tasksdir = tasksdir

    def add(self, id_, text, status='unfinished'):
        if self.num_of_tasks <= self.limit:
            task = Task(id_, text, status)
            self.tasks[task.id_] = task
            self.num_of_tasks += 1

    def edit(self, id_):
        if id_ in self.tasks:
            text = input('enter change: ')
            self.tasks[id_].set_text(text)

    def finish(self, id_):
        if id_ in self.tasks:
            self.tasks[id_].set_status('finished')

    def finish_all(self):
        temp_dict = self.tasks.copy()
        for k in temp_dict:
            self.tasks[k].set_status('finished')

    def list_all(self):
        print('\n' + self.get_name().upper())
        print('=' * len(self.get_name()))
        if self.num_of_tasks == 0:
            print('No tasks')
        else:
            for k in self.tasks.keys():
                print('{:2}. [{}] {}'.format(self.tasks[k].get_id(),
                    'X' if self.tasks[k].get_status() == 'finished' else ' ',
                    self.tasks[k].get_text()))
        print('=' * len(self.get_name()), '\n')

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

    @classmethod
    def write_tasks(cls, tasks, path):
            if path.exists() and path.is_file():
                try:
                    with path.open('w') as f:
                        data = {}
                        for k in tasks:
                            data[tasks[k].get_id()] = {
                                'id':tasks[k].get_id(),
                                'text': tasks[k].get_text(),
                                'status': tasks[k].get_status()
                            }
                        json.dump(data, f, ensure_ascii=False, indent=2)
                        f.write('\n')
                except IOError:
                    # TODO: raise custom exception
                    pass
            else:
                # TODO: raise custom exception
                pass

    @classmethod
    def read_tasks(cls, tasks, path):
        if path.exists() and path.is_file():
            try:
                with path.open('r') as f:
                    data = json.load(f)
                    for k in data:
                        id_ = data[k]['id']
                        tasks.ids.remove(id_)
                        text = data[k]['text']
                        status = data[k]['status']
                        tasks.add(id_, text, status)
            except IOError:
                # TODO: raise BadPath exception
                pass
        else:
            # TODO: raise BadPath exception
            pass

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--add',
                help='add TASK to tasklist')
        parser.add_argument('-e', '--edit', type=int,
                help='edit TASK with specified id')
        parser.add_argument('-f', '--finish', type=int,
                help='mark TASK as finished')
        parser.add_argument('-F', '--finish-all', action='store_true',
                help='mark all TASKS as finished')
        parser.add_argument('-r', '--remove', type=int,
                help='remove TASK from tasklist')
        parser.add_argument('-R', '--remove-all', action='store_true',
                help='remove all TASKS from tasklist')
        parser.add_argument('-u', '--unfinish', type=int,
                help='mark TASK as unfinished')
        parser.add_argument('-U', '--unfinish-all', action='store_true',
                help='mark all TASKS as unfinished')
        return parser


if __name__ == '__main__':
    tasks = Tasklist()
    filename = tasks.get_name() + '.json'
    tasksdir = tasks.get_tasksdir()
    path = pathlib.Path().resolve().joinpath(tasksdir, filename)
    tasks.read_tasks(tasks, path)
    args = tasks.get_parser().parse_args()
    if args.add:
        id_ = tasks.ids[0]
        tasks.ids.remove(id_)
        tasks.add(id_, args.add)
        tasks.list_all()
        tasks.write_tasks(tasks.get_tasks(), path)
    elif args.edit:
        tasks.edit(args.edit)
        tasks.list_all()
        tasks.write_tasks(tasks.get_tasks(), path)
    elif args.finish:
        tasks.finish(args.finish)
        tasks.list_all()
        tasks.write_tasks(tasks.get_tasks(), path)
    elif args.finish_all:
        tasks.finish_all()
        tasks.list_all()
        tasks.write_tasks(tasks.get_tasks(), path)
    elif args.remove:
        tasks.remove(args.remove)
        tasks.ids.append(args.remove)
        tasks.list_all()
        tasks.write_tasks(tasks.get_tasks(), path)
    elif args.remove_all:
        tasks.remove_all()
        tasks.list_all()
        tasks.write_tasks(tasks.get_tasks(), path)
    elif args.unfinish:
        tasks.unfinish(args.unfinish)
        tasks.list_all()
        tasks.write_tasks(tasks.get_tasks(), path)
    elif args.unfinish_all:
        tasks.unfinish_all()
        tasks.list_all()
        tasks.write_tasks(tasks.get_tasks(), path)
    else:
        tasks.list_all()
