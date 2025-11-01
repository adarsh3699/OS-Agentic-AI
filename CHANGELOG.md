# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2025-11-01

### Added

- Professional project structure with `src/`, `docs/`, and `tests/` directories
- Multi-model support with automatic fallback (Groq, Gemini, Ollama)
- Persistent memory system across sessions
- Self-critique and verification tools
- Error recovery with 5+ alternative strategies
- Comprehensive documentation split into focused guides
- Development tooling (Makefile, linting, type checking)
- Example configuration files

### Changed

- Reorganized all Python code into `src/` package
- Merged 6 redundant MD files into 3 focused documentation files
- Simplified imports and module structure
- Updated system prompt for better reliability
- Improved step-by-step verification workflow

### Removed

- Redundant documentation files (AGENTIC_AI_GUIDE.md, AI_IMPROVEMENTS.md, etc.)
- Cluttered root directory files
- Duplicate content across multiple guides

### Fixed

- Import paths for new package structure
- Verification workflow to prevent premature task completion
- API key management with example templates

## [2.0.0] - Earlier

### Added

- Professional-grade features (80% parity with Cursor AI)
- Self-awareness and self-critique capabilities
- Persistent memory system
- Advanced error recovery
- 20 tools total (8 new professional tools)

## [1.0.0] - Initial Release

### Added

- Basic agentic AI functionality
- 12 core tools for computer control
- File and folder operations
- Terminal command execution with safety filters
- Mouse and keyboard control
- Application launcher
