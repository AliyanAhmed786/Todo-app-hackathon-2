# Data Model: Todo Console Application

## Task Entity

### Fields
- **id**: Integer (auto-incrementing, unique, required)
  - Starts from 1 and never recycles after deletion
  - Primary identifier for each task
- **title**: String (1-200 characters, required, non-whitespace)
  - Cannot consist of only whitespace characters
  - Must be between 1-200 characters
- **description**: String (0-1000 characters, optional)
  - Can be empty (0 characters)
  - Maximum 1000 characters
- **status**: String ("incomplete" or "complete", required)
  - Default value: "incomplete"
  - Only two valid values
- **created_date**: DateTime (timestamp, required)
  - Automatically set when task is created

### Validation Rules
1. Title must be 1-200 characters
2. Title cannot consist of only whitespace characters
3. Description must be 0-1000 characters
4. Status must be either "incomplete" or "complete"
5. ID must be unique and auto-incrementing
6. ID never recycles after deletion

### State Transitions
- **incomplete** → **complete**: When user marks task as complete
- **complete** → **incomplete**: When user marks complete task as incomplete

### Relationships
- No relationships with other entities (standalone entity)

## Task Service Operations

### Available Operations
1. **Create Task**: Add new task with title, optional description, default status "incomplete"
2. **Get All Tasks**: Retrieve all tasks in the system
3. **Get Task by ID**: Retrieve specific task by its ID
4. **Update Task**: Modify title or description of existing task
5. **Toggle Status**: Change task status between "incomplete" and "complete"
6. **Delete Task**: Remove task by ID (ID not reused)

### Business Rules
1. Duplicate titles are allowed
2. Task IDs never recycle after deletion
3. All operations must provide appropriate success/error messages
4. Delete operations require user confirmation