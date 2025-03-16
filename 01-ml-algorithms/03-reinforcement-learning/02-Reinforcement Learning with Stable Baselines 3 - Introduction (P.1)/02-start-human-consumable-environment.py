#!/usr/bin/env python
# coding: utf-8

# YouTube video: [Reinforcement Learning with Stable Baselines 3 - Introduction (P.1)](https://www.youtube.com/watch?v=XbWhJdQgi7E)
# 
# # Timestamps
# 
# 01:06 : install pytorch \
# 02:50 : terminology     \
# 05:30 : start of the coding example                         \
# 07:40 : OP's mindset of approaching reinforcement learning 

# # Command
# 
# - Export jypyter notebook into python script
# 
# ``` shell
# jupyter nbconvert --to script your_notebook_name.ipynb
# 
# ```

# In[1]:


import gymnasium as gym


# - [reset()](https://gymnasium.farama.org/api/env/)
# 
#     reset the environment to an initial state, required before calling step \
#     returns the first agent observation for an episode and information.     \
#     i.e. metrics, debug information
# 
# - action_space
# 
#     the space object corresponding to valid actions        \
#     all valid actions should be contained within the space
# 

# In[5]:


env = gym.make("LunarLander-v3", render_mode="human")

# Having a new environment
# before step into that environment
# need to reset the environment to initial state
env.reset()

for setp in range(200):
    env.render()
    env.step(env.action_space.sample())

env.close()


# In[ ]:




