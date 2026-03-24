class ToDoItem(object):

    def __init__(self, description = "Undefined task", priority = 0):
        self.priority = priority
        self.completed = False
        self.description = description
    
    def increment_priority(self):
        self.priority = self.priority + 1#min(self.priority + 1,10)
    
    def decrement_priority(self):
        self.priority = min(self.priority - 1,0)
    
    def toggle(self):
        self.completed = not self.completed

    def get_priority(self):
        return self.priority
