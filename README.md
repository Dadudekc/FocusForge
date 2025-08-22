# focus-forge

Your solo battle OS for deep focus and productivity.

> **Status:** FocusForge is in the middle of a full rewrite from Python to C++. The
> step-by-step migration plan lives in [`docs/cpp_rewrite_plan.md`](docs/cpp_rewrite_plan.md).

## 🎯 Mission

Track. Train. Transform.

## 🏗️ Project Structure

```
focus-forge/
├── core/                    # Core functionality
│   ├── trackers/           # Distraction and activity tracking
│   ├── analytics/          # Focus reporting and analysis
│   ├── engine/             # Decision engine and RL components
│   └── utils/              # Shared utilities
├── gui/                    # User interface components
│   ├── components/         # Main UI components
│   ├── dialogs/           # Modal dialogs
│   └── themes/            # UI themes
├── meta_skills/           # Gamification system
│   ├── animations/        # Skill animations
│   └── levels/            # Skill progression
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docs/                  # Documentation
├── config/                # Configuration files
└── logs/                  # Application logs
```

## 🚀 Features

- 🧠 Advanced distraction detection
- 📊 Session analytics and reporting
- 🎮 Gamified meta-skills system
- 📋 Kanban-style task board
- 🎯 Focus environment optimization
- 📈 Progress tracking and visualization

## 🛠️ Development

### Prerequisites

- Python 3.8+ (legacy implementation)
- PyQt5
- SQLite3
- C++17 compiler and CMake (for the ongoing rewrite)

### Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running

```bash
python main.py  # legacy Python entry point
```

The C++ executable and build instructions will be added as the rewrite matures.

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📚 Documentation

- [Vision](docs/VISION.md)
- [Roadmap](docs/ROADMAP_V2.md)
- [Configuration](config/project_config.yaml)
- [C++ Rewrite Plan](docs/cpp_rewrite_plan.md)



