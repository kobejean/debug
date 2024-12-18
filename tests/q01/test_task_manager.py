
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
    # After running complete_task "Parent Task" should be complete
    assert manager.tasks[0].completed == True
    # After running complete_task "Subtask" should also be complete
    assert manager.tasks[0].subtasks[0].completed == True

def test_add_subtask():
    manager = TaskManager()
    manager.add_task("Parent Task", 2)
    subtask = manager.add_subtask("Parent Task", "Subtask")
    # "Parent Task" should have just one subtask
    assert len(manager.tasks[0].subtasks) == 1
    # "Subtask" should have title "Subtask"
    assert manager.tasks[0].subtasks[0].title == "Subtask"
    # "Subtask" should inherit priority from "Parent Task" which is 2
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
    # parent priority same because it already has smaller value
    assert manager.tasks[0].priority == 1 

def test_delete_task():
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.add_subtask("Task 2", "Subtask")
    assert manager.delete_task("Task 1") == True
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Task 2"

# HARD

def test_delete_subtask():
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.add_subtask("Task 2", "Subtask")
    assert manager.delete_task("Subtask") == True
    assert len(manager.tasks[1].subtasks) == 0

def test_add_subtask_to_subtask():
    manager = TaskManager()
    manager.add_task("Parent Task", 2)
    subtask1 = manager.add_subtask("Parent Task", "Subtask 1")
    subtask2 = manager.add_subtask("Subtask 1", "Subtask 2")

    assert len(manager.tasks[0].subtasks) == 1
    assert manager.tasks[0].subtasks[0].title == "Subtask 1"
    assert manager.tasks[0].subtasks[0].priority == 2
    assert len(manager.tasks[0].subtasks[0].subtasks) == 1
    assert manager.tasks[0].subtasks[0].subtasks[0].title == "Subtask 2"
    assert manager.tasks[0].subtasks[0].subtasks[0].priority == 2

def test_change_priority_propagate():
    manager = TaskManager()
    manager.add_task("Task", 3)
    manager.add_subtask("Task", "Subtask")
    manager.change_priority("Subtask", 1)
    assert manager.tasks[0].subtasks[0].priority == 1
    # parent priority should change to 1 value because Subtask was changed to 1 which is lower than 3
    assert manager.tasks[0].priority == 1 

def test_get_incomplete_tasks_nested1():
    manager = TaskManager()
    manager.add_task("Task 1", 3)
    manager.add_task("Task 2", 1)
    manager.add_subtask("Task 1", "Subtask 1")
    manager.complete_task("Subtask 1")
    incomplete = manager.get_incomplete_tasks()
    assert len(incomplete) == 2
    assert incomplete[0].title == "Task 2" # lower priority value first
    assert incomplete[1].title == "Task 1"


def test_get_incomplete_tasks_nested2():
    manager = TaskManager()
    manager.add_task("Task 1", 3)
    manager.add_task("Task 2", 1)
    manager.add_subtask("Task 1", "Subtask 1")
    manager.add_subtask("Subtask 1", "Subtask 2")
    manager.complete_task("Task 2")
    incomplete = manager.get_incomplete_tasks()
    assert len(incomplete) == 3
    assert incomplete[0].title == "Task 1"
    assert incomplete[1].title == "Subtask 1"
    assert incomplete[2].title == "Subtask 2"


def test_get_incomplete_tasks_nested3():
    manager = TaskManager()
    manager.add_task("Task 1", 3)
    manager.add_task("Task 2", 1)
    manager.add_subtask("Task 1", "Subtask 1")
    manager.add_subtask("Subtask 1", "Subtask 2")
    manager.complete_task("Subtask 2")
    incomplete = manager.get_incomplete_tasks()
    assert len(incomplete) == 3
    assert incomplete[0].title == "Task 2"  # lower priority value first
    assert incomplete[1].title == "Task 1"
    assert incomplete[2].title == "Subtask 1"

def test_delete_subsubtask():
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.add_subtask("Task 2", "Subtask 1")
    manager.add_subtask("Subtask 1", "Subtask 2")
    manager.add_subtask("Subtask 1", "Subtask 3")
    assert manager.delete_task("Subtask 2") == True
    assert len(manager.tasks[1].subtasks) == 1
    assert len(manager.tasks[1].subtasks[0].subtasks) == 1
    assert manager.tasks[1].subtasks[0].subtasks[0].title == "Subtask 3"

def test_change_priority_propagate2():
    manager = TaskManager()
    manager.add_task("Task 1", 5)
    manager.add_task("Task 2", 4)
    manager.add_subtask("Task 2", "Subtask 1")
    manager.add_subtask("Subtask 1", "Subtask 2")
    manager.add_subtask("Subtask 1", "Subtask 3")
    manager.change_priority("Subtask 3", 3)
    # Subtask 3 changed
    assert manager.tasks[1].subtasks[0].subtasks[1].priority == 3
    # Subtask 2 unchanged
    assert manager.tasks[1].subtasks[0].subtasks[0].priority == 4
    # Subtask 1 changed
    assert manager.tasks[1].subtasks[0].priority == 3
    # Task 2 changed
    assert manager.tasks[1].priority == 3
    # Task 1 unchanged
    assert manager.tasks[0].priority == 5
