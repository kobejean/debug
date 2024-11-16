# task_manager.py

class Task:
    def __init__(self, title, priority=1, completed=False):
        self.title = title
        self.priority = priority
        self.completed = completed
        self.subtasks = []

class TaskManager:
    def __init__(self):
        self.tasks = []
        
    def add_task(self, title, priority=1):
        task = Task(title, priority)
        self.tasks.append(task)
        return task
        
    def complete_task(self, title):
        for task in self.tasks:
            if task.title == title:
                task.completed = True
                # Bug 1: Doesn't mark subtasks as complete
                return True
        return False
    
    def add_subtask(self, parent_title, subtask_title):
        for task in self.tasks:
            if task.title == parent_title:
                # Bug 2: Doesn't inherit parent's priority
                subtask = Task(subtask_title, 1)
                task.subtasks.append(subtask)
                return subtask
        return None
    
    def get_incomplete_tasks(self):
        incomplete = []
        for task in self.tasks:
            if task.completed == False:
                incomplete.append(task)
            # Bug 3: Always adds subtasks regardless of completion status
            for subtask in task.subtasks:
                incomplete.append(subtask)
        # Bug 4: Returns list without sorting by priority
        return incomplete
    
    def change_priority(self, title, new_priority):
        for task in self.tasks:
            if task.title == title:
                # Bug 5: Doesn't validate priority value
                task.priority = new_priority
                return True
            # Bug 6: Missing subtask priority update
        return False
    
    def delete_task(self, title):
        for i, task in enumerate(self.tasks):
            if task.title == title:
                del self.tasks[i]
                return True
            for j, subtask in enumerate(task.subtasks):
                if subtask.title == title:
                    # Bug 7: Wrong index in subtask deletion
                    del task.subtasks[i]
                    return True
        return False

# test_task_manager.py

import pytest
from task_manager import TaskManager, Task

def test_add_task():
    manager = TaskManager()
    task = manager.add_task("Test Task", 2)
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Test Task"
    assert manager.tasks[0].priority == 2

def test_complete_task():
    manager = TaskManager()
    manager.add_task("Parent Task")
    manager.add_subtask("Parent Task", "Subtask")
    manager.complete_task("Parent Task")
    assert manager.tasks[0].completed == True
    assert manager.tasks[0].subtasks[0].completed == True

def test_add_subtask():
    manager = TaskManager()
    manager.add_task("Parent Task", 2)
    subtask = manager.add_subtask("Parent Task", "Subtask")
    assert len(manager.tasks[0].subtasks) == 1
    assert manager.tasks[0].subtasks[0].title == "Subtask"
    assert manager.tasks[0].subtasks[0].priority == 2

def test_get_incomplete_tasks():
    manager = TaskManager()
    manager.add_task("Task 1", 3)
    manager.add_task("Task 2", 1)
    manager.add_subtask("Task 1", "Subtask 1")
    manager.complete_task("Task 2")
    incomplete = manager.get_incomplete_tasks()
    assert len(incomplete) == 2
    assert incomplete[0].title == "Task 1"
    assert incomplete[1].title == "Subtask 1"

def test_change_priority():
    manager = TaskManager()
    manager.add_task("Task", 1)
    manager.add_subtask("Task", "Subtask")
    manager.change_priority("Subtask", 3)
    assert manager.tasks[0].subtasks[0].priority == 3
    assert manager.tasks[0].priority == 1

def test_delete_task():
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.add_subtask("Task 1", "Subtask")
    assert manager.delete_task("Task 1") == True
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Task 2"