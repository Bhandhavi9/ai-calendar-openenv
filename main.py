import random
from typing import Dict, List

# -----------------------------
# Environment
# -----------------------------
class SmartSchedulerEnv:
    def __init__(self):
        self.max_steps = 3
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        self.state_data = {
            "participants": self._generate_participants(),
            "proposal_history": [],
            "done": False
        }
        return self.state()

    def _generate_participants(self):
        return [
            {"name": "Alice", "timezone": 0, "availability": [9,10,15], "priority": 2},
            {"name": "Bob", "timezone": 1, "availability": [10,15], "priority": 1},
            {"name": "Charlie", "timezone": -1, "availability": [9,15], "priority": 1}
        ]

    def state(self):
        return self.state_data

    def step(self, action: Dict):
        self.current_step += 1
        start = action.get("start_time")

        participants = self.state_data["participants"]

        attendance = 0
        vip_present = False

        for p in participants:
            local_time = start + p["timezone"]
            if local_time in p["availability"]:
                attendance += 1
                if p["priority"] == 2:
                    vip_present = True

        attendance_ratio = attendance / len(participants)
        vip_score = 1 if vip_present else 0

        reward = (0.5 * attendance_ratio) + (0.5 * vip_score)

        if start < 9 or start > 18:
            reward -= 0.3

        done = self.current_step >= self.max_steps

        self.state_data["proposal_history"].append(action)
        self.state_data["done"] = done

        return {
            "state": self.state(),
            "reward": max(0.0, min(1.0, reward)),
            "done": done
        }

# -----------------------------
# Tasks
# -----------------------------
class TaskEasy:
    def grade(self, reward):
        return reward

class TaskMedium:
    evaluate(agent
