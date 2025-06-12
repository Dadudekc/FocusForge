# train_rl.py

import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from focus_env import FocusEnv
from database import Database
from decision_engine import DecisionEngine

def main():
    db = Database()
    decision_engine = DecisionEngine(db)
    env = FocusEnv(db, decision_engine)
    
    # Verify the environment adheres to Gym's API
    check_env(env, warn=True)
    
    # Initialize PPO model
    model = PPO('MlpPolicy', env, verbose=1)
    
    # Train the model
    print("Starting training...")
    model.learn(total_timesteps=100000)  # Adjust timesteps as needed
    
    # Save the trained model
    model.save("ppo_focus_forge")
    print("Training completed and model saved as 'ppo_focus_forge.zip'.")

if __name__ == "__main__":
    main()
