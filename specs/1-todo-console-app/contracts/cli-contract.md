# CLI Contract: Todo Console Application

## Overview
This document describes the command-line interface contract for the Todo Console Application, defining the user interactions, inputs, outputs, and error handling.

## Menu Interface

### Main Menu Options
The application presents a menu with 6 numbered options:

1. **Add Task**
2. **View Task List**
3. **Mark as Complete**
4. **Update Task**
5. **Delete Task**
6. **Exit Application**

### Input Format
- User enters a number (1-6) to select a menu option
- Follow prompts for additional input as required by the selected option

## Operation Contracts

### 1. Add Task
**Input**:
- Menu selection: `1`
- Title (string, 1-200 chars, no whitespace-only)
- Optional Description (string, 0-1000 chars)

**Output**:
- Success: "Task #X created successfully"
- Error: Appropriate error message

**Validation**:
- Title must be 1-200 characters
- Title cannot be whitespace-only
- Description must be 0-1000 characters

### 2. View Task List
**Input**:
- Menu selection: `2`

**Output**:
- List of all tasks in format: `ID. [Status] Title - Description`
- If no tasks: "No tasks found"

### 3. Mark as Complete
**Input**:
- Menu selection: `3`
- Task ID (integer)

**Output**:
- Success: "Task #X marked as [status] successfully"
- Error: "Task not found" or other error message

### 4. Update Task
**Input**:
- Menu selection: `4`
- Task ID (integer)
- New title or description (as applicable)

**Output**:
- Success: "Task #X updated successfully"
- Error: "Task not found" or validation error

### 5. Delete Task
**Input**:
- Menu selection: `5`
- Task ID (integer)
- Confirmation: `Y` or `N`

**Output**:
- Success: "Task #X deleted successfully"
- Error: "Task not found" or other error message

**Confirmation Flow**:
- After entering ID, system prompts: "Are you sure? (Y/N)"
- User enters `Y` to confirm or `N` to cancel

### 6. Exit Application
**Input**:
- Menu selection: `6`

**Output**:
- Application terminates gracefully
- In-memory data is lost (as per specification)

## Error Handling Contract

### Standard Error Messages
- "Task not found" - when ID doesn't exist
- "Title cannot be only whitespace characters" - validation error
- "Invalid input" - when user enters invalid data
- "Invalid choice" - when user enters menu option outside 1-6 range

### Validation Error Messages
- "Title must be between 1-200 characters"
- "Description must be between 0-1000 characters"

## Data Format Contract

### Task Display Format
```
ID. [Status] Title - Description
```
Example: `1. [incomplete] Buy groceries - Weekly shopping list`

### Status Values
- "incomplete" - task not completed
- "complete" - task completed

## Success Message Format
All successful operations follow this pattern:
```
Task #X [action] successfully
```
Examples:
- "Task #1 created successfully"
- "Task #2 updated successfully"
- "Task #3 marked as complete successfully"
- "Task #4 deleted successfully"

## Exit Behavior
- Upon selecting option 6 or Ctrl+C, application exits gracefully
- All in-memory data is lost (consistent with specification)
- No cleanup required