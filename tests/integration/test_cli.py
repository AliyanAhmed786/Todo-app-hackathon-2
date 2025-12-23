import pytest
from unittest.mock import patch, MagicMock
from src.cli.menu import Menu


class TestCLIMenu:
    def test_add_task_success(self):
        """Test successful task addition via CLI."""
        menu = Menu()

        # Patch input to simulate user input
        with patch('builtins.input', side_effect=['Test Title', 'Test Description']):
            with patch('builtins.print') as mock_print:
                menu.add_task()

                # Check that success message was printed
                mock_print.assert_called()
                # Verify a success message was printed (the exact call depends on the implementation)
                success_calls = [call for call in mock_print.call_args_list if 'created successfully' in str(call)]
                assert len(success_calls) > 0

    def test_add_task_with_empty_description(self):
        """Test adding a task with empty description."""
        menu = Menu()

        with patch('builtins.input', side_effect=['Test Title', '']):
            with patch('builtins.print') as mock_print:
                menu.add_task()

                # Check that success message was printed
                success_calls = [call for call in mock_print.call_args_list if 'created successfully' in str(call)]
                assert len(success_calls) > 0

    def test_add_task_whitespace_title_error(self):
        """Test adding a task with whitespace-only title (should fail)."""
        menu = Menu()

        with patch('builtins.input', side_effect=['   ', 'Test Description']):
            with patch('builtins.print') as mock_print:
                menu.add_task()

                # Check that error message was printed
                error_calls = [call for call in mock_print.call_args_list if 'cannot be only whitespace' in str(call)]
                assert len(error_calls) > 0

    def test_add_task_empty_title_error(self):
        """Test adding a task with empty title (should fail)."""
        menu = Menu()

        with patch('builtins.input', side_effect=['', 'Test Description']):
            with patch('builtins.print') as mock_print:
                menu.add_task()

                # Check that error message was printed
                error_calls = [call for call in mock_print.call_args_list if 'between 1-200 characters' in str(call)]
                assert len(error_calls) > 0

    def test_view_task_list_empty(self):
        """Test viewing an empty task list."""
        menu = Menu()

        with patch('builtins.print') as mock_print:
            menu.view_task_list()

            # Check that "No tasks found" message was printed
            no_tasks_calls = [call for call in mock_print.call_args_list if 'No tasks found' in str(call)]
            assert len(no_tasks_calls) > 0

    def test_view_task_list_with_tasks(self):
        """Test viewing a task list with tasks."""
        menu = Menu()

        # Add a task first
        menu.task_service.create_task("Test Title", "Test Description")

        with patch('builtins.print') as mock_print:
            menu.view_task_list()

            # Check that task information was printed
            task_calls = [call for call in mock_print.call_args_list if 'complete' in str(call) or 'incomplete' in str(call)]
            assert len(task_calls) > 0

    def test_view_task_list_format(self):
        """Test that tasks are displayed in the correct format."""
        menu = Menu()

        # Add a task first
        task = menu.task_service.create_task("Test Title", "Test Description")

        with patch('builtins.print') as mock_print:
            menu.view_task_list()

            # Check that the task was printed in the correct format
            task_calls = [call for call in mock_print.call_args_list if str(task.id) in str(call)]
            assert len(task_calls) > 0

    def test_mark_complete_toggle(self):
        """Test marking a task as complete."""
        menu = Menu()

        # Add a task first
        task = menu.task_service.create_task("Test Title")

        with patch('builtins.input', side_effect=[str(task.id)]):
            with patch('builtins.print') as mock_print:
                menu.mark_complete()

                # Check that success message was printed
                success_calls = [call for call in mock_print.call_args_list if 'marked as' in str(call)]
                assert len(success_calls) > 0

    def test_update_task_success(self):
        """Test updating a task successfully."""
        menu = Menu()

        # Add a task first
        task = menu.task_service.create_task("Original Title", "Original Description")

        with patch('builtins.input', side_effect=[str(task.id), 'New Title', 'New Description']):
            with patch('builtins.print') as mock_print:
                menu.update_task()

                # Check that success message was printed
                success_calls = [call for call in mock_print.call_args_list if 'updated successfully' in str(call)]
                assert len(success_calls) > 0

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        menu = Menu()

        # Add a task first
        task = menu.task_service.create_task("Test Title")

        with patch('builtins.input', side_effect=[str(task.id), 'Y']):
            with patch('builtins.print') as mock_print:
                menu.delete_task()

                # Check that success message was printed
                success_calls = [call for call in mock_print.call_args_list if 'deleted successfully' in str(call)]
                assert len(success_calls) > 0

    def test_delete_task_cancel(self):
        """Test canceling task deletion."""
        menu = Menu()

        # Add a task first
        task = menu.task_service.create_task("Test Title")

        with patch('builtins.input', side_effect=[str(task.id), 'N']):
            with patch('builtins.print') as mock_print:
                menu.delete_task()

                # Check that cancellation message was printed
                cancel_calls = [call for call in mock_print.call_args_list if 'deletion cancelled' in str(call)]
                assert len(cancel_calls) > 0

    def test_main_menu_loop_exit(self):
        """Test the main menu loop exit functionality."""
        menu = Menu()

        with patch.object(menu, 'display_menu'):  # Mock display_menu to avoid printing during test
            with patch('builtins.input', side_effect=['6']):  # '6' is exit option
                # This should not raise an exception and should exit the loop
                menu.run()