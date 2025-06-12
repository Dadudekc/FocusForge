# decision_engine.py

from stable_baselines3 import PPO
from focus_env import FocusEnv
import os
from gym import Wrapper
import logging
import numpy as np

class DecisionEngine:
    def __init__(self, db, distraction_detector):
        self.db = db
        self.distraction_detector = distraction_detector
        # Default Pomodoro settings
        self.work_duration = 25  # minutes
        self.break_duration = 5  # minutes

        # Initialize RL environment with both db and decision_engine
        self.env = FocusEnv(db, self)

        # Load trained PPO model if available
        self.model = None
        model_path = "ppo_focus_forge"
        if os.path.exists(model_path + ".zip"):
            try:
                self.model = PPO.load(model_path)
                print("PPO model loaded successfully.")
            except Exception as e:
                print(f"Failed to load PPO model: {e}")
                self.model = None
        else:
            print("PPO model not found. Proceeding with rule-based adjustments.")

    def get_optimal_durations(self):
        state = self.env.reset()
        action, _states = self.model.predict(state, deterministic=True)
        return action

    def apply_rules(self):
        """
        Adjusts work and break durations based on focus performance and distractions.
        """
        success_rate = self.db.get_success_rate()
        consecutive_failures = self.db.get_consecutive_failures()
        current_work_duration = self.db.get_average_work_duration() or 25
        current_break_duration = self.db.get_average_distractions() or 5

        # Check for distractions
        detected_distractions = self.distraction_detector.reset_distractions()
        distraction_penalty = min(10, detected_distractions * 2)  # Reduce work time if distractions occur

        # Convert observation into a NumPy array for RL model
        obs = np.array([[success_rate, consecutive_failures, current_work_duration, current_break_duration]], dtype=np.float32)
        
        # Ensure the model receives the correct input format
        action, _states = self.model.predict(obs, deterministic=True)

        # Decode action into work/break duration changes
        work_change = (action // 3 - 1) * 5  # -5, 0, +5
        break_change = (action % 3 - 1) * 5  # -5, 0, +5

        # Adjust work duration based on distractions
        new_work = np.clip(current_work_duration + work_change - distraction_penalty, 15, 60)
        new_break = np.clip(current_break_duration + break_change + (detected_distractions * 1), 5, 30)

        print(f"Adjusted Work Time: {new_work} min, Adjusted Break Time: {new_break} min")
        return new_work, new_break

    def save_model(self, path="ppo_focus_forge"):
        if self.model:
            self.model.save(path)
            print("PPO model saved successfully.")
        else:
            print("No PPO model to save.")

    def train_model(self, total_timesteps=10000):
        if not self.model:
            # Initialize a new model
            self.model = PPO("MlpPolicy", self.env, verbose=1)
        self.model.learn(total_timesteps=total_timesteps)
        self.save_model()

class ObservationOnlyWrapper(Wrapper):
    def reset(self, **kwargs):
        observation, info = self.env.reset(**kwargs)
        return observation  # Return only the observation

    def step(self, action):
        observation, reward, done, truncated, info = self.env.step(action)
        return observation, reward, done, truncated, info
