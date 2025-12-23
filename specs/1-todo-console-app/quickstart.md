# Quickstart Guide: Todo Console Application

## Prerequisites
- Python 3.13+ installed on your system

## Setup Instructions

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Navigate to the project directory**:
   ```bash
   cd <project-root>
   ```

3. **Run the application**:
   ```bash
   python src/main.py
   ```

## Running the Application

The application will start and display the main menu:

```
Todo Console Application
========================
1. Add Task
2. View Task List
3. Mark as Complete
4. Update Task
5. Delete Task
6. Exit Application

Enter your choice (1-6):
```

## Basic Usage

### Adding a Task
1. Select option `1` from the menu
2. Enter a title (1-200 characters, not only whitespace)
3. Optionally enter a description (0-1000 characters)
4. The system will create the task and display a success message

### Viewing Tasks
1. Select option `2` from the menu
2. All tasks will be displayed with ID, title, description, and status

### Marking as Complete
1. Select option `3` from the menu
2. Enter the task ID you want to mark
3. The system will toggle the task status and display a success message

### Updating a Task
1. Select option `4` from the menu
2. Enter the task ID you want to update
3. Enter new title or description
4. The system will update the task and display a success message

### Deleting a Task
1. Select option `5` from the menu
2. Enter the task ID you want to delete
3. Confirm deletion by entering `Y`
4. The system will delete the task and display a success message

### Exiting
- Select option `6` from the menu to exit the application

## Error Handling

- Invalid inputs will display appropriate error messages
- Non-existent task IDs will display "Task not found" messages
- Invalid titles (empty, too long, whitespace only) will be rejected
- Delete confirmation prevents accidental deletions