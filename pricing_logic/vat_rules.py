"""
VAT Rules Calculator - Handles country and task-specific VAT calculations
"""

from typing import Dict, Any,List
from datetime import datetime


class VATCalculator:
    def __init__(self):
        self.vat_rates = {
            'france': {
                'standard': 0.20,  
                'reduced': 0.10,   
                'super_reduced': 0.055,  
                'zero': 0.0        
            },
            'germany': {
                'standard': 0.19,
                'reduced': 0.07,
                'zero': 0.0
            },
            'spain': {
                'standard': 0.21,
                'reduced': 0.10,
                'super_reduced': 0.04,
                'zero': 0.0
            },
            'italy': {
                'standard': 0.22,
                'reduced': 0.10,
                'super_reduced': 0.04,
                'zero': 0.0
            }
        }
        
        
        self.task_vat_categories = {
            'tile_removal': {
                'france': 'reduced',    
                'germany': 'standard',
                'spain': 'reduced',
                'italy': 'reduced'
            },
            'plumbing': {
                'france': 'reduced',    
                'germany': 'standard',
                'spain': 'reduced',
                'italy': 'reduced'
            },
            'toilet_replacement': {
                'france': 'standard',   
                'germany': 'standard',
                'spain': 'standard',
                'italy': 'standard'
            },
            'vanity_installation': {
                'france': 'standard',   
                'germany': 'standard',
                'spain': 'standard',
                'italy': 'standard'
            },
            'painting': {
                'france': 'reduced',    
                'germany': 'standard',
                'spain': 'reduced',
                'italy': 'reduced'
            },
            'floor_installation': {
                'france': 'reduced',    
                'germany': 'standard',
                'spain': 'reduced',
                'italy': 'reduced'
            },
            'general_renovation': {
                'france': 'reduced',    
                'germany': 'standard',
                'spain': 'reduced',
                'italy': 'reduced'
            },
            'energy_efficiency': {
                'france': 'super_reduced',  
                'germany': 'reduced',
                'spain': 'super_reduced',
                'italy': 'super_reduced'
            }
        }
        
        
        self.vat_conditions = {
            'building_age': {
                'old_building': {  
                    'france': {'renovation_discount': True, 'rate_reduction': 0.10}
                }
            },
            'accessibility_improvements': {
                'france': 'super_reduced',  
                'germany': 'reduced',
                'spain': 'super_reduced',
                'italy': 'super_reduced'
            },
            'energy_certification': {
                'france': 'super_reduced',  
                'germany': 'reduced',
                'spain': 'super_reduced',
                'italy': 'super_reduced'
            }
        }
    
    def get_vat_rate(self, task: str, country: str = 'france', 
                     conditions: Dict[str, Any] = None) -> float:
        """
        Get VAT rate for a specific task and country
        
        Args:
            task: Type of renovation task
            country: Country code (lowercase)
            conditions: Special conditions affecting VAT
        
        Returns:
            VAT rate as decimal (e.g., 0.20 for 20%)
        """
        country_lower = country.lower()
        
        if country_lower not in self.vat_rates:
            country_lower = 'france'
        
        vat_category = 'standard'  
        if task in self.task_vat_categories:
            vat_category = self.task_vat_categories[task].get(country_lower, 'standard')
        
        if conditions:
            vat_category = self._apply_vat_conditions(vat_category, country_lower, conditions)
        
        return self.vat_rates[country_lower][vat_category]
    
    def _apply_vat_conditions(self, base_category: str, country: str, 
                            conditions: Dict[str, Any]) -> str:
        """Apply special conditions to determine final VAT category"""

        if conditions.get('energy_efficiency', False):
            return self.vat_conditions['energy_certification'].get(country, base_category)
        
        if conditions.get('accessibility_improvements', False):
            return self.vat_conditions['accessibility_improvements'].get(country, base_category)
        
        if country == 'france' and conditions.get('building_age_years', 0) > 2:
            if base_category == 'standard':
                return 'reduced'
        
        return base_category
    
    def calculate_vat_amount(self, base_amount: float, task: str, 
                           country: str = 'france', conditions: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate VAT amount and total including VAT
        
        Args:
            base_amount: Amount before VAT
            task: Type of renovation task
            country: Country code
            conditions: Special conditions
        
        Returns:
            Dictionary with VAT breakdown
        """
        vat_rate = self.get_vat_rate(task, country, conditions)
        vat_amount = base_amount * vat_rate
        total_amount = base_amount + vat_amount
        
        return {
            'base_amount': round(base_amount, 2),
            'vat_rate': round(vat_rate, 3),
            'vat_percentage': round(vat_rate * 100, 1),
            'vat_amount': round(vat_amount, 2),
            'total_amount': round(total_amount, 2),
            'country': country,
            'task': task,
            'vat_category': self._get_vat_category_name(task, country, conditions)
        }
    
    def _get_vat_category_name(self, task: str, country: str, conditions: Dict[str, Any] = None) -> str:
        """Get human-readable VAT category name"""
        vat_rate = self.get_vat_rate(task, country, conditions)
        country_rates = self.vat_rates.get(country.lower(), self.vat_rates['france'])
        
        for category, rate in country_rates.items():
            if abs(rate - vat_rate) < 0.001:  
                return category
        
        return 'standard'
    
    def get_vat_summary_by_tasks(self, tasks_costs: Dict[str, float], 
                                country: str = 'france', conditions: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate VAT summary for multiple tasks
        
        Args:
            tasks_costs: Dictionary of {task: cost_amount}
            country: Country code
            conditions: Special conditions
        
        Returns:
            Complete VAT summary
        """
        vat_breakdown = {}
        total_base = 0.0
        total_vat = 0.0
        
        for task, cost in tasks_costs.items():
            task_vat = self.calculate_vat_amount(cost, task, country, conditions)
            vat_breakdown[task] = task_vat
            total_base += cost
            total_vat += task_vat['vat_amount']
        
        
        vat_groups = {}
        for task, vat_data in vat_breakdown.items():
            rate = vat_data['vat_rate']
            if rate not in vat_groups:
                vat_groups[rate] = {
                    'vat_percentage': vat_data['vat_percentage'],
                    'base_amount': 0.0,
                    'vat_amount': 0.0,
                    'tasks': []
                }
            vat_groups[rate]['base_amount'] += vat_data['base_amount']
            vat_groups[rate]['vat_amount'] += vat_data['vat_amount']
            vat_groups[rate]['tasks'].append(task)
        
        
        for rate_group in vat_groups.values():
            rate_group['base_amount'] = round(rate_group['base_amount'], 2)
            rate_group['vat_amount'] = round(rate_group['vat_amount'], 2)
        
        return {
            'country': country,
            'total_base_amount': round(total_base, 2),
            'total_vat_amount': round(total_vat, 2),
            'total_with_vat': round(total_base + total_vat, 2),
            'vat_groups': vat_groups,
            'task_breakdown': vat_breakdown,
            'conditions_applied': conditions or {}
        }
    
    