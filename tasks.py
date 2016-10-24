import argparse
import sys

class Task(object):

    def __init__(self, task_id, task):
        self.task_id = task_id
        self.task = task

    def get_task_id(self):
        return self.task_id

    def get_task(self):
        return self.task

    def set_id(self, task_id):
        self.task_id = task_id

    def set_task(self, task):
        self.task = task


class Tasklist(object):

    task_id = 1
    num_of_tasks = 0

    def __init__(self, name='Tasks'):
        self.name = name
        self.done = {}
        self.undone = {}
        self.limit = 99

    def add_task(self, task_text):
        if self.num_of_tasks <= self.limit:
            task = Task(self.task_id, task_text)
            self.undone[task.task_id] = task
            self.task_id += 1
            self.num_of_tasks += 1

    def remove_task(self, task_id):
        if task_id in self.done.keys():
            self.done.pop(task_id)
            self.num_of_tasks -= 1
        if task_id in self.undone.keys():
            self.undone.pop(task_id)
            self.num_of_tasks -= 1

    def change_task(self, task_id, task):
        if task_id in self.done.keys():
            self.done[task_id].set_task(task)
        if task_id in self.undone.keys():
            self.undone[task_id].set_task(task)

    def do_task(self, task_id):
        if task_id in self.undone.keys():
            self.done[task_id] = self.undone.pop(task_id)

    def undo_task(self, task_id):
        if task_id in self.done.keys():
            self.undone[task_id] = self.done.pop(task_id)

    def do_all_tasks(self):
        temp_dict = self.undone.copy()
        for k in temp_dict.keys():
            self.done[k] = self.undone.pop(k)

    def undo_all_tasks(self):
        temp = self.done.copy()
        for k in temp:
            self.undone[k] = self.done.pop(k)

    def clear_all_tasks(self):
        self.done.clear()
        self.undone.clear()
        self.tasks_id = 1
        self.num_of_tasks = 0

    def list_all_tasks(self):
        header = '{}: {}/{}'.format(self.name.upper(),
                                    self.num_of_tasks,
                                    self.limit)
        print('\n' + header)
        print('=' * len(header))
        if self.num_of_tasks == 0:
            print('No tasks')
        else:
            for k in self.done.keys():
                print('{:2}. [X] {}'.format(self.done[k].task_id,
                                            self.done[k].task))
            for k in self.undone.keys():
                print('{:2}. [ ] {}'.format(self.undone[k].task_id,
                                            self.undone[k].task))
        print('=' * len(header) + '\n')


def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument('init', help='Create a task list in current directory')
    #args = parser.parse_args()
    #print(args.init)
    tasks = Tasklist()
    tasks.list_all_tasks()


if __name__ == '__main__':
    main()
