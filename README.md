# Focus Forge AI Agent

**Focus Forge** is an AI-powered Pomodoro-based productivity application that dynamically adjusts work and break sessions based on user behavior. It leverages Reinforcement Learning (PPO) to optimize focus efficiency over time.

## **Features**

- **Dynamic Session Adjustment:** Automatically modifies Pomodoro durations based on performance.
- **Task Management:** Prioritize and manage tasks with ease.
- **Distraction Detection:** Monitors active windows and user inactivity to detect distractions.
- **Analytics & Visualization:** Gain insights into your productivity patterns.
- **Reinforcement Learning Optimization:** AI-driven optimizations for personalized focus sessions.

## **Installation**

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/focus_forge.git
   cd focus_forge

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database:**

   The database is automatically initialized when you run the application for the first time.

5. **Train the Reinforcement Learning Model (Optional but Recommended):**

   ```bash
   python train_rl.py
   ```



6. **Train the Reinforcement Learning Model (Optional but Recommended):**

   ```bash
   python train_rl.py
   ```

   Note: Training may take time based on the number of timesteps and available computational resources.

7. **Running the Application:**

   ```bash
   python main.py
   ```


8. **Usage:**

   - **Add Tasks:**

     Enter a task description.
     Select priority (High, Medium, Low).
     Click "Add Task" to include it in your task list.

   - **Start Timer:**

     Click "Start" to begin a work session.
     The timer will count down, switching between work and break sessions automatically.

   - **Monitor Sessions:**

     View session history and performance metrics.

   - **Analyze Productivity Patterns:**

     Analyze productivity patterns through visual charts.

   - **Settings:**

     Access settings to customize default work/break durations.
     Toggle Reinforcement Learning optimization.

9. **Project Structure:**

   - **main.py:** Core PyQt5 application.
   - **database.py:** Handles all database operations.
   - **decision_engine.py:** Implements rule-based and RL-based session adjustments.
   - **focus_env.py:** Custom Gym environment for RL.
   - **distraction_monitor.py:** Monitors active window changes.
   - **activity_monitor.py:** Tracks keyboard and mouse activity.
   - **train_rl.py:** Script to train the PPO model.
   - **requirements.txt:** List of project dependencies.
   - **README.md:** Project documentation.

10. **Contributing:**

   Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

11. **License:**

   MIT License. See LICENSE for details.


12. **Contact:**

   For questions or feedback, please contact me at [Donotcontactme@gmail.com].



