#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import d
import argparse
import pathlib
import sys

def get_args():
    parser = argparse.ArgumentParser(
            description='A simple CLI task management tool',
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog,
                max_help_position=35,
            )
    )
    parser.add_argument('-a', dest='add', nargs='+', action='append',
            help='add TASK to task list', metavar='TASK')
    parser.add_argument('-c', dest='change', nargs='+',
            help='change task with specified ID', metavar='(ID, TASK)')
    parser.add_argument('-f', dest='finish', type=int, nargs='+',
            help='finish task(s) with specified ID(s)', metavar='ID')
    parser.add_argument('-F', dest='finish_all', action='store_true',
            help='mark all tasks as finished')
    parser.add_argument('--init', dest='init', action='store_true',
            help='create task list in current directory')
    parser.add_argument('-l', dest='list_all', action='store_true',
            help='list all tasks')
    parser.add_argument('-r', dest='remove', type=int, nargs='+',
            help='remove task(s) with specified ID(s)', metavar='ID')
    parser.add_argument('-R', dest='remove_all', action='store_true',
            help='remove task list')
    parser.add_argument('-u', dest='undo', type=int, nargs='+',
            help='reset task(s) with specified ID(s)', metavar='ID')
    parser.add_argument('-U', dest='undo_all', action='store_true',
            help='mark all tasks as unfinished')
    return parser.parse_args()


def main():
    args = get_args()
    taskfile = pathlib.Path().resolve().joinpath('todo.json')
    if args.init:
        if not taskfile.exists():
            taskfile.touch()
            print('Task list has been successfully created.')
        else:
            print('Task list already exists.')
    elif taskfile.exists():
        tasks = d.Tasklist()
        tasks.read(taskfile)
        if args.add:
            for a in args.add:
                text = ' '.join(a)
                tasks.add(text)
        if args.change:
            try:
                id_ = int(args.change[0])
                text = ' '.join(args.change[1:])
                tasks.change(id_, text)
            except ValueError:
                print('Invalid task id type.')
        if args.finish:
            for id_ in args.finish:
                tasks.finish(id_)
        if args.finish_all:
            tasks.finish_all()
        if args.remove:
            for id_ in args.remove:
                tasks.remove(id_)
        if args.remove_all:
            tasks.remove_all()
            taskfile.unlink()
            sys.exit(0)
        if args.undo:
            for id_ in args.undo:
                tasks.undo(id_)
        if args.undo_all:
            tasks.undo_all()
        tasks.write(taskfile)
        if args.list_all:
            tasks.list_all()
    else:
        print('Type  d --init  to create task list.')
