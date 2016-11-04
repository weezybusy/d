#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import pathlib

class Task(object):

    def __init__(self, id_=1, text='text', status=0):
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
        if id_ > 0:
            self.id_ = id_

    def set_text(self, text):
        self.text = text

    def set_status(self, status):
        if status in (0, 1):
            self.status = status


class Tasklist(object):

    ids = [i for i in range(1, 100)]
    num_of_tasks = 0

    def __init__(self):
        self.tasks = {}
        self.limit = 99

    def get_tasks(self):
        return self.tasks

    def add(self, text, id_=None, status=0):
        if self.num_of_tasks <= self.limit:
            if id_ is None:
                if self.ids:
                    id_ = self.ids.pop(0)
            else:
                if id_ in self.ids:
                    self.ids.remove(id_)
            if id_ is not None:
                task = Task(id_, text, status)
                self.tasks[task.id_] = task
                self.num_of_tasks += 1
        else:
            print('\nExceeded {N} tasks limit.\n'.format(N=self.limit))

    def change(self, id_):
        if id_ in self.tasks:
            text = input('text: ')
            self.tasks[id_].set_text(text)
            return True
        else:
            print('\nNo task with id {N}.\n'.format(N=id_))
            return False

    def finish(self, id_):
        if id_ in self.tasks:
            self.tasks[id_].set_status(1)
            return True
        else:
            print('\nNo task with id {N}.\n'.format(N=id_))
            return False

    def finish_all(self):
        for t in self.tasks:
            self.tasks[t].set_status(1)

    def list_all(self):
        if self.num_of_tasks:
            print('')
            for t in self.tasks:
                id_ = self.tasks[t].get_id()
                text = self.tasks[t].get_text()
                status = self.tasks[t].get_status()
                print('{id_:2}. [{status}] {text}'.format(
                    id_=id_,
                    status='X' if status else ' ',
                    text=text
                ))
            print('')
        else:
            print('\nTask list is empty.\n')

    def remove(self, id_):
        if id_ in self.tasks:
            self.tasks.pop(id_)
            self.ids.append(id_)
            self.num_of_tasks -= 1
            return True
        else:
            print('\nNo task with id {N}.\n'.format(N=id_))
            return False

    def remove_all(self):
        self.tasks.clear()
        self.num_of_tasks = 0
        self.ids = [i for i in range(1, 100)]

    def unfinish(self, id_):
        if id_ in self.tasks:
            self.tasks[id_].set_status(0)
            return True
        else:
            print('\nNo task with id {N}.\n'.format(N=id_))
            return False

    def unfinish_all(self):
        for t in self.tasks:
            self.tasks[t].set_status(0)


def write_tasks(tasks, taskfile):
    try:
        with taskfile.open('w') as f:
            data = {}
            ts = tasks.get_tasks()
            for t in ts:
                id_ = ts[t].get_id()
                text = ts[t].get_text()
                status = ts[t].get_status()
                data[id_] = {
                    'id': id_,
                    'text': text,
                    'status': status
                }
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(e)


def read_tasks(tasks, taskfile):
    if taskfile.stat().st_size > 0:
        try:
            with taskfile.open('r') as f:
                try:
                    data = json.load(f)
                    for k in data:
                        id_ = data[k]['id']
                        text = data[k]['text']
                        status = data[k]['status']
                        tasks.add(text, id_, status)
                except ValueError as e:
                    print(e)
        except IOError as e:
            print(e)


def get_parser():
    usage = 'do [-hlFRU] [--init] [-a TASK] [-cfru ID]'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-a', '--add', dest='add',
            help='add TASK to tasklist', metavar='TASK')
    parser.add_argument('-c', '--change', dest='change', type=int,
            help='change task with specified ID', metavar='ID')
    parser.add_argument('-f', '--finish', dest='finish', type=int,
            help='mark task with specified ID as finished', metavar='ID')
    parser.add_argument('-F', '--finish-all', dest='finish_all',
            action='store_true', help='mark all tasks as finished')
    parser.add_argument('--init', dest='init', action='store_true',
            help='create task list in current working directory')
    parser.add_argument('-l', '--list-all', dest='list_all',
            action='store_true', help='list all tasks')
    parser.add_argument('-r', '--remove', dest='remove', type=int,
            help='remove task with specified ID', metavar='ID')
    parser.add_argument('-R', '--remove-all', dest='remove_all',
            action='store_true', help='remove all tasks')
    parser.add_argument('-u', '--unfinish', dest='unfinish', type=int,
            help='mark task with specified ID as unfinished', metavar='ID')
    parser.add_argument('-U', '--unfinish-all', dest='unfinish_all',
            action='store_true', help='mark all tasks as unfinished')
    return parser


def main():
    args = get_parser().parse_args()
    taskfile = pathlib.Path().resolve().joinpath('todo.json')

    if args.init:
        taskfile.touch()
        print('\nTask list has been successfully created.\n' \
              'Type do -a <task> to add task.\n'             \
              'Type do -h to see all available options.\n')

    if taskfile.exists():
        tasks = Tasklist()
        read_tasks(tasks, taskfile)
        if args.add:
            text = args.add
            tasks.add(text)
            write_tasks(tasks, taskfile)
        if args.change:
            id_ = args.change
            if tasks.change(id_):
                write_tasks(tasks, taskfile)
        if args.finish:
            id_ = args.finish
            if tasks.finish(id_):
                write_tasks(tasks, taskfile)
        if args.finish_all:
            tasks.finish_all()
            write_tasks(tasks, taskfile)
        if args.remove:
            id_ = args.remove
            if tasks.remove(id_):
                write_tasks(tasks, taskfile)
        if args.remove_all:
            tasks.remove_all()
            write_tasks(tasks, taskfile)
        if args.unfinish:
            id_ = args.unfinish
            if tasks.unfinish(id_):
                write_tasks(tasks, taskfile)
        if args.unfinish_all:
            tasks.unfinish_all()
            write_tasks(tasks, taskfile)
        if args.list_all:
            tasks.list_all()
    else:
        print('\nType do --init to create task list.\n')


if __name__ == '__main__':
    main()
