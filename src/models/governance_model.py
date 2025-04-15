"""
GovernanceModel: Models governance effectiveness for disaster risk management
"""

import numpy as np
from collections import defaultdict

class GovernanceModel:
    """Model governance effectiveness for disaster risk management in Bangladesh"""
    def __init__(self):
        # Initialize governance parameters
        self._initialize_governance_parameters()
        
    def _initialize_governance_parameters(self):
        """Initialize parameters for governance modeling"""
        # Institutional structure for disaster risk governance
        self.institutional_structure = {
            'national': {
                'ministry_of_disaster_management': {
                    'capacity': 0.7,
                    'resources': 0.6,
                    'authority': 0.8,
                    'effectiveness': 0.65
                },
                'disaster_management_bureau': {
                    'capacity': 0.6,
                    'resources': 0.5,
                    'authority': 0.7,
                    'effectiveness': 0.6
                },
                'flood_forecasting_center': {
                    'capacity': 0.7,
                    'resources': 0.6,
                    'authority': 0.6,
                    'effectiveness': 0.65
                },
                'meteorological_department': {
                    'capacity': 0.7,
                    'resources': 0.5,
                    'authority': 0.6,
                    'effectiveness': 0.6
                },
                'inter_ministerial_coordination': {
                    'presence': 0.7,
                    'functionality': 0.5,
                    'effectiveness': 0.5
                }
            },
            'divisional': {
                'disaster_management_committees': {
                    'capacity': 0.5,
                    'resources': 0.4,
                    'authority': 0.6,
                    'effectiveness': 0.5
                },
                'relief_commissioners': {
                    'capacity': 0.6,
                    'resources': 0.5,
                    'authority': 0.7,
                    'effectiveness': 0.55
                }
            },
            'district': {
                'disaster_management_committees': {
                    'capacity': 0.5,
                    'resources': 0.4,
                    'authority': 0.6,
                    'effectiveness': 0.5
                },
                'district_commissioners': {
                    'capacity': 0.6,
                    'resources': 0.5,
                    'authority': 0.7,
                    'effectiveness': 0.6
                }
            },
            'upazila': {  # Sub-district
                'disaster_management_committees': {
                    'capacity': 0.4,
                    'resources': 0.3,
                    'authority': 0.5,
                    'effectiveness': 0.4
                },
                'upazila_administration': {
                    'capacity': 0.5,
                    'resources': 0.4,
                    'authority': 0.6,
                    'effectiveness': 0.45
                }
            },
            'union': {  # Lowest administrative unit
                'disaster_management_committees': {
                    'capacity': 0.3,
                    'resources': 0.2,
                    'authority': 0.4,
                    'effectiveness': 0.3
                },
                'union_parishad': {
                    'capacity': 0.4,
                    'resources': 0.3,
                    'authority': 0.5,
                    'effectiveness': 0.35
                }
            }
        }
        
        # Policy framework for disaster risk management
        self.policy_framework = {
            'disaster_management_act': {
                'comprehensiveness': 0.8,
                'implementation': 0.5,
                'enforcement': 0.5,
                'effectiveness': 0.55
            },
            'national_plan_for_disaster_management': {
                'comprehensiveness': 0.7,
                'implementation': 0.5,
                'resource_allocation': 0.4,
                'effectiveness': 0.5
            },
            'standing_orders_on_disasters': {
                'comprehensiveness': 0.7,
                'implementation': 0.6,
                'awareness': 0.5,
                'effectiveness': 0.55
            },
            'climate_change_strategy': {
                'comprehensiveness': 0.7,
                'implementation': 0.4,
                'mainstreaming': 0.4,
                'effectiveness': 0.45
            },
            'building_codes': {
                'comprehensiveness': 0.6,
                'implementation': 0.4,
                'enforcement': 0.3,
                'effectiveness': 0.35
            },
            'land_use_planning': {
                'comprehensiveness': 0.5,
                'implementation': 0.3,
                'enforcement': 0.3,
                'effectiveness': 0.35
            }
        }
        
        # Coordination mechanisms
        self.coordination_mechanisms = {
            'vertical_coordination': {
                'information_flow': 0.5,
                'resource_coordination': 0.4,
                'command_structure': 0.6,
                'effectiveness': 0.5
            },
            'horizontal_coordination': {
                'inter_agency': 0.4,
                'inter_sectoral': 0.4,
                'public_private': 0.3,
                'effectiveness': 0.35
            },
            'civil_military_coordination': {
                'institutional_arrangements': 0.7,
                'joint_exercises': 0.5,
                'protocols': 0.6,
                'effectiveness': 0.6
            },
            'international_coordination': {
                'un_agencies': 0.7,
                'bilateral_donors': 0.6,
                'regional_mechanisms': 0.5,
                'effectiveness': 0.6
            }
        }
        
        # Resource management
        self.resource_management = {
            'budgetary_allocation': {
                'adequacy': 0.4,
                'predictability': 0.5,
                'flexibility': 0.4,
                'effectiveness': 0.45
            },
            'emergency_funds': {
                'availability': 0.6,
                'accessibility': 0.5,
                'sufficiency': 0.4,
                'effectiveness': 0.5
            },
            'resource_distribution': {
                'equity': 0.4,
                'timeliness': 0.5,
                'targeting': 0.5,
                'effectiveness': 0.45
            },
            'human_resources': {
                'skills': 0.5,
                'training': 0.5,
                'retention': 0.4,
                'effectiveness': 0.45
            }
        }
        
        # Governance quality factors
        self.governance_quality = {
            'transparency': {
                'information_disclosure': 0.4,
                'budget_transparency': 0.4,
                'decision_process_transparency': 0.3,
                'effectiveness': 0.35
            },
            'accountability': {
                'monitoring_mechanisms': 0.4,
                'grievance_redress': 0.3,
                'performance_evaluation': 0.4,
                'effectiveness': 0.35
            },
            'participation': {
                'community_involvement': 0.5,
                'civil_society_engagement': 0.5,
                'private_sector_participation': 0.4,
                'effectiveness': 0.45
            },
            'anti_corruption': {
                'prevention_measures': 0.3,
                'detection_mechanisms': 0.3,
                'enforcement': 0.3,
                'effectiveness': 0.3
            }
        }
        
        # Regional variations in governance
        self.regional_governance = {
            'dhaka_division': {
                'institutional_capacity': 1.2,
                'resource_availability': 1.3,
                'coordination': 1.1,
                'policy_implementation': 1.1,
                'corruption_vulnerability': 1.2  # Higher value = more vulnerable
            },
            'chittagong_division': {
                'institutional_capacity': 1.1,
                'resource_availability': 1.1,
                'coordination': 1.0,
                'policy_implementation': 1.0,
                'corruption_vulnerability': 1.1
            },
            'khulna_division': {
                'institutional_capacity': 1.0,
                'resource_availability': 0.9,
                'coordination': 1.0,
                'policy_implementation': 0.9,
                'corruption_vulnerability': 1.0
            },
            'rajshahi_division': {
                'institutional_capacity': 0.9,
                'resource_availability': 0.8,
                'coordination': 0.9,
                'policy_implementation': 0.9,
                'corruption_vulnerability': 0.9
            },
            'barisal_division': {
                'institutional_capacity': 0.8,
                'resource_availability': 0.7,
                'coordination': 0.8,
                'policy_implementation': 0.8,
                'corruption_vulnerability': 0.9
            },
            'sylhet_division': {
                'institutional_capacity': 0.9,
                'resource_availability': 0.8,
                'coordination': 0.8,
                'policy_implementation': 0.8,
                'corruption_vulnerability': 0.9
            },
            'rangpur_division': {
                'institutional_capacity': 0.8,
                'resource_availability': 0.7,
                'coordination': 0.8,
                'policy_implementation': 0.8,
                'corruption_vulnerability': 0.9
            },
            'mymensingh_division': {
                'institutional_capacity': 0.8,
                'resource_availability': 0.7,
                'coordination': 0.8,
                'policy_implementation': 0.8,
                'corruption_vulnerability': 0.9
            }
        }
        
        # Bangladesh governance trends over time
        self.governance_trends = {
            'institutional_development': 0.01,  # Annual improvement rate
            'policy_implementation': 0.005,
            'coordination_improvement': 0.01,
            'resource_management': 0.005,
            'corruption_reduction': 0.005
        }
        
        # Governance effectiveness by disaster phase
        self.phase_effectiveness = {
            'prevention_mitigation': 0.4,
            'preparedness': 0.6,
            'response': 0.7,
            'recovery': 0.5
        }

    def simulate_governance(self, region, time_period, disaster_phase, external_factors=None):
        """Simulate governance effectiveness for a given context
        
        Args:
            region: Administrative region (division)
            time_period: Years from baseline (2025)
            disaster_phase: Phase of disaster management
            external_factors: Dictionary of external factors affecting governance
            
        Returns:
            Dictionary with governance effectiveness metrics
        """
        if external_factors is None:
            external_factors = {}
        
        # Apply regional variations
        if region in self.regional_governance:
            regional_factors = self.regional_governance[region]
        else:
            # Default to national average
            regional_factors = {
                'institutional_capacity': 1.0,
                'resource_availability': 1.0,
                'coordination': 1.0,
                'policy_implementation': 1.0,
                'corruption_vulnerability': 1.0
            }
            
        # Calculate base effectiveness of each governance component
        institutional_effectiveness = self._calculate_institutional_effectiveness(
            region, disaster_phase)
        
        policy_effectiveness = self._calculate_policy_effectiveness(
            region, disaster_phase)
            
        coordination_effectiveness = self._calculate_coordination_effectiveness(
            region, disaster_phase)
            
        resource_effectiveness = self._calculate_resource_effectiveness(
            region, disaster_phase)
            
        governance_quality_score = self._calculate_governance_quality(
            region, disaster_phase)
            
        # Apply regional factors
        institutional_effectiveness *= regional_factors['institutional_capacity']
        policy_effectiveness *= regional_factors['policy_implementation']
        coordination_effectiveness *= regional_factors['coordination']
        resource_effectiveness *= regional_factors['resource_availability']
        
        # Apply quality and corruption effects
        corruption_impact = 1 - (governance_quality_score['corruption_level'] * 
                                regional_factors['corruption_vulnerability'])
        
        # Apply time trends (governance improvement over time)
        time_factor = self._calculate_time_evolution(time_period)
        
        institutional_effectiveness *= time_factor['institutional']
        policy_effectiveness *= time_factor['policy']
        coordination_effectiveness *= time_factor['coordination']
        resource_effectiveness *= time_factor['resource']
        
        # External shocks/factors
        political_stability = external_factors.get('political_stability', 1.0)
        economic_condition = external_factors.get('economic_condition', 1.0)
        disaster_frequency = external_factors.get('disaster_frequency', 1.0)
        international_support = external_factors.get('international_support', 1.0)
        
        # Apply external factors as multipliers
        external_factor = (
            political_stability * 0.3 +
            economic_condition * 0.3 +
            (1 / max(0.5, disaster_frequency)) * 0.2 +  # High frequency strains governance
            international_support * 0.2
        )
        
        # Calculate overall governance effectiveness
        overall_effectiveness = (
            institutional_effectiveness * 0.25 +
            policy_effectiveness * 0.25 +
            coordination_effectiveness * 0.25 +
            resource_effectiveness * 0.25
        ) * corruption_impact * external_factor
        
        # Calculate phase-specific effectiveness
        phase_base = self.phase_effectiveness.get(disaster_phase, 0.5)
        phase_effectiveness = phase_base * overall_effectiveness / 0.5  # Normalize
        
        # Cap values at reasonable limits
        phase_effectiveness = min(1.0, max(0.1, phase_effectiveness))
        overall_effectiveness = min(1.0, max(0.1, overall_effectiveness))
        
        # Compile results
        governance_results = {
            'overall_effectiveness': overall_effectiveness,
            'phase_effectiveness': phase_effectiveness,
            'institutional_effectiveness': institutional_effectiveness,
            'policy_effectiveness': policy_effectiveness,
            'coordination_effectiveness': coordination_effectiveness,
            'resource_effectiveness': resource_effectiveness,
            'governance_quality': governance_quality_score,
            'regional_factors': regional_factors,
            'time_factor': time_factor,
            'external_factor': external_factor,
            'corruption_impact': corruption_impact
        }
        
        return governance_results
        
    def _calculate_institutional_effectiveness(self, region, disaster_phase):
        """Calculate institutional effectiveness"""
        # Different weights by administrative level based on disaster phase
        admin_level_weights = {
            'prevention_mitigation': {
                'national': 0.4, 'divisional': 0.2, 
                'district': 0.2, 'upazila': 0.1, 'union': 0.1
            },
            'preparedness': {
                'national': 0.3, 'divisional': 0.2, 
                'district': 0.2, 'upazila': 0.15, 'union': 0.15
            },
            'response': {
                'national': 0.2, 'divisional': 0.2, 
                'district': 0.2, 'upazila': 0.2, 'union': 0.2
            },
            'recovery': {
                'national': 0.25, 'divisional': 0.2, 
                'district': 0.2, 'upazila': 0.15, 'union': 0.2
            }
        }
        
        # Use default weights if phase not found
        if disaster_phase not in admin_level_weights:
            disaster_phase = 'preparedness'
            
        weights = admin_level_weights[disaster_phase]
        
        # Calculate effectiveness at each level
        effectiveness_by_level = {}
        
        # National level
        national_avg = 0
        for institution, metrics in self.institutional_structure['national'].items():
            if isinstance(metrics, dict) and 'effectiveness' in metrics:
                national_avg += metrics['effectiveness']
        
        if len(self.institutional_structure['national']) > 0:
            effectiveness_by_level['national'] = national_avg / len(self.institutional_structure['national'])
        else:
            effectiveness_by_level['national'] = 0.5
            
        # Other levels
        for level in ['divisional', 'district', 'upazila', 'union']:
            level_avg = 0
            for institution, metrics in self.institutional_structure[level].items():
                if isinstance(metrics, dict) and 'effectiveness' in metrics:
                    level_avg += metrics['effectiveness']
            
            if len(self.institutional_structure[level]) > 0:
                effectiveness_by_level[level] = level_avg / len(self.institutional_structure[level])
            else:
                effectiveness_by_level[level] = 0.4
        
        # Calculate weighted average
        institutional_effectiveness = sum(
            effectiveness_by_level[level] * weights[level]
            for level in weights
        )
        
        return institutional_effectiveness
        
    def _calculate_policy_effectiveness(self, region, disaster_phase):
        """Calculate policy framework effectiveness"""
        # Different weights for policies based on disaster phase
        policy_weights = {
            'prevention_mitigation': {
                'disaster_management_act': 0.2,
                'national_plan_for_disaster_management': 0.2,
                'standing_orders_on_disasters': 0.1,
                'climate_change_strategy': 0.2,
                'building_codes': 0.2,
                'land_use_planning': 0.1
            },
            'preparedness': {
                'disaster_management_act': 0.2,
                'national_plan_for_disaster_management': 0.2,
                'standing_orders_on_disasters': 0.3,
                'climate_change_strategy': 0.1,
                'building_codes': 0.1,
                'land_use_planning': 0.1
            },
            'response': {
                'disaster_management_act': 0.2,
                'national_plan_for_disaster_management': 0.2,
                'standing_orders_on_disasters': 0.4,
                'climate_change_strategy': 0.0,
                'building_codes': 0.1,
                'land_use_planning': 0.1
            },
            'recovery': {
                'disaster_management_act': 0.2,
                'national_plan_for_disaster_management': 0.2,
                'standing_orders_on_disasters': 0.2,
                'climate_change_strategy': 0.1,
                'building_codes': 0.2,
                'land_use_planning': 0.1
            }
        }
        
        # Use default weights if phase not found
        if disaster_phase not in policy_weights:
            disaster_phase = 'preparedness'
            
        weights = policy_weights[disaster_phase]
        
        # Calculate weighted policy effectiveness
        policy_effectiveness = 0
        
        for policy, weight in weights.items():
            if policy in self.policy_framework and 'effectiveness' in self.policy_framework[policy]:
                policy_effectiveness += self.policy_framework[policy]['effectiveness'] * weight
        
        return policy_effectiveness
        
    def _calculate_coordination_effectiveness(self, region, disaster_phase):
        """Calculate coordination mechanism effectiveness"""
        # Different weights for coordination mechanisms based on disaster phase
        coordination_weights = {
            'prevention_mitigation': {
                'vertical_coordination': 0.3,
                'horizontal_coordination': 0.4,
                'civil_military_coordination': 0.1,
                'international_coordination': 0.2
            },
            'preparedness': {
                'vertical_coordination': 0.3,
                'horizontal_coordination': 0.3,
                'civil_military_coordination': 0.2,
                'international_coordination': 0.2
            },
            'response': {
                'vertical_coordination': 0.3,
                'horizontal_coordination': 0.2,
                'civil_military_coordination': 0.3,
                'international_coordination': 0.2
            },
            'recovery': {
                'vertical_coordination': 0.2,
                'horizontal_coordination': 0.3,
                'civil_military_coordination': 0.2,
                'international_coordination': 0.3
            }
        }
        
        # Use default weights if phase not found
        if disaster_phase not in coordination_weights:
            disaster_phase = 'preparedness'
            
        weights = coordination_weights[disaster_phase]
        
        # Calculate weighted coordination effectiveness
        coordination_effectiveness = 0
        
        for mechanism, weight in weights.items():
            if mechanism in self.coordination_mechanisms and 'effectiveness' in self.coordination_mechanisms[mechanism]:
                coordination_effectiveness += self.coordination_mechanisms[mechanism]['effectiveness'] * weight
        
        return coordination_effectiveness
        
    def _calculate_resource_effectiveness(self, region, disaster_phase):
        """Calculate resource management effectiveness"""
        # Different weights for resource components based on disaster phase
        resource_weights = {
            'prevention_mitigation': {
                'budgetary_allocation': 0.4,
                'emergency_funds': 0.1,
                'resource_distribution': 0.2,
                'human_resources': 0.3
            },
            'preparedness': {
                'budgetary_allocation': 0.3,
                'emergency_funds': 0.3,
                'resource_distribution': 0.2,
                'human_resources': 0.2
            },
            'response': {
                'budgetary_allocation': 0.1,
                'emergency_funds': 0.4,
                'resource_distribution': 0.3,
                'human_resources': 0.2
            },
            'recovery': {
                'budgetary_allocation': 0.3,
                'emergency_funds': 0.2,
                'resource_distribution': 0.3,
                'human_resources': 0.2
            }
        }
        
        # Use default weights if phase not found
        if disaster_phase not in resource_weights:
            disaster_phase = 'preparedness'
            
        weights = resource_weights[disaster_phase]
        
        # Calculate weighted resource effectiveness
        resource_effectiveness = 0
        
        for resource, weight in weights.items():
            if resource in self.resource_management and 'effectiveness' in self.resource_management[resource]:
                resource_effectiveness += self.resource_management[resource]['effectiveness'] * weight
        
        return resource_effectiveness
        
    def _calculate_governance_quality(self, region, disaster_phase):
        """Calculate governance quality metrics"""
        governance_quality_scores = {}
        
        # Transparency
        transparency_score = 0
        transparency_count = 0
        for aspect, metrics in self.governance_quality['transparency'].items():
            if aspect != 'effectiveness':
                transparency_score += metrics
                transparency_count += 1
                
        if transparency_count > 0:
            governance_quality_scores['transparency'] = transparency_score / transparency_count
        else:
            governance_quality_scores['transparency'] = 0.4
            
        # Accountability
        accountability_score = 0
        accountability_count = 0
        for aspect, metrics in self.governance_quality['accountability'].items():
            if aspect != 'effectiveness':
                accountability_score += metrics
                accountability_count += 1
                
        if accountability_count > 0:
            governance_quality_scores['accountability'] = accountability_score / accountability_count
        else:
            governance_quality_scores['accountability'] = 0.4
            
        # Participation
        participation_score = 0
        participation_count = 0
        for aspect, metrics in self.governance_quality['participation'].items():
            if aspect != 'effectiveness':
                participation_score += metrics
                participation_count += 1
                
        if participation_count > 0:
            governance_quality_scores['participation'] = participation_score / participation_count
        else:
            governance_quality_scores['participation'] = 0.4
            
        # Corruption level (higher score = more corruption)
        corruption_score = 0
        corruption_count = 0
        for aspect, metrics in self.governance_quality['anti_corruption'].items():
            if aspect != 'effectiveness':
                corruption_score += (1 - metrics)  # Invert scores (lack of anti-corruption = corruption)
                corruption_count += 1
                
        if corruption_count > 0:
            governance_quality_scores['corruption_level'] = corruption_score / corruption_count
        else:
            governance_quality_scores['corruption_level'] = 0.6
            
        # Overall quality
        governance_quality_scores['overall_quality'] = (
            governance_quality_scores['transparency'] * 0.25 +
            governance_quality_scores['accountability'] * 0.25 +
            governance_quality_scores['participation'] * 0.25 +
            (1 - governance_quality_scores['corruption_level']) * 0.25  # Anti-corruption impact
        )
        
        return governance_quality_scores
        
    def _calculate_time_evolution(self, time_period):
        """Calculate evolution of governance capacities over time"""
        # Maximum improvement caps
        max_improvement = {
            'institutional': 1.5,  # 50% maximum improvement
            'policy': 1.4,
            'coordination': 1.4,
            'resource': 1.3,
            'corruption': 0.7   # Minimum corruption level (30% reduction)
        }
        
        # Calculate time factors based on trend rates
        institutional_factor = min(
            max_improvement['institutional'],
            1 + self.governance_trends['institutional_development'] * time_period
        )
        
        policy_factor = min(
            max_improvement['policy'],
            1 + self.governance_trends['policy_implementation'] * time_period
        )
        
        coordination_factor = min(
            max_improvement['coordination'],
            1 + self.governance_trends['coordination_improvement'] * time_period
        )
        
        resource_factor = min(
            max_improvement['resource'],
            1 + self.governance_trends['resource_management'] * time_period
        )
        
        corruption_reduction = max(
            max_improvement['corruption'],
            1 - self.governance_trends['corruption_reduction'] * time_period
        )
        
        time_factors = {
            'institutional': institutional_factor,
            'policy': policy_factor,
            'coordination': coordination_factor,
            'resource': resource_factor,
            'corruption_reduction': corruption_reduction
        }
        
        return time_factors
