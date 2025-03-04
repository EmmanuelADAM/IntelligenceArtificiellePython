import gymnasium as gym
import numpy as np
from gymnasium.envs.toy_text.frozen_lake import FrozenLakeEnv

class FrozenLakeWithPenalties(FrozenLakeEnv):
    def __init__(self, desc=None, map_name=None, is_slippery=False, render_mode="ansi"):
        super().__init__(desc=desc, map_name=map_name, is_slippery=is_slippery, render_mode=render_mode)

        # Modify reward structure: Create a new dictionary for custom rewards
        self.custom_rewards = np.zeros(self.desc.shape)
        
        # Define penalty state
        for row in range(self.desc.shape[0]):
            for col in range(self.desc.shape[1]):
                if self.desc[row, col] == b'P':  # Custom penalty tile
                    self.custom_rewards[row, col] = -1
    

    
    def step(self, action):
        next_state, reward, terminated, truncated, info = super().step(action)

        # Apply penalty if the agent steps on 'P'
        row, col = divmod(next_state, self.ncol)
        if self.desc[row, col] == b'P':  
            reward = self.custom_rewards[row, col]

        return next_state, reward, terminated, truncated, info



