#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import task
import json
import sys

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
            tsk = task.Task(id_, text, status)
            self.tasks[id_] = tsk
        else:
            print('Exceeded {N} tasks limit.'.format(N=99))

    def change(self, id_, text):
        if id_ in self.tasks:
            tsk = self.tasks[id_]
            tsk.set_text(text)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit(1)

    def finish(self, id_):
        if id_ in self.tasks:
            tsk = self.tasks[id_]
            tsk.set_status(1)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit(1)

    def finish_all(self):
        for tsk in self.tasks.values():
            tsk.set_status(1)

    def list_all(self):
        if len(self.ids) < 99:
            for tsk in self.tasks.values():
                print('{id_:2}. [{status}] {text}'.format(
                    id_=tsk.get_id(),
                    status='X' if tsk.get_status() else ' ',
                    text=tsk.get_text()
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
            tsk = self.tasks[id_]
            tsk.set_status(0)
        else:
            print('No task with id {N}.'.format(N=id_))
            sys.exit(1)

    def undo_all(self):
        for tsk in self.tasks.values():
            tsk.set_status(0)

    def read(self, taskfile):
        if taskfile.stat().st_size > 0:
            try:
                with taskfile.open('r') as f:
                    try:
                        data = json.load(f)
                        for tsk in data.values():
                            self.add(
                                    tsk['text'],
                                    tsk['id'],
                                    tsk['status']
                            )
                    except ValueError as e:
                        print(e)
            except IOError as e:
                print(e)

    def write(self, taskfile):
        try:
            with taskfile.open('w') as f:
                data = {}
                for tsk in self.tasks.values():
                    id_ = tsk.get_id()
                    text = tsk.get_text()
                    status = tsk.get_status()
                    data[id_] = {
                            'id': id_,
                            'text': text,
                            'status': status
                    }
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(e)
