"""
Material Database - Handles material costs and inventory
"""

import json
from typing import Dict, Any


class MaterialDB:
    def __init__(self):
        self.materials_data = {
            'tile_removal': {
                'budget_conscious': {'cost_per_m2': 15.0, 'items': ['disposal bags', 'protective sheets']},
                'standard': {'cost_per_m2': 20.0, 'items': ['disposal bags', 'protective sheets', 'cleaning supplies']},
                'premium': {'cost_per_m2': 25.0, 'items': ['eco-friendly disposal', 'premium protection', 'deep cleaning']}
            },
            'plumbing': {
                'budget_conscious': {'base_cost': 180.0, 'cost_per_m2': 25.0, 'items': ['basic pipes', 'standard fittings', 'sealants']},
                'standard': {'base_cost': 250.0, 'cost_per_m2': 35.0, 'items': ['quality pipes', 'standard fittings', 'premium sealants', 'shutoff valves']},
                'premium': {'base_cost': 400.0, 'cost_per_m2': 50.0, 'items': ['premium pipes', 'brass fittings', 'high-end fixtures', 'smart shutoffs']}
            },
            'toilet_replacement': {
                'budget_conscious': {'base_cost': 120.0, 'items': ['basic toilet', 'wax ring', 'bolts', 'supply line']},
                'standard': {'base_cost': 280.0, 'items': ['mid-range toilet', 'wax ring', 'stainless bolts', 'braided supply line']},
                'premium': {'base_cost': 650.0, 'items': ['high-end toilet', 'premium wax ring', 'brass bolts', 'premium supply line', 'bidet features']}
            },
            'vanity_installation': {
                'budget_conscious': {'base_cost': 200.0, 'cost_per_m2': 15.0, 'items': ['basic vanity', 'standard sink', 'basic faucet', 'mounting hardware']},
                'standard': {'base_cost': 450.0, 'cost_per_m2': 25.0, 'items': ['quality vanity', 'ceramic sink', 'mid-range faucet', 'quality hardware', 'mirror']},
                'premium': {'base_cost': 900.0, 'cost_per_m2': 40.0, 'items': ['custom vanity', 'designer sink', 'premium faucet', 'soft-close drawers', 'LED mirror']}
            },
            'painting': {
                'budget_conscious': {'cost_per_m2': 8.0, 'items': ['basic paint', 'primer', 'brushes', 'drop cloths']},
                'standard': {'cost_per_m2': 12.0, 'items': ['quality paint', 'premium primer', 'quality brushes', 'painter tape', 'drop cloths']},
                'premium': {'cost_per_m2': 18.0, 'items': ['premium paint', 'high-end primer', 'professional brushes', 'specialty finishes', 'complete protection']}
            },
            'floor_installation': {
                'budget_conscious': {'cost_per_m2': 35.0, 'items': ['basic ceramic tiles', 'standard adhesive', 'basic grout', 'spacers']},
                'standard': {'cost_per_m2': 55.0, 'items': ['quality ceramic tiles', 'premium adhesive', 'quality grout', 'leveling systems', 'sealer']},
                'premium': {'cost_per_m2': 85.0, 'items': ['designer tiles', 'premium adhesive', 'epoxy grout', 'leveling systems', 'premium sealer', 'trim pieces']}
            },
            'general_renovation': {
                'budget_conscious': {'cost_per_m2': 50.0, 'items': ['basic materials', 'standard supplies']},
                'standard': {'cost_per_m2': 80.0, 'items': ['quality materials', 'complete supplies', 'finishing materials']},
                'premium': {'cost_per_m2': 120.0, 'items': ['premium materials', 'high-end supplies', 'luxury finishes']}
            }
        }
    
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
    
    



    