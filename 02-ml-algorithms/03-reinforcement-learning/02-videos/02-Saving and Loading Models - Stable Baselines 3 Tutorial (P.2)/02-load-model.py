import gymnasium as gym
from stable_baselines3 import PPO

env = gym.make("LunarLander-v3", render_mode="human")

env.reset()


models_dir = "models/PPO"
model_path = f"{models_dir}/170000.zip"

model = PPO.load(model_path, env=env)

vec_env = model.get_env()

episodes = 5

for ep in range(episodes):
    obs     = vec_env.reset()
    done    = False
    
    while not done:
        vec_env.render()
        action, _ = model.predict(obs)
        obs, reward, done , info = vec_env.step(action)
        

env.close()