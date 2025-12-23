---
description: "Task list for Todo Console Application implementation"
---

# Tasks: 1-todo-console-app

**Input**: Design documents from `/specs/1-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with src/ and tests/ directories
- [X] T002 [P] Create src/models/ directory for task model
- [X] T003 [P] Create src/services/ directory for task service
- [X] T004 [P] Create src/cli/ directory for menu interface
- [X] T005 [P] Create tests/unit/ directory for unit tests
- [X] T006 [P] Create tests/integration/ directory for integration tests

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create base Task model in src/models/task.py with id, title, description, status, created_date fields
- [X] T008 [P] Implement Task model validation (title 1-200 chars, description 0-1000 chars, no whitespace-only title)
- [X] T009 [P] Create TaskService class in src/services/task_service.py with in-memory storage
- [X] T010 [P] Implement auto-incrementing ID functionality in TaskService (starting from 1, never recycled)
- [X] T011 [P] Create main menu structure in src/cli/menu.py
- [X] T012 Create main.py application entry point with menu loop
- [X] T013 [P] Create conftest.py for test configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add tasks with title and optional description, with validation and success feedback

**Independent Test**: Can be fully tested by adding a task with a title and verifying it appears in the task list. Delivers the core value of task creation.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T014 [P] [US1] Create unit test for Task model validation in tests/unit/test_task.py
- [X] T015 [P] [US1] Create unit test for TaskService add_task functionality in tests/unit/test_task_service.py
- [X] T016 [P] [US1] Create integration test for add task workflow in tests/integration/test_cli.py

### Implementation for User Story 1

- [X] T017 [P] [US1] Implement Task model validation methods in src/models/task.py (FR-008, FR-009)
- [X] T018 [P] [US1] Implement TaskService.create_task method with validation in src/services/task_service.py (FR-001, FR-002)
- [X] T019 [US1] Implement Add Task menu option in src/cli/menu.py (FR-012)
- [X] T020 [US1] Add input validation for title and description in menu.py (FR-008, FR-009)
- [X] T021 [US1] Display success message in format 'Task #X created successfully' in menu.py (FR-013)
- [X] T022 [US1] Add error handling for invalid title (whitespace-only) in menu.py (FR-008)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P2)

**Goal**: Display all tasks with their ID, title, description, and status

**Independent Test**: Can be fully tested by adding multiple tasks and viewing the complete list. Delivers the core value of task visibility.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T023 [P] [US2] Create unit test for TaskService get_all_tasks in tests/unit/test_task_service.py
- [X] T024 [P] [US2] Create integration test for view task list workflow in tests/integration/test_cli.py

### Implementation for User Story 2

- [X] T025 [P] [US2] Implement TaskService.get_all_tasks method in src/services/task_service.py (FR-004)
- [X] T026 [US2] Implement View Task List menu option in src/cli/menu.py (FR-012)
- [X] T027 [US2] Format task display as 'ID. [Status] Title - Description' in menu.py (Contract requirement)
- [X] T028 [US2] Handle case when no tasks exist, display appropriate message in menu.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark as Complete (Priority: P3)

**Goal**: Toggle task status between complete/incomplete

**Independent Test**: Can be fully tested by creating a task, marking it complete, and verifying the status change. Delivers the core value of task completion tracking.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T029 [P] [US3] Create unit test for TaskService toggle_status in tests/unit/test_task_service.py
- [X] T030 [P] [US3] Create integration test for mark complete workflow in tests/integration/test_cli.py

### Implementation for User Story 3

- [X] T031 [P] [US3] Implement TaskService.toggle_status method in src/services/task_service.py (FR-005)
- [X] T032 [P] [US3] Implement TaskService.get_task_by_id method in src/services/task_service.py
- [X] T033 [US3] Implement Mark as Complete menu option in src/cli/menu.py (FR-012)
- [X] T034 [US3] Add success message for mark complete operation in menu.py (FR-013)
- [X] T035 [US3] Add error handling for non-existent task IDs in menu.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task (Priority: P4)

**Goal**: Modify title or description of existing task

**Independent Test**: Can be fully tested by updating a task's title/description and verifying the changes persist. Delivers the value of task modification.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T036 [P] [US4] Create unit test for TaskService update_task in tests/unit/test_task_service.py
- [X] T037 [P] [US4] Create integration test for update task workflow in tests/integration/test_cli.py

### Implementation for User Story 4

- [X] T038 [P] [US4] Implement TaskService.update_task method in src/services/task_service.py (FR-006)
- [X] T039 [US4] Implement Update Task menu option in src/cli/menu.py (FR-012)
- [X] T040 [US4] Add input validation for updated title/description in menu.py (FR-008, FR-009)
- [X] T041 [US4] Add success message for update operation in menu.py (FR-013)
- [X] T042 [US4] Add error handling for non-existent task IDs in menu.py

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: Remove task by ID with confirmation prompt

**Independent Test**: Can be fully tested by deleting a task and verifying it no longer appears in the task list. Delivers the value of task removal.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T043 [P] [US5] Create unit test for TaskService delete_task in tests/unit/test_task_service.py
- [X] T044 [P] [US5] Create integration test for delete task workflow in tests/integration/test_cli.py

### Implementation for User Story 5

- [X] T045 [P] [US5] Implement TaskService.delete_task method in src/services/task_service.py (FR-007, FR-011)
- [X] T046 [US5] Implement Delete Task menu option in src/cli/menu.py (FR-012)
- [X] T047 [US5] Add confirmation prompt 'Are you sure? (Y/N)' before deletion in menu.py (FR-014)
- [X] T048 [US5] Implement success message for delete operation in menu.py (FR-013)
- [X] T049 [US5] Add error handling for non-existent task IDs in menu.py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T050 [P] Add comprehensive error handling throughout the application
- [X] T051 [P] Add input sanitization and validation for all user inputs
- [X] T052 [P] Create documentation in docs/ directory
- [X] T053 [P] Add README.md with setup and usage instructions
- [X] T054 [P] Add configuration validation
- [X] T055 Run all tests to ensure functionality meets success criteria

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints/cli
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Create unit test for Task model validation in tests/unit/test_task.py"
Task: "Create unit test for TaskService add_task functionality in tests/unit/test_task_service.py"
Task: "Create integration test for add task workflow in tests/integration/test_cli.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Implement Task model validation methods in src/models/task.py"
Task: "Implement TaskService.create_task method with validation in src/services/task_service.py"
Task: "Implement Add Task menu option in src/cli/menu.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence