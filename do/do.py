#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import pathlib
import sys

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

    def __init__(self):
        self.tasks = {}
        self.ids = [i for i in range(1, 100)]

    def add(self, text, id_=None, status=0):
        if self.ids:
            if id_ is None:
                id_ = self.ids.pop(0)
            else:
                if id_ in self.ids:
                    self.ids.remove(id_)
            task = Task(id_, text, status)
            self.tasks[id_] = task
        else:
            print('Exceeded {N} tasks limit.'.format(N=99))

    def change(self, id_):
        if id_ in self.tasks:
            text = input('text: ')
            task = self.tasks[id_]
            task.set_text(text)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit()

    def finish(self, id_):
        if id_ in self.tasks:
            task = self.tasks[id_]
            task.set_status(1)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit()

    def finish_all(self):
        for task in self.tasks.values():
            task.set_status(1)

    def list_all(self):
        if len(self.ids) < 99:
            for task in self.tasks.values():
                print('{id_:2}. [{status}] {text}'.format(
                    id_=task.get_id(),
                    status='X' if task.get_status() else ' ',
                    text=task.get_text()
                ))
        else:
            print('Task list is empty.')

    def remove(self, id_):
        if id_ in self.tasks:
            self.tasks.pop(id_)
            self.ids.append(id_)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit()

    def remove_all(self):
        self.tasks.clear()

    def unfinish(self, id_):
        if id_ in self.tasks:
            task = self.tasks[id_]
            task.set_status(0)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit()

    def unfinish_all(self):
        for task in self.tasks.values():
            task.set_status(0)

    def read(self, taskfile):
        if taskfile.stat().st_size > 0:
            try:
                with taskfile.open('r') as f:
                    try:
                        data = json.load(f)
                        for k in data:
                            id_ = data[k]['id']
                            text = data[k]['text']
                            status = data[k]['status']
                            self.add(text, id_, status)
                    except ValueError as e:
                        print(e)
            except IOError as e:
                print(e)

    def write(self, taskfile):
        try:
            with taskfile.open('w') as f:
                data = {}
                for task in self.tasks.values():
                    id_ = task.get_id()
                    text = task.get_text()
                    status = task.get_status()
                    data[id_] = {
                        'id': id_,
                        'text': text,
                        'status': status
                    }
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(e)


def get_parser():
    usage = 'do [--init] | [-a TASK] [-cfru ID] [-hlFRU]'
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
        print('Task list has been successfully created.\n' \
              'Type do -a <task> to add task.\n'           \
              'Type do -h to see all available options.')
    elif taskfile.exists():
        tasks = Tasklist()
        tasks.read(taskfile)
        if args.add:
            text = args.add
            tasks.add(text)
        if args.change:
            id_ = args.change
            tasks.change(id_)
        if args.finish:
            id_ = args.finish
            tasks.finish(id_)
        if args.finish_all:
            tasks.finish_all()
        if args.remove:
            id_ = args.remove
            tasks.remove(id_)
        if args.remove_all:
            tasks.remove_all()
        if args.unfinish:
            id_ = args.unfinish
            tasks.unfinish(id_)
        if args.unfinish_all:
            tasks.unfinish_all()
        tasks.write(taskfile)
        if args.list_all:
            tasks.list_all()
    else:
        print('Type do --init to create task list.')


if __name__ == '__main__':
    main()