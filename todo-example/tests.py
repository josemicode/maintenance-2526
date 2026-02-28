import unittest

from ToDoItem import ToDoItem


class TestToDoItem(unittest.TestCase):
    def setUp(self):
        self.item_completed = ToDoItem("Task Completed")
        self.item_completed.toggle()
        self.item_not_completed = ToDoItem("Task Completed", 5)
        self.item_top_priority = ToDoItem("Task Completed", 10)

    def test_increment_priority(self):
        self.item_not_completed.increment_priority()
        self.assertEqual(self.item_not_completed.get_priority(), 6)

        self.item_top_priority.increment_priority()
        self.assertEqual(self.item_top_priority.get_priority(), 10)

        for i in range(15):
            self.item_completed.increment_priority()
        self.assertEqual(self.item_completed.get_priority(), 10)
