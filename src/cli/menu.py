from ..services.task_service import TaskService
from ..models.task import Task
from typing import Optional
from colorama import Fore, Style, init
from tabulate import tabulate

# Initialize colorama
init()


class Menu:
    def __init__(self):
        """
        Initialize the menu interface with a task service.
        """
        self.task_service = TaskService()

    def display_menu(self):
        """
        Display the main menu options.
        """
        print(f"\n{Fore.CYAN}+============================================+{Style.RESET_ALL}")
        print(f"{Fore.CYAN}|       TODO CONSOLE APPLICATION             |{Style.RESET_ALL}")
        print(f"{Fore.CYAN}|    Manage your tasks efficiently            |{Style.RESET_ALL}")
        print(f"{Fore.CYAN}|--------------------------------------------|{Style.RESET_ALL}")
        print(f"{Fore.CYAN}| 1  Add Task              Create a new task |{Style.RESET_ALL}")
        print(f"{Fore.CYAN}| 2  View Task List        Display all tasks |{Style.RESET_ALL}")
        print(f"{Fore.CYAN}| 3  Mark as Complete      Toggle task status|{Style.RESET_ALL}")
        print(f"{Fore.CYAN}| 4  Update Task           Modify task       |{Style.RESET_ALL}")
        print(f"{Fore.CYAN}| 5  Delete Task           Remove a task     |{Style.RESET_ALL}")
        print(f"{Fore.CYAN}| 6  Exit Application      Quit program      |{Style.RESET_ALL}")
        print(f"{Fore.CYAN}+============================================+{Style.RESET_ALL}")
        print()

    def get_user_choice(self) -> str:
        """
        Get user's menu choice.

        Returns:
            str: User's choice as a string
        """
        return input("Enter your choice (1-6): ").strip()

    def add_task(self):
        """
        Handle the Add Task functionality.
        """
        print(f"\n{Fore.CYAN}--- Add Task ---{Style.RESET_ALL}")
        original_title = input("Enter task title: ")
        title = original_title.strip()

        description_input = input("Enter task description (optional, press Enter to skip): ").strip()
        description = description_input if description_input else None

        # Check if original title was only whitespace (but not empty)
        if original_title and original_title.isspace():
            print(f"{Fore.RED}Title cannot be only whitespace characters{Style.RESET_ALL}")
            return

        try:
            task = self.task_service.create_task(title, description)
            print(f"{Fore.GREEN}Task #{task.id} created successfully{Style.RESET_ALL}")
        except ValueError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def view_task_list(self):
        """
        Handle the View Task List functionality.
        """
        print(f"\n{Fore.CYAN}--- View Task List ---{Style.RESET_ALL}")
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print(f"{Fore.YELLOW}No tasks found{Style.RESET_ALL}")
            return

        # Prepare data for tabulate
        table_data = []
        for task in tasks:
            status_symbol = "✓" if task.status == "complete" else " "
            status_display = f"[{status_symbol}] {task.status.title()}"
            description_display = task.description if task.description else ""
            table_data.append([task.id, status_display, task.title, description_display])

        # Display table using tabulate
        headers = ["ID", "Status", "Title", "Description"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        print(table)

    def mark_complete(self):
        """
        Handle the Mark as Complete functionality.
        """
        print(f"\n{Fore.CYAN}--- Mark as Complete ---{Style.RESET_ALL}")
        task_id_str = input("Enter task ID to mark as complete: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid task ID (number).{Style.RESET_ALL}")
            return

        task = self.task_service.get_task_by_id(task_id)
        if not task:
            print(f"{Fore.RED}Task not found{Style.RESET_ALL}")
            return

        updated_task = self.task_service.toggle_status(task_id)
        if updated_task:
            print(f"{Fore.GREEN}Task #{task_id} marked as {updated_task.status} successfully{Style.RESET_ALL}")

    def update_task(self):
        """
        Handle the Update Task functionality.
        """
        print(f"\n{Fore.CYAN}--- Update Task ---{Style.RESET_ALL}")
        task_id_str = input("Enter task ID to update: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid task ID (number).{Style.RESET_ALL}")
            return

        task = self.task_service.get_task_by_id(task_id)
        if not task:
            print(f"{Fore.RED}Task not found{Style.RESET_ALL}")
            return

        print(f"{Fore.CYAN}Current task: [{task.status}] {task.title}{Style.RESET_ALL}")
        if task.description:
            print(f"{Fore.CYAN}Description: {task.description}{Style.RESET_ALL}")

        new_title = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
        new_description = input(f"Enter new description (current: '{task.description or 'None'}', press Enter to keep current): ").strip()

        # Use None for empty string to keep current value
        title_to_update = new_title if new_title else None
        description_to_update = new_description if new_description else None

        # If user entered empty string explicitly to clear description
        if new_description == "":
            description_to_update = ""

        updated_task = self.task_service.update_task(task_id, title_to_update, description_to_update)
        if updated_task:
            print(f"{Fore.GREEN}Task #{task_id} updated successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to update task{Style.RESET_ALL}")

    def delete_task(self):
        """
        Handle the Delete Task functionality.
        """
        print(f"\n{Fore.CYAN}--- Delete Task ---{Style.RESET_ALL}")
        task_id_str = input("Enter task ID to delete: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid task ID (number).{Style.RESET_ALL}")
            return

        task = self.task_service.get_task_by_id(task_id)
        if not task:
            print(f"{Fore.RED}Task not found{Style.RESET_ALL}")
            return

        confirmation = input("Are you sure? (Y/N): ").strip().upper()
        if confirmation == "Y":
            if self.task_service.delete_task(task_id):
                print(f"{Fore.GREEN}Task #{task_id} deleted successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Failed to delete task{Style.RESET_ALL}")
        elif confirmation == "N":
            print(f"{Fore.YELLOW}Task deletion cancelled{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid input. Please enter Y or N.{Style.RESET_ALL}")

    def display_dashboard(self):
        """
        Display a dashboard with task statistics using colors and box format.
        """
        stats = self.task_service.get_statistics()

        # Calculate completion rate as percentage
        completion_rate = round(stats["completion_rate"])

        # Create the dashboard with colored ASCII box format
        print(f"\n{Fore.MAGENTA}+============================================+{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}|          TASKS OVERVIEW                    |{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}|--------------------------------------------|{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}| Total Tasks:      {Fore.WHITE}{stats['total_tasks']:>24} |{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}| Completed:        {Fore.GREEN}{stats['completed_tasks']:>24}  {Fore.GREEN}C{Style.RESET_ALL}     |")
        print(f"{Fore.MAGENTA}| Pending:          {Fore.YELLOW}{stats['pending_tasks']:>24}  {Fore.YELLOW}P{Style.RESET_ALL}     |")
        print(f"{Fore.MAGENTA}| Completion Rate:  {Fore.CYAN}{completion_rate:>22}%{Style.RESET_ALL}     |")
        print(f"{Fore.MAGENTA}+============================================+{Style.RESET_ALL}")

    def run(self):
        """
        Run the main application loop.
        """
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
                self.display_dashboard()
            elif choice == "2":
                self.view_task_list()
                self.display_dashboard()
            elif choice == "3":
                self.mark_complete()
                self.display_dashboard()
            elif choice == "4":
                self.update_task()
                self.display_dashboard()
            elif choice == "5":
                self.delete_task()
                self.display_dashboard()
            elif choice == "6":
                self.display_dashboard()  # Show final stats before exiting
                print("Exiting application...")
                break
            else:
                print("Invalid choice. Please enter a number between 1-6.")