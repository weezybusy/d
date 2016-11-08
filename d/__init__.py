#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import d
import pathlib

def get_args():
    parser = argparse.ArgumentParser(
            description='A simple CLI task management tool',
            usage='%(prog)s [--init] | [-a TASK] [-c ID] [-fru ID ...] [-hlFRU]',
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog,
                indent_increment=2,
                max_help_position=45,
                width=90
            )
    )
    parser.add_argument('-a', '--add', dest='add', nargs='+',
            action='append', help='add TASK to task list', metavar='TASK')
    parser.add_argument('-c', '--change', dest='change', type=int,
            help='change task with specified ID', metavar='ID')
    parser.add_argument('-f', '--finish', dest='finish', type=int, nargs='+',
            help='finish task(s) with specified ID(s)',
            metavar='ID')
    parser.add_argument('-F', '--finish-all', dest='finish_all',
            action='store_true', help='mark all tasks as finished')
    parser.add_argument('--init', dest='init', action='store_true',
            help='create task list in current directory')
    parser.add_argument('-l', '--list-all', dest='list_all',
            action='store_true', help='list all tasks')
    parser.add_argument('-r', '--remove', dest='remove', type=int, nargs='+',
            help='remove task(s) with specified ID(s)', metavar='ID')
    parser.add_argument('-R', '--remove-all', dest='remove_all',
            action='store_true', help='remove all tasks')
    parser.add_argument('-u', '--undo', dest='undo', type=int,
            nargs='+', help='reset task(s) with specified ID(s)',
            metavar='ID')
    parser.add_argument('-U', '--undo-all', dest='undo_all',
            action='store_true', help='mark all tasks as unfinished')
    return parser.parse_args()


def main():
    args = get_args()
    taskfile = pathlib.Path().resolve().joinpath('todo.json')
    if args.init:
        taskfile.touch()
        print('Task list has been successfully created.\n'
              'Type do -a <task> to add first task.\n'
              'Type do -h to see all available options.')
    elif taskfile.exists():
        tasks = d.Tasklist()
        tasks.read(taskfile)
        if args.add:
            for a in args.add:
                text = ' '.join(a)
                tasks.add(text)
        if args.change:
            id_ = args.change
            tasks.change(id_)
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
        if args.undo:
            for id_ in args.undo:
                tasks.undo(id_)
        if args.undo_all:
            tasks.undo_all()
        tasks.write(taskfile)
        if args.list_all:
            tasks.list_all()
    else:
        print('Type do --init to create task list.')
