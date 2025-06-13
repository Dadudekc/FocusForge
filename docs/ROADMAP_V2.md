# FocusForge v2 Roadmap

## 🔰 Phase 1 — Core Focus Engine (Now)

### Core Features
- [x] 🧠 Distraction detection (active/inactive, app switch, text-level)
- [x] 🕒 Pomodoro & manual timer modes
- [x] 📋 Task manager with deadlines and hierarchy
- [x] 📈 Analytics: streaks, session breakdowns, average focus
- [x] 🧠 Meta-skills: XP for sessions, task completions, streaks

### Polish & Refinement
- [ ] 🎮 KantuBoard gamification polish (XP animations, draggable tasks)
- [ ] 📤 Session-to-report export
- [ ] 🔄 App usage logging for deep work stats

## 🧱 Phase 2 — Foundation Polish (July 2024)

### Code Quality
- [ ] ⚙️ Refactor `main_window.py` (complexity: 46) into smaller components
- [ ] 🧪 Add unit tests across all core modules
- [ ] 🗃️ Refactor SQLite schema to include per-task logs
- [ ] 📂 Centralize config/log paths for portability

### UI/UX
- [ ] 🌓 Dark/light theme toggle UI polish
- [ ] 🎨 Consistent design language across all components
- [ ] 📱 Responsive layout improvements

## 🌐 Phase 3 — Sync + Optional Bridge (August 2024)

### External Integrations
- [ ] 🔌 Discord summary hook (weekly status dump)
- [ ] 🛰️ JSON export format compatible with Dream.OS
- [ ] 📡 Dream.OS → FocusForge task injection bridge (one-way only)

### Data Portability
- [ ] 📤 Export/import functionality
- [ ] 🔄 Backup/restore system
- [ ] 📊 Data visualization improvements

## 🧠 Phase 4 — Deep Personal Feedback (Fall 2024)

### Intelligence Layer
- [ ] 🧠 DecisionEngine 2.0: smarter break duration prediction
- [ ] 🗣️ "Mid-session reflection" interrupt prompts
- [ ] 📜 Narrative-style session logs ("You sat for 47m. You faced 3 distractions. Your intent held.")
- [ ] 🎯 Intention Tracker: "What are you trying to do right now?" — with match scoring

### Personalization
- [ ] 🎯 Custom focus goals
- [ ] 📊 Personalized analytics
- [ ] 🎮 Custom meta-skill paths

## 📱 Phase 5 — Mobile Companion (Optional)

### Core Mobile Features
- [ ] Android app: timer, task, session sync
- [ ] Push notifications when session ends or goal missed
- [ ] Lightweight stats viewer

### Mobile Enhancements
- [ ] 📱 Widget support
- [ ] 🔔 Custom notification rules
- [ ] 📊 Mobile-optimized dashboards

## 🧬 System Structure

### Core Components
- `core/`: trackers, logger, RL engine
- `gui/`: dashboards, dialogs
- `meta_skills/`: gamification layer
- `kantu_board.py`: task gamifier
- `focus_report.py`: report logic
- `focus_env.py`: Gym-style AI training loop

### Development Guidelines
- Maintain modular architecture
- Keep core functionality independent
- Document all public APIs
- Write tests for new features

## Success Metrics

### User Engagement
- Daily active users
- Session completion rate
- Feature adoption rate
- User retention rate

### Performance
- Application response time
- Resource utilization
- Error rate
- Crash frequency

### Business
- User growth rate
- Feature usage statistics
- User satisfaction scores
- Support ticket volume 