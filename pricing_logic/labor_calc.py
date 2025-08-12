"""
Labor Calculator - Handles labor time estimation and hourly rates
"""

from typing import Dict, Any

class LaborCalculator:
    def __init__(self):
        self.labor_hours_data = {
            'tile_removal': {
                'base_hours': 2.0,  
                'hours_per_m2': 1.5,  
                'difficulty_multiplier': 1.0,
                'skill_level': 'general'
            },
            'plumbing': {
                'base_hours': 4.0,  
                'hours_per_m2': 2.5,  
                'difficulty_multiplier': 1.4,
                'skill_level': 'specialized'
            },
            'toilet_replacement': {
                'base_hours': 3.0,
                'hours_per_m2': 0.0,  
                'difficulty_multiplier': 1.1,
                'skill_level': 'general'
            },
            'vanity_installation': {
                'base_hours': 4.0,
                'hours_per_m2': 1.0,
                'difficulty_multiplier': 1.2,
                'skill_level': 'general'
            },
            'painting': {
                'base_hours': 1.0,
                'hours_per_m2': 0.8,  
                'difficulty_multiplier': 0.9,
                'skill_level': 'general'
            },
            'floor_installation': {
                'base_hours': 3.0,
                'hours_per_m2': 2.0,
                'difficulty_multiplier': 1.3,
                'skill_level': 'specialized'
            },
            'general_renovation': {
                'base_hours': 8.0,
                'hours_per_m2': 3.0,
                'difficulty_multiplier': 1.0,
                'skill_level': 'general'
            }
        }
        
        self.hourly_rates = {
            'paris': {
                'general': 45.0,
                'specialized': 65.0,
                'expert': 85.0
            },
            'marseille': {
                'general': 35.0,
                'specialized': 50.0,
                'expert': 70.0
            },
            'lyon': {
                'general': 40.0,
                'specialized': 58.0,
                'expert': 78.0
            },
            'toulouse': {
                'general': 32.0,
                'specialized': 46.0,
                'expert': 65.0
            },
            'nice': {
                'general': 42.0,
                'specialized': 60.0,
                'expert': 80.0
            },
            'nantes': {
                'general': 38.0,
                'specialized': 54.0,
                'expert': 74.0
            },
            'bordeaux': {
                'general': 39.0,
                'specialized': 56.0,
                'expert': 76.0
            }
        }
        
        self.complexity_multipliers = {
            'small_room': 1.1,  
            'standard_room': 1.0,
            'large_room': 0.95,  
            'difficult_access': 1.3,
            'old_building': 1.2,
            'new_construction': 0.9
        }
    
    def calculate_labor_hours(self, task: str, room_size: float, complexity_factors: list = None) -> float:
        """
        Calculate total labor hours for a task
        
        Args:
            task: Type of renovation task
            room_size: Room size in square meters
            complexity_factors: List of complexity factors affecting the job
        
        Returns:
            Total labor hours required
        """
        if task not in self.labor_hours_data:
            return max(4.0, room_size * 2.0)
        
        task_data = self.labor_hours_data[task]
        
        base_hours = task_data['base_hours']
        variable_hours = task_data['hours_per_m2'] * room_size
        difficulty_multiplier = task_data['difficulty_multiplier']
        
        total_hours = (base_hours + variable_hours) * difficulty_multiplier
        
        if complexity_factors:
            for factor in complexity_factors:
                if factor in self.complexity_multipliers:
                    total_hours *= self.complexity_multipliers[factor]
        
        if room_size < 5:
            total_hours *= self.complexity_multipliers['small_room']
        elif room_size > 15:
            total_hours *= self.complexity_multipliers['large_room']
        
        return round(total_hours, 2)
    
    def get_hourly_rate(self, city: str, task: str) -> float:
        """
        Get hourly rate for a task in a specific city
        
        Args:
            city: City name
            task: Type of renovation task
        
        Returns:
            Hourly rate in euros
        """
        city_lower = city.lower()
        
        if city_lower not in self.hourly_rates:
            city_lower = 'marseille'
        
        if task in self.labor_hours_data:
            skill_level = self.labor_hours_data[task]['skill_level']
        else:
            skill_level = 'general'
        
        return self.hourly_rates[city_lower][skill_level]
    
    def calculate_labor_cost(self, task: str, room_size: float, city: str, 
                           complexity_factors: list = None) -> Dict[str, Any]:
        """
        Calculate complete labor cost breakdown
        
        Args:
            task: Type of renovation task
            room_size: Room size in square meters
            city: City name
            complexity_factors: List of complexity factors
        
        Returns:
            Dictionary with complete labor cost breakdown
        """
        hours = self.calculate_labor_hours(task, room_size, complexity_factors)
        hourly_rate = self.get_hourly_rate(city, task)
        total_cost = hours * hourly_rate
        
        return {
            'task': task,
            'labor_hours': hours,
            'hourly_rate': hourly_rate,
            'city': city,
            'total_labor_cost': round(total_cost, 2),
            'skill_level_required': self.labor_hours_data.get(task, {}).get('skill_level', 'general'),
            'complexity_factors': complexity_factors or [],
            'estimated_days': round(hours / 8, 1)  
        }
  