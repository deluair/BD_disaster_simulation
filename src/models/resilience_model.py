"""
ResilienceModel: Models disaster resilience capacities across systems
"""

import numpy as np
from collections import defaultdict

class ResilienceModel:
    """Model disaster resilience capacities across different systems in Bangladesh"""
    def __init__(self):
        # Initialize resilience parameters
        self._initialize_resilience_parameters()
        
    def _initialize_resilience_parameters(self):
        """Initialize parameters for resilience modeling"""
        # Infrastructure resilience factors
        self.infrastructure_resilience = {
            'building_codes': {
                'enforcement_level': {
                    'major_urban': 0.7,  # 70% enforcement in major urban areas
                    'other_urban': 0.4,  # 40% in other urban areas
                    'rural': 0.2         # 20% in rural areas
                },
                'code_quality': 0.6,     # 60% quality/comprehensiveness
                'resilience_contribution': 0.3  # Contribution to overall resilience
            },
            'critical_infrastructure': {
                'redundancy': {
                    'power': 0.3,        # Redundancy in power systems
                    'water': 0.4,        # Redundancy in water systems
                    'healthcare': 0.5,   # Redundancy in healthcare
                    'transportation': 0.4 # Redundancy in transportation
                },
                'robustness': {
                    'power': 0.4,        # Structural robustness
                    'water': 0.5,
                    'healthcare': 0.6,
                    'transportation': 0.5
                },
                'resilience_contribution': 0.4
            },
            'protective_infrastructure': {
                'coverage': {
                    'coastal': 0.5,      # Coverage of embankments/polders
                    'riverine': 0.6,     # Coverage of flood protection
                    'urban': 0.4         # Coverage of drainage systems
                },
                'design_standard': {
                    'coastal': 0.5,      # Design relative to hazard intensity
                    'riverine': 0.6,
                    'urban': 0.5
                },
                'maintenance': {
                    'coastal': 0.4,      # Maintenance level
                    'riverine': 0.5,
                    'urban': 0.4
                },
                'resilience_contribution': 0.3
            }
        }
        
        # Social resilience parameters
        self.social_resilience = {
            'awareness': {
                'hazard_knowledge': {
                    'urban': 0.6,
                    'rural': 0.5,
                    'coastal': 0.7,      # Higher in frequently affected areas
                    'char_lands': 0.7
                },
                'risk_perception': {
                    'urban': 0.5,
                    'rural': 0.6,        # Often higher in rural areas
                    'coastal': 0.8,
                    'char_lands': 0.8
                },
                'resilience_contribution': 0.2
            },
            'social_capital': {
                'community_cohesion': {
                    'urban': 0.5,
                    'rural': 0.8,        # Higher in rural communities
                    'coastal': 0.7,
                    'char_lands': 0.7
                },
                'social_networks': {
                    'urban': 0.7,
                    'rural': 0.8,
                    'coastal': 0.7,
                    'char_lands': 0.6
                },
                'resilience_contribution': 0.3
            },
            'education': {
                'literacy': {
                    'urban': 0.8,
                    'rural': 0.6,
                    'male': 0.7,
                    'female': 0.6
                },
                'disaster_education': {
                    'urban': 0.5,
                    'rural': 0.4,
                    'coastal': 0.6,
                    'char_lands': 0.5
                },
                'resilience_contribution': 0.2
            },
            'coping_mechanisms': {
                'traditional_knowledge': {
                    'urban': 0.3,
                    'rural': 0.7,
                    'coastal': 0.8,
                    'indigenous': 0.9
                },
                'adaptation_practices': {
                    'agricultural': 0.6,
                    'housing': 0.5,
                    'livelihood': 0.5
                },
                'resilience_contribution': 0.3
            }
        }
        
        # Economic resilience indicators
        self.economic_resilience = {
            'household_financial': {
                'savings_rate': {
                    'urban_high_income': 0.6,
                    'urban_middle_income': 0.4,
                    'urban_low_income': 0.1,
                    'rural_high_income': 0.5,
                    'rural_middle_income': 0.3,
                    'rural_low_income': 0.1
                },
                'income_diversity': {
                    'urban_high_income': 0.7,
                    'urban_middle_income': 0.5,
                    'urban_low_income': 0.3,
                    'rural_high_income': 0.6,
                    'rural_middle_income': 0.4,
                    'rural_low_income': 0.2
                },
                'resilience_contribution': 0.3
            },
            'business_resilience': {
                'business_continuity': {
                    'large': 0.6,
                    'medium': 0.4,
                    'small': 0.2,
                    'micro': 0.1
                },
                'supply_chain_resilience': {
                    'manufacturing': 0.5,
                    'agriculture': 0.3,
                    'service': 0.6,
                    'informal': 0.2
                },
                'resilience_contribution': 0.3
            },
            'financial_protection': {
                'insurance_coverage': {
                    'urban_high_income': 0.4,
                    'urban_middle_income': 0.2,
                    'urban_low_income': 0.05,
                    'rural_high_income': 0.3,
                    'rural_middle_income': 0.1,
                    'rural_low_income': 0.01
                },
                'social_safety_nets': {
                    'coverage': 0.4,      # Population coverage
                    'adequacy': 0.3       # Adequacy of benefits
                },
                'resilience_contribution': 0.2
            },
            'economic_diversity': {
                'sector_diversity': 0.6,  # Economy-wide diversity
                'geographic_distribution': 0.5,  # Geographic distribution of economic activity
                'resilience_contribution': 0.2
            }
        }
        
        # Environmental/ecosystem resilience
        self.ecosystem_resilience = {
            'forest_ecosystems': {
                'mangrove_coverage': 0.5,  # Remaining coverage vs potential
                'mangrove_health': 0.6,    # Health of existing mangroves
                'forest_fragmentation': 0.4,  # Fragmentation (lower is better)
                'resilience_contribution': 0.4
            },
            'wetlands': {
                'wetland_coverage': 0.4,
                'wetland_health': 0.5,
                'hydrological_function': 0.6,
                'resilience_contribution': 0.3
            },
            'agricultural_ecosystems': {
                'soil_health': 0.5,
                'crop_diversity': 0.6,
                'sustainable_practices': 0.4,
                'resilience_contribution': 0.3
            }
        }
        
        # Institutional resilience systems
        self.institutional_resilience = {
            'disaster_governance': {
                'policy_framework': 0.7,  # Good policy framework
                'institutional_capacity': 0.5,
                'coordination': 0.5,
                'implementation': 0.4,
                'resilience_contribution': 0.3
            },
            'early_warning_systems': {
                'technical_capacity': 0.7,
                'institutional_capacity': 0.5,
                'communication_systems': 0.6,
                'community_integration': 0.5,
                'resilience_contribution': 0.3
            },
            'planning_systems': {
                'hazard_mapping': 0.6,
                'land_use_planning': 0.4,
                'building_control': 0.5,
                'implementation': 0.3,
                'resilience_contribution': 0.2
            },
            'knowledge_systems': {
                'research_capacity': 0.6,
                'indigenous_knowledge': 0.7,
                'knowledge_integration': 0.4,
                'resilience_contribution': 0.2
            }
        }
        
        # Regional resilience variations across Bangladesh
        self.regional_resilience = {
            'dhaka_division': {
                'infrastructure': 1.2,    # Multiplier relative to national average
                'social': 1.1,
                'economic': 1.3,
                'ecosystem': 0.7,
                'institutional': 1.2
            },
            'chittagong_division': {
                'infrastructure': 1.1,
                'social': 1.0,
                'economic': 1.2,
                'ecosystem': 0.9,
                'institutional': 1.0
            },
            'khulna_division': {
                'infrastructure': 0.9,
                'social': 1.0,
                'economic': 0.9,
                'ecosystem': 1.1,         # Sundarbans effect
                'institutional': 0.9
            },
            'rajshahi_division': {
                'infrastructure': 0.8,
                'social': 0.9,
                'economic': 0.8,
                'ecosystem': 0.7,
                'institutional': 0.8
            },
            'barisal_division': {
                'infrastructure': 0.7,
                'social': 0.9,
                'economic': 0.7,
                'ecosystem': 1.0,
                'institutional': 0.8
            },
            'sylhet_division': {
                'infrastructure': 0.8,
                'social': 0.9,
                'economic': 0.9,
                'ecosystem': 1.0,         # Haor ecosystems
                'institutional': 0.8
            },
            'rangpur_division': {
                'infrastructure': 0.7,
                'social': 0.8,
                'economic': 0.7,
                'ecosystem': 0.8,
                'institutional': 0.7
            },
            'mymensingh_division': {
                'infrastructure': 0.8,
                'social': 0.9,
                'economic': 0.8,
                'ecosystem': 0.9,
                'institutional': 0.8
            }
        }

    def calculate_resilience(self, region_type, socioeconomic_profile, governance_quality, hazard_type):
        """Calculate resilience scores for a specific context
        
        Args:
            region_type: Type of region (urban, rural, coastal, etc.)
            socioeconomic_profile: Socioeconomic characteristics
            governance_quality: Governance effectiveness metrics
            hazard_type: Type of hazard being considered
            
        Returns:
            Dictionary with resilience scores across dimensions
        """
        # Resilience dimensions to calculate
        resilience_dimensions = {
            'infrastructure_resilience': 0.0,
            'social_resilience': 0.0,
            'economic_resilience': 0.0,
            'ecosystem_resilience': 0.0,
            'institutional_resilience': 0.0
        }
        
        # Get regional adjustment factors
        division = socioeconomic_profile.get('division', 'dhaka_division')
        if division in self.regional_resilience:
            regional_factors = self.regional_resilience[division]
        else:
            # Default to national average
            regional_factors = {
                'infrastructure': 1.0,
                'social': 1.0,
                'economic': 1.0,
                'ecosystem': 1.0,
                'institutional': 1.0
            }
        
        # Calculate infrastructure resilience
        infrastructure_resilience = self._calculate_infrastructure_resilience(
            region_type, socioeconomic_profile, hazard_type)
        resilience_dimensions['infrastructure_resilience'] = (
            infrastructure_resilience * regional_factors['infrastructure'])
        
        # Calculate social resilience
        social_resilience = self._calculate_social_resilience(
            region_type, socioeconomic_profile, hazard_type)
        resilience_dimensions['social_resilience'] = (
            social_resilience * regional_factors['social'])
        
        # Calculate economic resilience
        economic_resilience = self._calculate_economic_resilience(
            region_type, socioeconomic_profile, hazard_type)
        resilience_dimensions['economic_resilience'] = (
            economic_resilience * regional_factors['economic'])
        
        # Calculate ecosystem resilience
        ecosystem_resilience = self._calculate_ecosystem_resilience(
            region_type, hazard_type)
        resilience_dimensions['ecosystem_resilience'] = (
            ecosystem_resilience * regional_factors['ecosystem'])
        
        # Calculate institutional resilience
        institutional_resilience = self._calculate_institutional_resilience(
            governance_quality, hazard_type)
        resilience_dimensions['institutional_resilience'] = (
            institutional_resilience * regional_factors['institutional'])
        
        # Calculate overall resilience score (weighted average)
        weights = {
            'infrastructure_resilience': 0.25,
            'social_resilience': 0.2,
            'economic_resilience': 0.2,
            'ecosystem_resilience': 0.15,
            'institutional_resilience': 0.2
        }
        
        overall_resilience = sum(
            resilience_dimensions[dim] * weights[dim] for dim in resilience_dimensions
        )
        
        # Add overall score to results
        resilience_dimensions['overall_resilience'] = overall_resilience
        
        # Calculate hazard-specific resilience
        resilience_dimensions['hazard_specific_resilience'] = self._calculate_hazard_specific_resilience(
            hazard_type, resilience_dimensions)
        
        return resilience_dimensions

    def _calculate_infrastructure_resilience(self, region_type, socioeconomic_profile, hazard_type):
        """Calculate infrastructure resilience score"""
        # Building code resilience
        if 'urban' in region_type and 'major' in region_type:
            building_code_enforcement = self.infrastructure_resilience['building_codes']['enforcement_level']['major_urban']
        elif 'urban' in region_type:
            building_code_enforcement = self.infrastructure_resilience['building_codes']['enforcement_level']['other_urban']
        else:
            building_code_enforcement = self.infrastructure_resilience['building_codes']['enforcement_level']['rural']
            
        code_quality = self.infrastructure_resilience['building_codes']['code_quality']
        building_code_resilience = building_code_enforcement * code_quality
        
        # Critical infrastructure resilience
        ci_resilience = {}
        for system, redundancy in self.infrastructure_resilience['critical_infrastructure']['redundancy'].items():
            robustness = self.infrastructure_resilience['critical_infrastructure']['robustness'][system]
            ci_resilience[system] = (redundancy + robustness) / 2
        
        avg_ci_resilience = sum(ci_resilience.values()) / len(ci_resilience)
        
        # Protective infrastructure resilience
        if 'coastal' in region_type:
            pi_type = 'coastal'
        elif 'riverine' in region_type or 'floodplain' in region_type:
            pi_type = 'riverine'
        else:
            pi_type = 'urban'
            
        coverage = self.infrastructure_resilience['protective_infrastructure']['coverage'][pi_type]
        design = self.infrastructure_resilience['protective_infrastructure']['design_standard'][pi_type]
        maintenance = self.infrastructure_resilience['protective_infrastructure']['maintenance'][pi_type]
        
        protective_resilience = (coverage * 0.4 + design * 0.4 + maintenance * 0.2)
        
        # Combine infrastructure resilience components with weights
        infrastructure_resilience = (
            building_code_resilience * self.infrastructure_resilience['building_codes']['resilience_contribution'] +
            avg_ci_resilience * self.infrastructure_resilience['critical_infrastructure']['resilience_contribution'] +
            protective_resilience * self.infrastructure_resilience['protective_infrastructure']['resilience_contribution']
        )
        
        return infrastructure_resilience
        
    def _calculate_social_resilience(self, region_type, socioeconomic_profile, hazard_type):
        """Calculate social resilience score"""
        # Determine region category for lookup
        region_category = 'urban' if 'urban' in region_type else 'rural'
        if 'coastal' in region_type:
            region_category = 'coastal'
        elif 'char' in region_type:
            region_category = 'char_lands'
            
        # Calculate awareness component
        hazard_knowledge = self.social_resilience['awareness']['hazard_knowledge'].get(region_category, 0.5)
        risk_perception = self.social_resilience['awareness']['risk_perception'].get(region_category, 0.5)
        awareness_score = (hazard_knowledge + risk_perception) / 2
        
        # Calculate social capital component
        community_cohesion = self.social_resilience['social_capital']['community_cohesion'].get(region_category, 0.5)
        social_networks = self.social_resilience['social_capital']['social_networks'].get(region_category, 0.5)
        social_capital_score = (community_cohesion + social_networks) / 2
        
        # Calculate education component
        literacy = self.social_resilience['education']['literacy'].get(region_category, 0.5)
        disaster_education = self.social_resilience['education']['disaster_education'].get(region_category, 0.4)
        education_score = (literacy * 0.6 + disaster_education * 0.4)
        
        # Calculate coping mechanisms component
        traditional_knowledge = self.social_resilience['coping_mechanisms']['traditional_knowledge'].get(region_category, 0.5)
        
        # Determine adaptation practices category
        if 'agricultural' in socioeconomic_profile.get('livelihood_type', ''):
            adaptation_category = 'agricultural'
        elif 'housing' in socioeconomic_profile.get('vulnerability_type', ''):
            adaptation_category = 'housing'
        else:
            adaptation_category = 'livelihood'
            
        adaptation_practices = self.social_resilience['coping_mechanisms']['adaptation_practices'].get(adaptation_category, 0.5)
        coping_score = (traditional_knowledge * 0.5 + adaptation_practices * 0.5)
        
        # Combine social resilience components with weights
        social_resilience = (
            awareness_score * self.social_resilience['awareness']['resilience_contribution'] +
            social_capital_score * self.social_resilience['social_capital']['resilience_contribution'] +
            education_score * self.social_resilience['education']['resilience_contribution'] +
            coping_score * self.social_resilience['coping_mechanisms']['resilience_contribution']
        )
        
        return social_resilience
        
    def _calculate_economic_resilience(self, region_type, socioeconomic_profile, hazard_type):
        """Calculate economic resilience score"""
        # Determine income and location categories
        location_category = 'urban' if 'urban' in region_type else 'rural'
        
        # Determine income category based on socioeconomic profile
        income_level = socioeconomic_profile.get('income_level', 'middle_income')
        income_category = f"{location_category}_{income_level}"
        
        # Calculate household financial resilience
        savings_rate = self.economic_resilience['household_financial']['savings_rate'].get(income_category, 0.3)
        income_diversity = self.economic_resilience['household_financial']['income_diversity'].get(income_category, 0.3)
        household_score = (savings_rate * 0.6 + income_diversity * 0.4)
        
        # Calculate business resilience
        business_size = socioeconomic_profile.get('business_size', 'small')
        business_continuity = self.economic_resilience['business_resilience']['business_continuity'].get(business_size, 0.3)
        
        business_type = socioeconomic_profile.get('business_type', 'informal')
        supply_chain = self.economic_resilience['business_resilience']['supply_chain_resilience'].get(business_type, 0.3)
        business_score = (business_continuity * 0.5 + supply_chain * 0.5)
        
        # Calculate financial protection
        insurance = self.economic_resilience['financial_protection']['insurance_coverage'].get(income_category, 0.1)
        safety_nets_coverage = self.economic_resilience['financial_protection']['social_safety_nets']['coverage']
        safety_nets_adequacy = self.economic_resilience['financial_protection']['social_safety_nets']['adequacy']
        safety_nets = (safety_nets_coverage + safety_nets_adequacy) / 2
        protection_score = (insurance * 0.5 + safety_nets * 0.5)
        
        # Calculate economic diversity
        sector_diversity = self.economic_resilience['economic_diversity']['sector_diversity']
        geo_distribution = self.economic_resilience['economic_diversity']['geographic_distribution']
        diversity_score = (sector_diversity * 0.6 + geo_distribution * 0.4)
        
        # Combine economic resilience components with weights
        economic_resilience = (
            household_score * self.economic_resilience['household_financial']['resilience_contribution'] +
            business_score * self.economic_resilience['business_resilience']['resilience_contribution'] +
            protection_score * self.economic_resilience['financial_protection']['resilience_contribution'] +
            diversity_score * self.economic_resilience['economic_diversity']['resilience_contribution']
        )
        
        return economic_resilience
        
    def _calculate_ecosystem_resilience(self, region_type, hazard_type):
        """Calculate ecosystem resilience score"""
        # Calculate forest ecosystem resilience
        mangrove_coverage = self.ecosystem_resilience['forest_ecosystems']['mangrove_coverage']
        mangrove_health = self.ecosystem_resilience['forest_ecosystems']['mangrove_health']
        forest_fragmentation = self.ecosystem_resilience['forest_ecosystems']['forest_fragmentation']
        
        # Lower fragmentation is better (reverse the scale)
        forest_connectivity = 1 - forest_fragmentation
        
        forest_score = (mangrove_coverage * 0.4 + mangrove_health * 0.4 + forest_connectivity * 0.2)
        
        # Calculate wetlands resilience
        wetland_coverage = self.ecosystem_resilience['wetlands']['wetland_coverage']
        wetland_health = self.ecosystem_resilience['wetlands']['wetland_health']
        hydrological_function = self.ecosystem_resilience['wetlands']['hydrological_function']
        
        wetland_score = (wetland_coverage * 0.3 + wetland_health * 0.3 + hydrological_function * 0.4)
        
        # Calculate agricultural ecosystem resilience
        soil_health = self.ecosystem_resilience['agricultural_ecosystems']['soil_health']
        crop_diversity = self.ecosystem_resilience['agricultural_ecosystems']['crop_diversity']
        sustainable_practices = self.ecosystem_resilience['agricultural_ecosystems']['sustainable_practices']
        
        agricultural_score = (soil_health * 0.3 + crop_diversity * 0.4 + sustainable_practices * 0.3)
        
        # Weight ecosystem components based on region type
        if 'coastal' in region_type:
            # Coastal areas benefit more from mangroves
            weights = {'forest': 0.5, 'wetland': 0.3, 'agricultural': 0.2}
        elif 'haor' in region_type or 'wetland' in region_type:
            # Wetland areas benefit more from wetland ecosystems
            weights = {'forest': 0.2, 'wetland': 0.6, 'agricultural': 0.2}
        elif 'rural' in region_type:
            # Rural areas benefit more from agricultural ecosystems
            weights = {'forest': 0.2, 'wetland': 0.3, 'agricultural': 0.5}
        else:
            # Default weight distribution
            weights = {'forest': 0.3, 'wetland': 0.3, 'agricultural': 0.4}
        
        # Combine ecosystem resilience components with region-specific weights
        ecosystem_resilience = (
            forest_score * weights['forest'] +
            wetland_score * weights['wetland'] +
            agricultural_score * weights['agricultural']
        )
        
        return ecosystem_resilience
        
    def _calculate_institutional_resilience(self, governance_quality, hazard_type):
        """Calculate institutional resilience score"""
        # Extract governance quality metrics
        policy_implementation = governance_quality.get('policy_implementation', 0.5)
        coordination = governance_quality.get('coordination', 0.5)
        corruption_level = governance_quality.get('corruption_level', 0.5)
        
        # Transform corruption level (higher value means less corruption)
        corruption_reformed = 1 - corruption_level
        
        # Calculate disaster governance score
        policy_framework = self.institutional_resilience['disaster_governance']['policy_framework']
        institutional_capacity = self.institutional_resilience['disaster_governance']['institutional_capacity']
        governance_coordination = self.institutional_resilience['disaster_governance']['coordination']
        implementation = self.institutional_resilience['disaster_governance']['implementation'] * policy_implementation
        
        governance_score = (policy_framework * 0.2 + institutional_capacity * 0.3 + 
                           governance_coordination * coordination * 0.2 + implementation * 0.3)
        
        # Calculate early warning systems score
        technical_capacity = self.institutional_resilience['early_warning_systems']['technical_capacity']
        ews_institutional = self.institutional_resilience['early_warning_systems']['institutional_capacity']
        communication = self.institutional_resilience['early_warning_systems']['communication_systems']
        community_integration = self.institutional_resilience['early_warning_systems']['community_integration']
        
        ews_score = (technical_capacity * 0.3 + ews_institutional * 0.2 + 
                    communication * 0.3 + community_integration * 0.2)
        
        # Calculate planning systems score
        hazard_mapping = self.institutional_resilience['planning_systems']['hazard_mapping']
        land_use = self.institutional_resilience['planning_systems']['land_use_planning']
        building_control = self.institutional_resilience['planning_systems']['building_control']
        planning_implementation = self.institutional_resilience['planning_systems']['implementation'] * policy_implementation
        
        planning_score = (hazard_mapping * 0.3 + land_use * 0.3 + 
                         building_control * 0.2 + planning_implementation * 0.2)
        
        # Calculate knowledge systems score
        research = self.institutional_resilience['knowledge_systems']['research_capacity']
        indigenous = self.institutional_resilience['knowledge_systems']['indigenous_knowledge']
        knowledge_integration = self.institutional_resilience['knowledge_systems']['knowledge_integration']
        
        knowledge_score = (research * 0.4 + indigenous * 0.3 + knowledge_integration * 0.3)
        
        # Combine institutional resilience components with corruption impact
        institutional_resilience = (
            governance_score * self.institutional_resilience['disaster_governance']['resilience_contribution'] +
            ews_score * self.institutional_resilience['early_warning_systems']['resilience_contribution'] +
            planning_score * self.institutional_resilience['planning_systems']['resilience_contribution'] +
            knowledge_score * self.institutional_resilience['knowledge_systems']['resilience_contribution']
        ) * corruption_reformed  # Corruption reduces all institutional effectiveness
        
        return institutional_resilience
        
    def _calculate_hazard_specific_resilience(self, hazard_type, resilience_dimensions):
        """Calculate hazard-specific resilience scores"""
        # Hazard-specific importance weights for different resilience dimensions
        hazard_weights = {
            'flood': {
                'infrastructure_resilience': 0.3,
                'social_resilience': 0.2,
                'economic_resilience': 0.15,
                'ecosystem_resilience': 0.2,
                'institutional_resilience': 0.15
            },
            'cyclone': {
                'infrastructure_resilience': 0.35,
                'social_resilience': 0.25,
                'economic_resilience': 0.1,
                'ecosystem_resilience': 0.15,
                'institutional_resilience': 0.15
            },
            'drought': {
                'infrastructure_resilience': 0.15,
                'social_resilience': 0.2,
                'economic_resilience': 0.25,
                'ecosystem_resilience': 0.25,
                'institutional_resilience': 0.15
            },
            'landslide': {
                'infrastructure_resilience': 0.3,
                'social_resilience': 0.2,
                'economic_resilience': 0.1,
                'ecosystem_resilience': 0.3,
                'institutional_resilience': 0.1
            }
        }
        
        # Default to flood weights if hazard type not specified
        if hazard_type not in hazard_weights:
            hazard_type = 'flood'
            
        # Calculate hazard-specific resilience
        hazard_resilience = sum(
            resilience_dimensions[dim] * hazard_weights[hazard_type][dim]
            for dim in hazard_weights[hazard_type]
        )
        
        return hazard_resilience
