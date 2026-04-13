import unittest
from datetime import datetime, timedelta

from models import Task, TaskPriority, TaskStatus
from task_priority import calculate_task_score, sort_tasks_by_importance, get_top_priority_tasks


class TestTaskPriority(unittest.TestCase):
    def test_calculate_task_score_overdue_urgent(self):
        task = Task(
            title="Fix bug",
            priority=TaskPriority.URGENT,
            due_date=datetime.now() - timedelta(days=1),
            tags=["urgent", "backend"]
        )
        score = calculate_task_score(task)
        self.assertGreater(score, 0)
        self.assertTrue(score >= 6 * 10 + 35 + 8)

    def test_calculate_task_score_done_reduces_score(self):
        task = Task(title="Write docs", priority=TaskPriority.HIGH)
        task.mark_as_done()
        score = calculate_task_score(task)
        self.assertLess(score, 0)

    def test_sort_tasks_by_importance(self):
        urgent_task = Task("Urgent task", priority=TaskPriority.URGENT)
        high_task = Task("High task", priority=TaskPriority.HIGH)
        sorted_tasks = sort_tasks_by_importance([high_task, urgent_task])
        self.assertEqual(sorted_tasks[0].title, "Urgent task")

    def test_get_top_priority_tasks_limit(self):
        tasks = [
            Task("Task 1", priority=TaskPriority.LOW),
            Task("Task 2", priority=TaskPriority.MEDIUM),
            Task("Task 3", priority=TaskPriority.HIGH)
        ]
        top_tasks = get_top_priority_tasks(tasks, limit=2)
        self.assertEqual(len(top_tasks), 2)
        self.assertEqual(top_tasks[0].priority, TaskPriority.HIGH)


if __name__ == "__main__":
    unittest.main()
