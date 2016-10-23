import sys

class Task(object):

    def __init__(self, task_id, task):
        self.task_id = task_id
        self.task = task
        self.status = 0

    def get_task_id(self):
        return self.task_id

    def get_task(self):
        return self.task

    def get_status(self):
        return self.status

    def set_id(self, task_id):
        self.task_id = task_id

    def set_task(self, task):
        self.task = task

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return '{:2} [{}] {}'.format(self.task_id,
                                    'X' if self.status else ' ',
                                    self.task)

class Tasklist(object):

    task_id = 1
    tasks_total = 0

    def __init__(self, name='Tasks'):
        self.name = name
        self.done = {}
        self.undone = {}

    def add(self, task_text):
        if self.tasks_total == 99:
            return
        task = Task(self.task_id, task_text)
        self.undone[task.task_id] = task
        self.task_id += 1
        self.tasks_total += 1

    def delete(self, task_id):
        if task_id in self.done.keys():
            self.done.pop(task_id)
            self.tasks_total -= 1
        elif task_id in self.undone.keys():
            self.undone.pop(task_id)
            self.tasks_total -= 1

    def change(self, task_id, task):
        if task_id in self.done.keys():
            self.done[task_id].set_task(task)
        elif task_id in self.undone.keys():
            self.undone[task_id].set_task(task)

    def do(self, task_id):
        if task_id in self.undone.keys():
            self.undone[task_id].set_status(1)
            self.done[task_id] = self.undone.pop(task_id)

    def undo(self, task_id):
        if task_id in self.done.keys():
            self.done[task_id].set_status(0)
            self.undone[task_id] = self.done.pop(task_id)

    def do_all(self):
        temp_dict = self.undone.copy()
        for k in temp_dict.keys():
            self.done[k] = self.undone.pop(k)
            self.done[k].set_status(1)

    def clear(self):
        self.done.clear()
        self.undone.clear()
        self.tasks_id = 1
        self.tasks_total = 0

    def undo_all(self):
        temp = self.done.copy()
        for k in temp:
            self.undone[k] = self.done.pop(k)
            self.undone[k].set_status(0)

    def show(self):
        header = '{}: {}/{}'.format(self.name.upper(), self.tasks_total, 99)
        print('\n' + header)
        print('=' * len(header))
        if self.tasks_total == 0:
            print('No tasks')
        else:
            for k in self.done.keys():
                print(self.done[k])
            for k in self.undone.keys():
                print(self.undone[k])
        print('=' * len(header) + '\n')

def main():
    tasks = Tasklist()
    tasks.show()

if __name__ == '__main__':
    main()
