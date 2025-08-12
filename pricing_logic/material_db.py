"""
Material Database - Handles material costs and inventory
"""

import json
from typing import Dict, Any


class MaterialDB:
    def __init__(self):
        with open('data/materials.json', 'r') as f:
            self.materials_data = json.load(f)
    
    def get_material_cost(self, task: str, room_size: float, budget_preference: str = 'standard') -> float:
        """
        Calculate material cost for a specific task
        
        Args:
            task: Type of renovation task
            room_size: Room size in square meters
            budget_preference: budget_conscious, standard, or premium
        
        Returns:
            Total material cost in euros
        """
        if task not in self.materials_data:
            base_cost_per_m2 = {'budget_conscious': 30, 'standard': 50, 'premium': 80}
            return room_size * base_cost_per_m2.get(budget_preference, 50)
        
        task_data = self.materials_data[task][budget_preference]
        
        total_cost = 0.0
        
        if 'base_cost' in task_data:
            total_cost += task_data['base_cost']
        
        if 'cost_per_m2' in task_data:
            total_cost += task_data['cost_per_m2'] * room_size
        
        return total_cost
    
    def get_material_list(self, task: str, budget_preference: str = 'standard') -> list:
        """Get list of materials needed for a task"""
        if task not in self.materials_data:
            return ['general supplies']
        
        return self.materials_data[task][budget_preference].get('items', [])
    
    def get_all_tasks(self) -> list:
        """Get list of all available tasks"""
        return list(self.materials_data.keys())
    
    



    