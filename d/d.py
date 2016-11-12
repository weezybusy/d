#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

    def change(self, id_, text):
        if id_ in self.tasks:
            task = self.tasks[id_]
            task.set_text(text)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit(1)

    def finish(self, id_):
        if id_ in self.tasks:
            task = self.tasks[id_]
            task.set_status(1)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit(1)

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
            sys.exit(1)

    def remove_all(self):
        self.tasks.clear()

    def undo(self, id_):
        if id_ in self.tasks:
            task = self.tasks[id_]
            task.set_status(0)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit(1)

    def undo_all(self):
        for task in self.tasks.values():
            task.set_status(0)

    def read(self, taskfile):
        if taskfile.stat().st_size > 0:
            try:
                with taskfile.open('r') as f:
                    try:
                        data = json.load(f)
                        for task in data.values():
                            self.add(
                                    task['text'],
                                    task['id'],
                                    task['status']
                            )
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
