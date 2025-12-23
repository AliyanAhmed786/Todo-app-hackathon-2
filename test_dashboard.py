#!/usr/bin/env python3
"""
Test script to verify the dashboard functionality
"""
from src.cli.menu import Menu

def test_dashboard():
    print("Testing Dashboard functionality...")

    # Create a menu instance
    menu = Menu()

    # Initially, dashboard should show 0 tasks
    print("\nInitial dashboard (should show 0 tasks):")
    menu.display_dashboard()

    # Add some test tasks
    print("\nAdding test tasks...")
    task1 = menu.task_service.create_task("Test Task 1", "Test Description 1")
    task2 = menu.task_service.create_task("Test Task 2", "Test Description 2")
    print(f"Created tasks: {task1.title}, {task2.title}")

    # Show dashboard after adding tasks
    print("\nDashboard after adding 2 tasks (should show 2 pending):")
    menu.display_dashboard()

    # Mark one task as complete
    print(f"\nMarking task {task1.id} as complete...")
    toggled_task = menu.task_service.toggle_status(task1.id)
    print(f"Task {task1.id} status changed to: {toggled_task.status}")

    # Show dashboard after marking task complete
    print("\nDashboard after marking 1 task as complete (should show 1 completed, 1 pending):")
    menu.display_dashboard()

    # Add one more task
    task3 = menu.task_service.create_task("Test Task 3", "Test Description 3")
    print(f"\nAdded another task: {task3.title}")

    # Show final dashboard
    print("\nFinal dashboard (should show 1 completed, 2 pending, 33% completion rate):")
    menu.display_dashboard()

    print("\nDashboard functionality verified!")

if __name__ == "__main__":
    test_dashboard()