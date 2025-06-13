# focus_env.py

import gymnasium as gym
from gymnasium import spaces
import numpy as np

class FocusEnv(gym.Env):
    """
    Custom Environment for Focus Forge AI Agent.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, db, decision_engine):
        super(FocusEnv, self).__init__()
        self.db = db
        self.decision_engine = decision_engine
        self.current_step = 0
        self.max_steps = 1000  # Define as per your requirement

        # Define action and observation space
        # Actions: 0-8 (9 discrete actions)
        # Each action corresponds to a combination of work duration adjustment (-5, 0, +5) and break duration adjustment (-5, 0, +5)
        self.action_space = spaces.Discrete(9)

        # Observations:
        # [success_rate (%), consecutive_failures (0 or 1), current_work_duration, current_break_duration]
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0, 15, 5], dtype=np.float32),
            high=np.array([100.0, 1, 60, 30], dtype=np.float32),
            dtype=np.float32
        )

        # Initialize state
        self.state = self._initialize_state()

    def _initialize_state(self):
        work_duration = self.decision_engine.work_duration
        success_rate = self.db.get_success_rate()
        consecutive_failures = 1 if self.db.get_consecutive_failures() else 0
        break_duration = self.decision_engine.break_duration
        return np.array([success_rate, consecutive_failures, work_duration, break_duration], dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.state = self._initialize_state()
        return self.state, {}

    def step(self, action):
        # Validate action
        assert self.action_space.contains(action), f"Invalid action: {action}"

        # Decode action
        work_change = (action // 3 - 1) * 5  # -5, 0, +5
        break_change = (action % 3 - 1) * 5  # -5, 0, +5

        # Apply action adjustments
        new_work = np.clip(self.state[2] + work_change, 15, 60)
        new_break = np.clip(self.state[3] + break_change, 5, 30)

        # Update Decision Engine settings
        self.decision_engine.work_duration = new_work
        self.decision_engine.break_duration = new_break

        # Calculate reward based on recent sessions
        recent_sessions = self.db.get_recent_sessions(limit=10)
        reward = 0
        for session in recent_sessions:
            if session[6] == 1 and session[7] <= 3:  # completed without excessive distractions
                reward += 1
            elif session[6] == 1 and session[7] > 3:
                reward -= 2  # Completed but with distractions
            elif session[6] == 0 and session[7] > 3:
                reward -= 5  # Abandoned with excessive distractions
            else:
                reward -= 1  # Other failures

        # Bonus for streaks
        streak = self.db.get_streak()
        if streak >= 3:
            reward += 3

        # Update state
        success_rate = self.db.get_success_rate()
        consecutive_failures = 1 if self.db.get_consecutive_failures() else 0
        self.state = np.array([success_rate, consecutive_failures, new_work, new_break], dtype=np.float32)

        # Check if done
        self.current_step += 1
        done = self.current_step >= self.max_steps

        info = {}

        return self.state, reward, done, False, info

    def render(self, mode='human'):
        if mode == "human":
            print(f"Step: {self.current_step}, Work Duration: {self.state[2]} min, Break Duration: {self.state[3]} min, Success Rate: {self.state[0]}%, Consecutive Failures: {self.state[1]}")

    def close(self):
        pass
