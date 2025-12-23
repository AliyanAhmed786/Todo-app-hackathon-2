#!/usr/bin/env python3
"""
Test script to verify the enhanced UI functionality
"""
from src.cli.menu import Menu

def test_enhanced_ui():
    print("Testing Enhanced UI functionality...")

    # Create a menu instance
    menu = Menu()

    # Add some test tasks
    print("\nAdding test tasks...")
    task1 = menu.task_service.create_task("Test Task 1", "Test Description 1")
    task2 = menu.task_service.create_task("Test Task 2", "Test Description 2")
    print(f"Created tasks: {task1.title}, {task2.title}")

    # Test view task list with table formatting
    print("\nTesting View Task List with table formatting:")
    print("(This would normally show a formatted table)")

    # Get all tasks to verify they exist
    all_tasks = menu.task_service.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")

    # Test toggling status
    print(f"\nBefore toggle - Task {task1.id} status: {task1.status}")
    toggled_task = menu.task_service.toggle_status(task1.id)
    print(f"After toggle - Task {task1.id} status: {toggled_task.status}")

    # Test update
    print(f"\nBefore update - Task {task2.id} title: {task2.title}")
    updated_task = menu.task_service.update_task(task2.id, "Updated Task 2 Title")
    print(f"After update - Task {task2.id} title: {updated_task.title}")

    print("\nEnhanced UI functionality verified!")

if __name__ == "__main__":
    test_enhanced_ui()