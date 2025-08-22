# C++ Rewrite Plan

## Task List: Migrate FocusForge from Python to C++ with TDD

1. **Set Up C++ Infrastructure**
   - Choose a build system (e.g., CMake) and configure the root project.
   - Establish a C++ testing framework (GoogleTest or Catch2) and integrate it with the build.
   - Set up continuous integration to run C++ tests automatically.

2. **Capture Existing Python Behavior**
   - Inventory each Python module (e.g., GUI, trackers, analytics) and document public APIs and expected behavior.
   - Write Python-side characterization tests that describe current behavior before refactoring.

3. **Create C++ Project Skeleton**
   - Mirror the existing Python package structure in a new `src/` directory with headers and source files.
   - Implement placeholder classes/methods that match the Python interfaces so tests can be ported gradually.

4. **Port Core Logic (Tracker Modules)**
   - For each tracker (`activity_monitor`, `distraction_logger`, etc.),
     a. Write failing C++ unit tests reflecting the Python characterization tests.
     b. Implement the C++ version.
     c. Run tests until they pass.
     d. Remove the corresponding Python module once covered by tests.
   - Document any behavioral differences and update tests accordingly.

5. **Port Analytics/Reporting**
   - Translate reporting features (e.g., `FocusReport`) into C++, ensuring data formats and outputs match Python behavior.
   - Add tests to verify CSV generation and analytics calculations.

6. **Port GUI**
   - Decide on a GUI toolkit (likely Qt in C++).
   - Incrementally rewrite each Python `gui` component (e.g., `MainWindow`, `SplashScreen`) in C++ Qt.
   - Use Qt test utilities to validate signals, slots, and widget behavior without launching full UI.
   - Remove Python GUI files after their C++ counterparts and tests are validated.

7. **Integration & End-to-End Tests**
   - Build integration tests that combine core, analytics, and GUI layers to simulate user flows.
   - Ensure the full workflow (launch → monitor → report generation) functions in C++.

8. **Deprecate Python Entry Points**
   - Once C++ components can run the full application, replace `main.py` with a C++ `main()` that wires everything together.
   - Confirm that the application launches cleanly and generates reports as before.

9. **Clean-Up and Documentation**
   - Remove remaining Python files and update `requirements.txt`/build instructions to reflect the pure C++ project.
   - Rewrite `README.md` and developer docs to describe C++ build, test, and run processes.
   - Ensure `TASK_LIST.md` is updated with completion notes and any future enhancement ideas.

10. **Ongoing Maintenance**
    - Adopt static analysis (clang-tidy, sanitizers) and code formatting (clang-format) to keep codebase healthy.
    - Continue adding regression tests for new features or bug fixes.

### References
- The current Python entry point and GUI wiring can be seen in `main.py`, which uses PyQt components and the `AdvancedDistractionDetector` class.
- Existing project tasks and roadmap are detailed in `TASK_LIST.md`.

---

## Rewriting FocusForge in C++

Rewriting the project in C++ is certainly possible, but it will likely be a significant effort. Here are some general steps and considerations that might help you get started:

### 1. Understand the Existing Codebase
- **Identify features and modules**: Document what each part of the current project does.
- **Examine dependencies**: Know which libraries and services are being used so you can find C++ equivalents or decide on replacements.

### 2. Plan the Architecture
- **Decide on a build system**: CMake is widely used and works across platforms.
- **Set up project structure**: Organize source, include, test, and resource directories for clarity.
- **Choose libraries**: Depending on the project’s needs (e.g., networking, UI, JSON parsing), pick suitable C++ libraries or frameworks.

### 3. Incremental Translation
- **Port module by module**: Translate small parts and verify functionality incrementally rather than rewriting everything at once.
- **Maintain parallel builds**: If possible, keep the existing version running so you can compare behavior between the original and C++ implementations.

### 4. Testing & Validation
- **Unit tests**: Translate or create tests for each module to ensure parity with the original project.
- **Integration tests**: Verify that modules interact correctly.
- **Continuous integration**: Automate builds and tests to catch regressions early.

### 5. Performance & Safety
- **Memory management**: Leverage modern C++ smart pointers and RAII principles to prevent leaks.
- **Concurrency**: Use standard library facilities (e.g., `std::thread`, `std::async`) or a dedicated framework if the project requires it.
- **Static analysis & tools**: Tools like `clang-tidy` and sanitizers can help catch issues early.

### 6. Documentation & Maintenance
- **Document API changes**: Clearly describe any differences from the original project for future maintainers.
- **Continuous refactoring**: C++ has many paradigms (procedural, OO, generic, functional); refactor to keep code clean and understandable.

---

*This document captures planning guidance for migrating FocusForge from Python to C++.*
