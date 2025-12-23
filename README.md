# Todo Console Application

A simple command-line todo application that allows users to manage personal tasks through a menu-driven interface.

## Features

- Add tasks with title and optional description
- View all tasks with their status
- Mark tasks as complete/incomplete
- Update task title or description
- Delete tasks with confirmation
- In-memory storage (data persists only during current session)

## Requirements

- Python 3.13+

## Setup

1. Clone the repository
2. Navigate to the project directory
3. Run the application using Python:

```bash
python src/main.py
```

## Usage

The application presents a menu with 6 options:

1. **Add Task**: Create a new task with a title and optional description
2. **View Task List**: Display all tasks with their ID, status, title, and description
3. **Mark as Complete**: Toggle a task's status between complete/incomplete
4. **Update Task**: Modify an existing task's title or description
5. **Delete Task**: Remove a task with confirmation prompt
6. **Exit Application**: Quit the application

## Validation Rules

- Task title: 1-200 characters, cannot be only whitespace
- Task description: 0-1000 characters
- Task status: either "incomplete" or "complete"

## Testing

To run the tests:

```bash
pytest tests/
```

## Project Structure

```
src/
├── models/
│   └── task.py          # Task entity with validation
├── services/
│   └── task_service.py  # Business logic for task operations
├── cli/
│   └── menu.py          # Menu-driven interface implementation
└── main.py              # Application entry point

tests/
├── unit/
│   ├── test_task.py     # Unit tests for Task model
│   └── test_task_service.py  # Unit tests for task service
└── integration/
    └── test_cli.py      # Integration tests for CLI interface
```