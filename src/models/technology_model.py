"""
TechnologyModel: Models technology adoption for disaster risk management
"""

import numpy as np
from collections import defaultdict

class TechnologyModel:
    """Model technology adoption for disaster risk management in Bangladesh"""
    def __init__(self):
        # Initialize technology parameters
        self._initialize_technology_parameters()
        
    def _initialize_technology_parameters(self):
        """Initialize parameters for technology modeling"""
        # Early warning technologies
        self.early_warning_tech = {
            'weather_forecasting': {
                'current_capacity': 0.7,  # Current capacity (0-1 scale)
                'adoption_rate': 0.03,    # Annual improvement rate
                'regional_availability': {
                    'urban': 0.8,         # Availability by region type
                    'rural': 0.6,
                    'coastal': 0.7,
                    'remote': 0.5
                },
                'effectiveness': 0.75     # Effectiveness when available
            },
            'remote_sensing': {
                'current_capacity': 0.6,
                'adoption_rate': 0.04,
                'regional_availability': {
                    'urban': 0.7,
                    'rural': 0.6,
                    'coastal': 0.8,
                    'remote': 0.5
                },
                'effectiveness': 0.8
            },
            'mobile_alerts': {
                'current_capacity': 0.75,
                'adoption_rate': 0.05,
                'regional_availability': {
                    'urban': 0.9,
                    'rural': 0.7,
                    'coastal': 0.8,
                    'remote': 0.6
                },
                'effectiveness': 0.85
            },
            'community_warning_systems': {
                'current_capacity': 0.65,
                'adoption_rate': 0.02,
                'regional_availability': {
                    'urban': 0.7,
                    'rural': 0.8,
                    'coastal': 0.9,
                    'remote': 0.7
                },
                'effectiveness': 0.7
            }
        }
        
        # Resilient infrastructure technologies
        self.resilient_infrastructure_tech = {
            'flood_resistant_construction': {
                'current_adoption': 0.3,   # Current adoption rate
                'adoption_rate': 0.02,     # Annual increase
                'regional_availability': {
                    'urban': 0.5,
                    'rural': 0.2,
                    'coastal': 0.4,
                    'remote': 0.1
                },
                'effectiveness': 0.7
            },
            'water_management_systems': {
                'current_adoption': 0.4,
                'adoption_rate': 0.03,
                'regional_availability': {
                    'urban': 0.6,
                    'rural': 0.3,
                    'coastal': 0.5,
                    'remote': 0.2
                },
                'effectiveness': 0.6
            },
            'resilient_energy_systems': {
                'current_adoption': 0.3,
                'adoption_rate': 0.04,
                'regional_availability': {
                    'urban': 0.5,
                    'rural': 0.2,
                    'coastal': 0.3,
                    'remote': 0.1
                },
                'effectiveness': 0.7
            },
            'climate_smart_agriculture': {
                'current_adoption': 0.25,
                'adoption_rate': 0.03,
                'regional_availability': {
                    'urban': 0.3,
                    'rural': 0.4,
                    'coastal': 0.3,
                    'remote': 0.2
                },
                'effectiveness': 0.6
            }
        }
        
        # Information and communication technologies
        self.ict_tech = {
            'mobile_networks': {
                'current_coverage': 0.9,   # Population coverage
                'growth_rate': 0.02,
                'regional_availability': {
                    'urban': 0.98,
                    'rural': 0.85,
                    'coastal': 0.9,
                    'remote': 0.7
                },
                'reliability': 0.8         # Network reliability
            },
            'internet_access': {
                'current_coverage': 0.65,
                'growth_rate': 0.05,
                'regional_availability': {
                    'urban': 0.85,
                    'rural': 0.5,
                    'coastal': 0.6,
                    'remote': 0.3
                },
                'reliability': 0.75
            },
            'geospatial_systems': {
                'current_adoption': 0.5,
                'adoption_rate': 0.04,
                'regional_availability': {
                    'urban': 0.7,
                    'rural': 0.4,
                    'coastal': 0.6,
                    'remote': 0.3
                },
                'effectiveness': 0.8
            },
            'social_media_penetration': {
                'current_usage': 0.6,
                'growth_rate': 0.05,
                'regional_availability': {
                    'urban': 0.8,
                    'rural': 0.5,
                    'coastal': 0.6,
                    'remote': 0.3
                },
                'effectiveness': 0.75
            }
        }
        
        # Technology adoption barriers
        self.adoption_barriers = {
            'economic': {
                'cost_barrier': 0.7,      # Significance of barrier (0-1)
                'annual_reduction': 0.03,  # Annual reduction in barrier
                'regional_variation': {
                    'urban': 0.6,
                    'rural': 0.8,
                    'coastal': 0.7,
                    'remote': 0.9
                }
            },
            'technical': {
                'literacy_barrier': 0.6,
                'annual_reduction': 0.02,
                'regional_variation': {
                    'urban': 0.5,
                    'rural': 0.7,
                    'coastal': 0.6,
                    'remote': 0.8
                }
            },
            'infrastructure': {
                'dependency_barrier': 0.65,
                'annual_reduction': 0.03,
                'regional_variation': {
                    'urban': 0.4,
                    'rural': 0.7,
                    'coastal': 0.6,
                    'remote': 0.8
                }
            },
            'institutional': {
                'governance_barrier': 0.6,
                'annual_reduction': 0.02,
                'regional_variation': {
                    'urban': 0.5,
                    'rural': 0.6,
                    'coastal': 0.6,
                    'remote': 0.7
                }
            }
        }
        
        # Technology effectiveness for different hazards
        self.hazard_tech_effectiveness = {
            'flood': {
                'early_warning': 0.8,
                'resilient_infrastructure': 0.7,
                'ict': 0.6
            },
            'cyclone': {
                'early_warning': 0.9,
                'resilient_infrastructure': 0.6,
                'ict': 0.7
            },
            'drought': {
                'early_warning': 0.7,
                'resilient_infrastructure': 0.5,
                'ict': 0.6
            },
            'landslide': {
                'early_warning': 0.6,
                'resilient_infrastructure': 0.5,
                'ict': 0.5
            },
            'river_erosion': {
                'early_warning': 0.5,
                'resilient_infrastructure': 0.7,
                'ict': 0.4
            }
        }

    def simulate_technology_adoption(self, region_type, time_period, hazard_type, socioeconomic_profile):
        """Simulate technology adoption and effectiveness for disaster risk reduction
        
        Args:
            region_type: Type of region (urban, rural, coastal, remote)
            time_period: Years from baseline (2025)
            hazard_type: Type of hazard being considered
            socioeconomic_profile: Socioeconomic characteristics that affect adoption
            
        Returns:
            Dictionary with technology adoption and effectiveness metrics
        """
        # Get baseline regional type for technology availability
        if 'urban' in region_type.lower():
            region_category = 'urban'
        elif 'coastal' in region_type.lower():
            region_category = 'coastal'
        elif 'remote' in region_type.lower() or 'char' in region_type.lower():
            region_category = 'remote'
        else:
            region_category = 'rural'
            
        # Calculate early warning technology adoption and effectiveness
        early_warning_metrics = self._calculate_early_warning_tech(
            region_category, time_period, hazard_type)
            
        # Calculate resilient infrastructure technology adoption
        infrastructure_metrics = self._calculate_infrastructure_tech(
            region_category, time_period, hazard_type)
            
        # Calculate ICT adoption and effectiveness
        ict_metrics = self._calculate_ict_tech(
            region_category, time_period, hazard_type)
            
        # Calculate adoption barriers
        barriers = self._calculate_adoption_barriers(
            region_category, time_period, socioeconomic_profile)
            
        # Apply barrier effects to technology adoption
        barrier_factor = (
            (1 - barriers['economic'] * 0.4) * 
            (1 - barriers['technical'] * 0.3) * 
            (1 - barriers['infrastructure'] * 0.2) * 
            (1 - barriers['institutional'] * 0.1)
        )
        
        # Adjust adoption rates based on barriers
        early_warning_metrics['effective_adoption'] *= barrier_factor
        infrastructure_metrics['effective_adoption'] *= barrier_factor
        ict_metrics['effective_adoption'] *= barrier_factor
        
        # Calculate hazard-specific technology effectiveness
        if hazard_type in self.hazard_tech_effectiveness:
            hazard_effectiveness = self.hazard_tech_effectiveness[hazard_type]
        else:
            # Default to flood if hazard type not found
            hazard_effectiveness = self.hazard_tech_effectiveness['flood']
            
        # Calculate overall technology contribution to risk reduction
        early_warning_contribution = (
            early_warning_metrics['effective_adoption'] * 
            early_warning_metrics['effectiveness'] * 
            hazard_effectiveness['early_warning']
        )
        
        infrastructure_contribution = (
            infrastructure_metrics['effective_adoption'] * 
            infrastructure_metrics['effectiveness'] * 
            hazard_effectiveness['resilient_infrastructure']
        )
        
        ict_contribution = (
            ict_metrics['effective_adoption'] * 
            ict_metrics['effectiveness'] * 
            hazard_effectiveness['ict']
        )
        
        # Overall technology effectiveness for risk reduction
        overall_effectiveness = (
            early_warning_contribution * 0.4 +
            infrastructure_contribution * 0.4 +
            ict_contribution * 0.2
        )
        
        # Compile results
        technology_results = {
            'early_warning': early_warning_metrics,
            'resilient_infrastructure': infrastructure_metrics,
            'ict': ict_metrics,
            'adoption_barriers': barriers,
            'barrier_factor': barrier_factor,
            'early_warning_contribution': early_warning_contribution,
            'infrastructure_contribution': infrastructure_contribution,
            'ict_contribution': ict_contribution,
            'overall_effectiveness': overall_effectiveness
        }
        
        return technology_results
        
    def _calculate_early_warning_tech(self, region_category, time_period, hazard_type):
        """Calculate early warning technology adoption and effectiveness"""
        # Initialize metrics
        adoption = 0
        availability = 0
        effectiveness = 0
        tech_count = 0
        
        # Calculate for each early warning technology
        for tech, params in self.early_warning_tech.items():
            # Calculate adoption with time evolution
            tech_adoption = min(
                1.0,  # Cap at 100%
                params['current_capacity'] + params['adoption_rate'] * time_period
            )
            
            # Get regional availability
            tech_availability = params['regional_availability'].get(region_category, 0.5)
            
            # Sum up metrics
            adoption += tech_adoption
            availability += tech_availability
            effectiveness += params['effectiveness']
            tech_count += 1
            
        # Calculate averages
        if tech_count > 0:
            avg_adoption = adoption / tech_count
            avg_availability = availability / tech_count
            avg_effectiveness = effectiveness / tech_count
        else:
            avg_adoption = 0.5
            avg_availability = 0.5
            avg_effectiveness = 0.5
            
        # Calculate effective adoption (adoption × availability)
        effective_adoption = avg_adoption * avg_availability
        
        # Return early warning metrics
        return {
            'adoption': avg_adoption,
            'availability': avg_availability,
            'effectiveness': avg_effectiveness,
            'effective_adoption': effective_adoption
        }
        
    def _calculate_infrastructure_tech(self, region_category, time_period, hazard_type):
        """Calculate resilient infrastructure technology adoption and effectiveness"""
        # Initialize metrics
        adoption = 0
        availability = 0
        effectiveness = 0
        tech_count = 0
        
        # Calculate for each resilient infrastructure technology
        for tech, params in self.resilient_infrastructure_tech.items():
            # Calculate adoption with time evolution
            tech_adoption = min(
                1.0,  # Cap at 100%
                params['current_adoption'] + params['adoption_rate'] * time_period
            )
            
            # Get regional availability
            tech_availability = params['regional_availability'].get(region_category, 0.5)
            
            # Sum up metrics
            adoption += tech_adoption
            availability += tech_availability
            effectiveness += params['effectiveness']
            tech_count += 1
            
        # Calculate averages
        if tech_count > 0:
            avg_adoption = adoption / tech_count
            avg_availability = availability / tech_count
            avg_effectiveness = effectiveness / tech_count
        else:
            avg_adoption = 0.3
            avg_availability = 0.3
            avg_effectiveness = 0.5
            
        # Calculate effective adoption (adoption × availability)
        effective_adoption = avg_adoption * avg_availability
        
        # Return infrastructure metrics
        return {
            'adoption': avg_adoption,
            'availability': avg_availability,
            'effectiveness': avg_effectiveness,
            'effective_adoption': effective_adoption
        }
        
    def _calculate_ict_tech(self, region_category, time_period, hazard_type):
        """Calculate ICT adoption and effectiveness"""
        # Initialize metrics
        adoption = 0
        availability = 0
        effectiveness = 0
        tech_count = 0
        
        # Calculate for each ICT technology
        for tech, params in self.ict_tech.items():
            # Calculate adoption with time evolution
            if 'current_coverage' in params:
                tech_adoption = min(
                    1.0,  # Cap at 100%
                    params['current_coverage'] + params['growth_rate'] * time_period
                )
                tech_effectiveness = params['reliability']
            else:
                tech_adoption = min(
                    1.0,
                    params['current_adoption'] + params['adoption_rate'] * time_period
                )
                tech_effectiveness = params['effectiveness']
            
            # Get regional availability
            tech_availability = params['regional_availability'].get(region_category, 0.5)
            
            # Sum up metrics
            adoption += tech_adoption
            availability += tech_availability
            effectiveness += tech_effectiveness
            tech_count += 1
            
        # Calculate averages
        if tech_count > 0:
            avg_adoption = adoption / tech_count
            avg_availability = availability / tech_count
            avg_effectiveness = effectiveness / tech_count
        else:
            avg_adoption = 0.5
            avg_availability = 0.5
            avg_effectiveness = 0.6
            
        # Calculate effective adoption (adoption × availability)
        effective_adoption = avg_adoption * avg_availability
        
        # Return ICT metrics
        return {
            'adoption': avg_adoption,
            'availability': avg_availability,
            'effectiveness': avg_effectiveness,
            'effective_adoption': effective_adoption
        }
        
    def _calculate_adoption_barriers(self, region_category, time_period, socioeconomic_profile):
        """Calculate technology adoption barriers"""
        # Extract socioeconomic factors that affect barriers
        poverty_rate = socioeconomic_profile.get('poverty_rate', 0.3)
        education_level = socioeconomic_profile.get('education_level', 0.6)
        service_access = socioeconomic_profile.get('service_access', 0.5)
        
        # Initialize barrier metrics
        barriers = {}
        
        # Calculate economic barriers
        economic_base = self.adoption_barriers['economic']['cost_barrier']
        economic_reduction = self.adoption_barriers['economic']['annual_reduction'] * time_period
        economic_regional = self.adoption_barriers['economic']['regional_variation'].get(region_category, 0.7)
        
        # Economic barrier is affected by poverty rate
        poverty_effect = poverty_rate / 0.3  # Normalize against 30% poverty rate
        barriers['economic'] = max(
            0.1,  # Minimum barrier
            (economic_base * economic_regional - economic_reduction) * poverty_effect
        )
        
        # Calculate technical barriers
        technical_base = self.adoption_barriers['technical']['literacy_barrier']
        technical_reduction = self.adoption_barriers['technical']['annual_reduction'] * time_period
        technical_regional = self.adoption_barriers['technical']['regional_variation'].get(region_category, 0.6)
        
        # Technical barrier is affected by education level
        education_effect = (1 - education_level) / 0.4  # Normalize against 60% education level
        barriers['technical'] = max(
            0.1,
            (technical_base * technical_regional - technical_reduction) * education_effect
        )
        
        # Calculate infrastructure barriers
        infra_base = self.adoption_barriers['infrastructure']['dependency_barrier']
        infra_reduction = self.adoption_barriers['infrastructure']['annual_reduction'] * time_period
        infra_regional = self.adoption_barriers['infrastructure']['regional_variation'].get(region_category, 0.65)
        
        # Infrastructure barrier is affected by service access
        service_effect = (1 - service_access) / 0.5  # Normalize against 50% service access
        barriers['infrastructure'] = max(
            0.1,
            (infra_base * infra_regional - infra_reduction) * service_effect
        )
        
        # Calculate institutional barriers
        inst_base = self.adoption_barriers['institutional']['governance_barrier']
        inst_reduction = self.adoption_barriers['institutional']['annual_reduction'] * time_period
        inst_regional = self.adoption_barriers['institutional']['regional_variation'].get(region_category, 0.6)
        
        # Assume institutional barriers reduction is less dependent on socioeconomic factors
        barriers['institutional'] = max(
            0.2,
            inst_base * inst_regional - inst_reduction
        )
        
        return barriers
