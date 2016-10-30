import argparse
import json
from pathlib import Path

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

    free_ids = [i for i in range(1, 100)]
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

    def get_free_id(self):
        return self.free_ids.pop(0)

    def get_free_ids_len(self):
        return len(self.free_ids)

    def set_name(self, name):
        self.name = name

    def set_tasksdir(self, tasksdir):
        self.tasksdir = tasksdir

    def return_id(self, id_):
        self.free_ids.append(id_)

    def add(self, id_, text, status='unfinished'):
        if self.num_of_tasks <= self.limit:
            task = Task(id_, text, status)
            self.tasks[task.id_] = task
            self.num_of_tasks += 1

    def remove(self, id_):
        if id_ in self.tasks:
            self.tasks.pop(id_)
            self.num_of_tasks -= 1
            self.return_id(id_)

    def remove_all(self):
        self.tasks.clear()
        self.free_ids = [i for i in range(1, 100)]
        self.num_of_tasks = 0

    def edit(self, id_, text):
        if id_ in self.tasks:
            self.tasks[id_].set_task(text)

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


def write_tasks(tasks, path):
        if path.exists() and path.is_file():
            try:
                with path.open('w') as f:
                    data = {}
                    for k in tasks:
                        data[tasks[k].get_id()] = {
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


def read_tasks(tasks, path):
    if path.exists() and path.is_file():
        try:
            with path.open('r') as f:
                data = json.load(f)
                for k in data:
                    tasks.add(int(k), data[k]['text'], data[k]['status'])
        except IOError:
            # TODO: raise BadPath exception
            pass
    else:
        # TODO: raise BadPath exception
        pass


def main():
    tasks = Tasklist()
    path = Path().resolve().joinpath(tasks.get_tasksdir(),
                                     tasks.get_name() + '.json')
    read_tasks(tasks, path)

    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--add', dest='add', type=str,
            help='add TASK to tasklist')

    parser.add_argument('-e', '--edit', dest='edit', nargs=2,
            help='edit TASK with specified id')

    parser.add_argument('-f', '--finish', dest='finish', type=int,
            help='mark TASK as finished')

    parser.add_argument('-F', '--finish-all', dest='finish-all',
            action='store_true', help='mark all TASKS as finished')

    parser.add_argument('-r', '--remove', dest='remove', type=int,
            help='remove TASK from tasklist')

    parser.add_argument('-R', '--remove-all', dest='remove-all',
            action='store_true', help='remove all TASKS from tasklist')

    parser.add_argument('-u', '--unfinish', dest='unfinish', type=int,
            help='mark TASK as unfinished')

    parser.add_argument('-U', '--unfinish-all', dest='unfinish-all',
            action='store_true', help='mark all TASKS as unfinished')

    args = parser.parse_args()

    if args.add:
        tasks.add(args.add)
        write_tasks(tasks.get_tasks(), path)
    elif args.finish:
        tasks.finish(args.finish)
        write_tasks(tasks.get_tasks(), path)
    elif args.finish_all:
        tasks.finish_all()
        write_tasks(tasks.get_tasks(), path)
    elif args.edit:
        tasks.edit(int(args.edit[0]), args.edit[1])
        write_tasks(tasks.get_tasks(), path)
    elif args.remove:
        tasks.remove(args.remove)
        write_tasks(tasks.get_tasks(), path)
    elif args.remove_all:
        tasks.remove_all()
        write_tasks(tasks.get_tasks(), path)
    elif args.unfinish:
        tasks.unfinish(args.unfinish)
        write_tasks(tasks.get_tasks(), path)
    elif args.unfinish_all:
        tasks.unfinish_all()
        write_tasks(tasks.get_tasks(), path)
    else:
        tasks.list_all()

    # TODO: finish parse options and make pretty output

if __name__ == '__main__':
    main()
