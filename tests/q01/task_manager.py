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
    
    def find_task(self, title):
        def find_subtask(task):
            if task.title == title:
                return task
            else:
                for subtask in task.subtasks:
                    found = find_subtask(subtask)
                    if found is not None:
                        return found
        for task in self.tasks:
            found = find_subtask(task)
            if found:
                return found
                
        
    def add_task(self, title, priority=1):
        task = Task(title, priority)
        self.tasks.append(task)
        return task
        
    def complete_task(self, title):
        found = self.find_task(title)
        def complete_subtasks(task):
            task.completed = True
            for subtask in task.subtasks:
                complete_subtasks(subtask)
        if found:
            complete_subtasks(found)
            return True
        return False
    
    def add_subtask(self, parent_title, subtask_title):
        found = self.find_task(parent_title)
        if found:
            subtask = Task(subtask_title, found.priority)
            found.subtasks.append(subtask)
            return subtask
        return None
    
    def get_incomplete_tasks(self):
        incomplete = []
        def incomplete_subtasks(task):
            if task.completed == False:
                incomplete.append(task)
                for subtask in task.subtasks:
                    incomplete_subtasks(subtask)
        for subtask in self.tasks:
            incomplete_subtasks(subtask)
        incomplete.sort(key=lambda task: task.priority)
        return incomplete
    
    def change_priority(self, title, new_priority):
        def change_priority_subtask(task):
            if task.title == title:
                task.priority = new_priority
                return task
            else:
                for subtask in task.subtasks:
                    found = change_priority_subtask(subtask)
                    if found is not None:
                        task.priority = min(task.priority, new_priority)
                        return found
        for task in self.tasks:
            found = change_priority_subtask(task)
            if found is not None:
                task.priority = min(task.priority, new_priority)
                return True
        return False
    
    def delete_task(self, title):

        def delete_subtask(task):
            if task.title == title:
                return task
            else:
                for i, subtask in enumerate(task.subtasks):
                    found = delete_subtask(subtask)
                    if found == True:
                        return found
                    if found:
                        del task.subtasks[i]
                        return True
        for i,task in enumerate(self.tasks):
            found = delete_subtask(task)
            if found == True:
                return found
            if found:
                del self.tasks[i]
                return True
        return False
