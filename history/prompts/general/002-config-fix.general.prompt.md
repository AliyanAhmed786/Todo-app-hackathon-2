---
id: 002
title: Config Fix for AttributeError
stage: general
date_iso: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Wajiz.pk
command: python main.py error fix
labels: ["bug-fix", "configuration", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/config.py
tests_yaml: |
  - Import test for main.py
---

# Config Fix for AttributeError

## Summary

Fixed an AttributeError in the backend configuration that prevented the application from starting. The error occurred due to incorrect method usage on the int type.

## Error Details

The original error was:
```
AttributeError: type object 'int' has no attribute 'getenv'
```

This occurred in `backend/config.py` line 19 where `int.getenv()` was incorrectly used instead of `os.getenv()` followed by `int()` conversion.

## Change Made

**File**: `backend/config.py`
- **Line 19**: Changed `int.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)` to `int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))`
- This properly converts the environment variable string to an integer after getting it from os.getenv()

## Verification

- Successfully imported the main module without errors
- Application now starts correctly
- Configuration values are properly loaded

## Outcome

The backend application now starts successfully without the AttributeError. This fix enables the application to properly read the refresh token expiration days setting from environment variables.