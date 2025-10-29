# Claude Instance Coordination

This directory is for communication between different Claude instances working on the 100X Platform.

## Structure

- `messages/` - Numbered message files for inter-Claude communication
- `context/` - Persistent context that all Claude instances should read on startup
- `bugs/` - Bug tracking and issues

## Usage

When one Claude instance needs to communicate with another:
1. Create a numbered message file in `messages/` (e.g., `122.md`)
2. Include timestamp, sender ID, and urgency level
3. The receiving Claude will check this directory on startup

## Current Session

- **Session ID**: 011CUcCpz8d8uRu53bencYP3
- **Branch**: claude/check-repository-response-011CUcCpz8d8uRu53bencYP3
- **Date**: October 29, 2025
