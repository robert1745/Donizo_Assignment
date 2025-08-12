import json
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime
from pricing_logic.material_db import MaterialDB
from pricing_logic.labor_calc import LaborCalculator
from pricing_logic.vat_rules import VATCalculator


class SmartPricingEngine:
    def __init__(self):
        self.material_db = MaterialDB()
        self.labor_calc = LaborCalculator()
        self.vat_calc = VATCalculator()
        
        
        self.city_multipliers = {
            'paris': 1.25,
            'marseille': 1.0,
            'lyon': 1.15,
            'toulouse': 0.95,
            'nice': 1.20,
            'nantes': 1.05,
            'bordeaux': 1.10
        }
        
        
        self.base_margin = 0.20  
        self.margin_protection_min = 0.15  
    
  
    def generate_quote(self, transcript: str) -> Dict[str, Any]:
        """Generate complete structured quote from transcript"""
        parsed_data = self.parse_transcript(transcript)
        
        quote = {
            'quote_id': f"QTE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'client_info': {
                'location': parsed_data['location'],
                'budget_preference': parsed_data['budget_preference']
            },
            'project_details': {
                'zone': parsed_data['room_type'],
                'room_size_m2': parsed_data['room_size'],
                'tasks_identified': parsed_data['tasks']
            },
            'pricing': {
                'zones': {},
                'summary': {}
            },
            'confidence_score': 0.0,
            'confidence_flags': parsed_data['confidence_flags']
        }
        
        zone_total = 0.0
        zone_tasks = {}
        
        for task in parsed_data['tasks']:
            task_quote = self._calculate_task_pricing(
                task, 
                parsed_data['room_size'], 
                parsed_data['location'],
                parsed_data['budget_preference']
            )
            zone_tasks[task] = task_quote
            zone_total += task_quote['total_price']
        
        city_multiplier = self.city_multipliers.get(parsed_data['location'], 1.0)
        zone_total *= city_multiplier
        
        for task in zone_tasks:
            zone_tasks[task]['total_price'] *= city_multiplier
            zone_tasks[task]['city_multiplier'] = city_multiplier
        
        quote['pricing']['zones'][parsed_data['room_type']] = {
            'tasks': zone_tasks,
            'zone_total': round(zone_total, 2)
        }
        
        total_materials = sum(task['materials_cost'] for task in zone_tasks.values())
        total_labor = sum(task['labor_cost'] for task in zone_tasks.values())
        total_before_vat = total_materials + total_labor
        total_vat = sum(task['vat_amount'] for task in zone_tasks.values())
        
        quote['pricing']['summary'] = {
            'total_materials': round(total_materials * city_multiplier, 2),
            'total_labor': round(total_labor * city_multiplier, 2),
            'subtotal_before_vat': round(total_before_vat * city_multiplier, 2),
            'total_vat': round(total_vat * city_multiplier, 2),
            'total_price': round(zone_total, 2),
            'city_multiplier': city_multiplier,
            'average_margin': self._calculate_average_margin(zone_tasks)
        }
        
        quote['confidence_score'] = self._calculate_confidence_score(parsed_data, zone_tasks)
        
        return quote
    
    def _calculate_task_pricing(self, task: str, room_size: float, location: str, budget_pref: str) -> Dict[str, Any]:
        """Calculate pricing for a specific task"""
        materials_cost = self.material_db.get_material_cost(task, room_size, budget_pref)
        labor_hours = self.labor_calc.calculate_labor_hours(task, room_size)
        labor_rate = self.labor_calc.get_hourly_rate(location, task)
        labor_cost = labor_hours * labor_rate
        
        subtotal = materials_cost + labor_cost
        margin_rate = self._calculate_dynamic_margin(task, budget_pref, subtotal)
        margin_amount = subtotal * margin_rate
        
        subtotal_with_margin = subtotal + margin_amount
        vat_rate = self.vat_calc.get_vat_rate(task, 'france')
        vat_amount = subtotal_with_margin * vat_rate
        
        total_price = subtotal_with_margin + vat_amount
        
        return {
            'task_name': task,
            'materials_cost': round(materials_cost, 2),
            'labor_hours': labor_hours,
            'labor_rate': labor_rate,
            'labor_cost': round(labor_cost, 2),
            'subtotal': round(subtotal, 2),
            'margin_rate': round(margin_rate, 3),
            'margin_amount': round(margin_amount, 2),
            'vat_rate': round(vat_rate, 3),
            'vat_amount': round(vat_amount, 2),
            'total_price': round(total_price, 2),
            'estimated_duration_days': round(labor_hours / 8, 1)
        }
    
    def _calculate_dynamic_margin(self, task: str, budget_pref: str, subtotal: float) -> float:
        """Calculate dynamic margin based on task complexity and budget preference"""
        base_margin = self.base_margin
        
        if budget_pref == 'budget_conscious':
            base_margin *= 0.8  
        elif budget_pref == 'premium':
            base_margin *= 1.3  
        
        
        complex_tasks = ['plumbing', 'tile_removal', 'floor_installation']
        if task in complex_tasks:
            base_margin *= 1.1  
        
        
        return max(base_margin, self.margin_protection_min)
    
    def _calculate_average_margin(self, zone_tasks: Dict[str, Any]) -> float:
        """Calculate average margin across all tasks"""
        if not zone_tasks:
            return 0.0
        
        total_margin = sum(task['margin_rate'] for task in zone_tasks.values())
        return round(total_margin / len(zone_tasks), 3)
     
    def _calculate_confidence_score(self, parsed_data: Dict[str, Any], zone_tasks: Dict[str, Any]) -> float:
        """Calculate overall confidence score for the quote"""
        confidence = 1.0
        
        if parsed_data['confidence_flags']:
            confidence -= 0.1 * len(parsed_data['confidence_flags'])
        
        if len(parsed_data['tasks']) < 3:
            confidence -= 0.1
        
        if parsed_data['room_size'] < 2 or parsed_data['room_size'] > 30:
            confidence -= 0.15
        
        if parsed_data['location'] in self.city_multipliers:
            confidence += 0.05
        
        return max(0.0, min(1.0, round(confidence, 2)))