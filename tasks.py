from pathlib import Path
import json

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

    def set_name(self, name):
        self.name = name

    def add(self, text):
        if self.num_of_tasks <= self.limit and len(self.free_ids) != 0:
            id_ = self.free_ids.pop(0)
            task = Task(id_, text)
            self.tasks[task.id_] = task
            self.num_of_tasks += 1

    def remove(self, id_):
        if id_ in self.tasks:
            self.tasks.pop(id_)
            self.num_of_tasks -= 1
            self.free_ids.append(id_)

    def change(self, id_, text):
        if id_ in self.tasks:
            self.tasks[id_].set_task(text)

    def finish(self, id_):
        if id_ in self.tasks:
            self.tasks[id_].set_status('finished')

    def finish_all(self):
        temp_dict = self.tasks.copy()
        for k in temp_dict:
            self.tasks[k].set_status('finished')

    def clear_all(self):
        self.tasks.clear()
        self.free_ids = [i for i in range(1, 100)]
        self.num_of_tasks = 0

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


def write_tasks(tasks, f):
    ts = tasks.get_tasks()
    for k in ts:
        id_ = ts[k].get_id()
        text = ts[k].get_text()
        status = ts[k].get_status()
        data = json.dumps({id_: (text, status)}, ensure_ascii=False,
                                                 sort_keys=True)
        f.write(data + '\n')


def read_tasks(tasks, f):
    pass


def main():
    tasks = Tasklist()
    tasks.add('Math')
    tasks.add('Programming')
    tasks.add('Jogging')
    tasks.finish(1)
    tasks.finish(3)
    tasks.list_all()

    tasksdir = '.'
    path = Path().resolve().joinpath(tasksdir, tasks.get_name() + '.json')

    if path.is_dir():
        # TODO: raise custom exception
        pass
    else:
        if path.exists():
            try:
                with path.open('w') as f:
                    write_tasks(tasks, f)
            except IOError:
                # TODO: raise custom exception
                pass

    with path.open('r') as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            print(data)


if __name__ == '__main__':
    main()
