"""
SocioeconomicModel: Models socioeconomic factors affecting disaster vulnerability
"""

import numpy as np
from collections import defaultdict

class SocioeconomicModel:
    """Model socioeconomic factors affecting disaster vulnerability in Bangladesh"""
    def __init__(self):
        # Initialize socioeconomic parameters
        self._initialize_socioeconomic_parameters()
        
    def _initialize_socioeconomic_parameters(self):
        """Initialize parameters for socioeconomic modeling"""
        # Demographic factors
        self.demographics = {
            'population_density': {
                'dhaka_division': 1500,  # persons per sq km
                'chittagong_division': 900,
                'khulna_division': 600,
                'rajshahi_division': 1000,
                'barisal_division': 650,
                'sylhet_division': 550,
                'rangpur_division': 800,
                'mymensingh_division': 1000,
                'national_average': 1100,
                'annual_growth_rate': 0.01  # 1% annual growth
            },
            'age_structure': {
                'children_0_14': 0.27,  # 27% of population
                'working_age_15_64': 0.67,  # 67% of population
                'elderly_65_plus': 0.06,  # 6% of population
                'dependency_ratio': 0.48  # Ratio of dependent to working population
            },
            'urbanization': {
                'urban_population_share': 0.38,  # 38% urban
                'urban_growth_rate': 0.035,  # 3.5% annual growth
                'slum_population_share': 0.40,  # 40% of urban population in slums
                'planned_settlement_share': 0.25  # 25% in planned settlements
            },
            'gender': {
                'gender_ratio': 0.98,  # Males per female
                'female_headed_households': 0.14  # 14% of households
            },
            'migration': {
                'rural_to_urban': 0.02,  # Annual rate
                'climate_displaced': 0.005,  # Annual rate
                'international_outmigration': 0.003  # Annual rate
            }
        }
        
        # Economic factors
        self.economic = {
            'income_distribution': {
                'below_poverty_line': 0.20,  # 20% below poverty line
                'extreme_poverty': 0.10,  # 10% in extreme poverty
                'low_income': 0.40,  # 40% low income
                'middle_income': 0.30,  # 30% middle income
                'high_income': 0.10,  # 10% high income
                'gini_coefficient': 0.32  # Inequality measure
            },
            'employment': {
                'unemployment_rate': 0.05,  # 5% unemployment
                'underemployment_rate': 0.25,  # 25% underemployment
                'informal_sector_share': 0.85,  # 85% in informal sector
                'agricultural_employment': 0.40,  # 40% in agriculture
                'industrial_employment': 0.20,  # 20% in industry
                'service_employment': 0.40  # 40% in services
            },
            'economic_growth': {
                'gdp_growth_rate': 0.065,  # 6.5% annual growth
                'agricultural_growth': 0.035,  # 3.5% growth
                'industrial_growth': 0.08,  # 8% growth
                'service_growth': 0.065  # 6.5% growth
            },
            'remittances': {
                'gdp_share': 0.06,  # 6% of GDP
                'household_dependency': 0.12  # 12% of households highly dependent
            }
        }
        
        # Social infrastructure
        self.social_infrastructure = {
            'education': {
                'literacy_rate': 0.74,  # 74% literacy
                'primary_enrollment': 0.98,  # 98% enrollment
                'secondary_enrollment': 0.67,  # 67% enrollment
                'tertiary_enrollment': 0.18,  # 18% enrollment
                'gender_parity_index': 1.06  # Ratio of female to male enrollment
            },
            'healthcare': {
                'physicians_per_1000': 0.5,  # 0.5 per 1000 people
                'hospital_beds_per_1000': 0.8,  # 0.8 per 1000 people
                'access_to_healthcare': 0.65,  # 65% with reasonable access
                'health_insurance_coverage': 0.03  # 3% with insurance
            },
            'social_protection': {
                'coverage_rate': 0.35,  # 35% covered by some program
                'adequacy': 0.40,  # 40% adequacy of benefits
                'targeting_efficiency': 0.6  # 60% targeting efficiency
            },
            'social_cohesion': {
                'community_organizations': 0.60,  # 60% of communities with organizations
                'religious_institutions': 0.95,  # 95% coverage
                'trust_index': 0.55  # Social trust level
            }
        }
        
        # Vulnerability factors
        self.vulnerability_factors = {
            'housing': {
                'permanent_housing': 0.30,  # 30% in permanent housing
                'semi_permanent': 0.45,  # 45% in semi-permanent
                'temporary_housing': 0.25,  # 25% in temporary/kutcha
                'homeless': 0.003,  # 0.3% homeless
                'disaster_resistant_housing': 0.15  # 15% disaster resistant
            },
            'basic_services': {
                'improved_water_access': 0.87,  # 87% access
                'improved_sanitation': 0.61,  # 61% access
                'electricity_access': 0.85,  # 85% access
                'solid_waste_disposal': 0.55  # 55% access
            },
            'asset_ownership': {
                'land_ownership': 0.65,  # 65% own some land
                'livestock_ownership': 0.45,  # 45% own livestock
                'savings_access': 0.40,  # 40% have savings
                'financial_inclusion': 0.50  # 50% have bank accounts
            },
            'livelihoods': {
                'livelihood_diversity': 0.35,  # 35% have diverse livelihoods
                'climate_sensitive_livelihoods': 0.65,  # 65% in climate-sensitive sectors
                'livelihood_resilience': 0.30  # 30% with resilient livelihoods
            }
        }
        
        # Regional socioeconomic profiles
        self.regional_profiles = {
            'urban_megacity': {
                'poverty_rate': 0.15,
                'informal_settlement': 0.40,
                'service_access': 0.80,
                'employment_stability': 0.60,
                'social_protection': 0.45,
                'education_level': 0.75,
                'health_access': 0.70,
                'vulnerability_index': 0.40  # Lower is better
            },
            'urban_secondary': {
                'poverty_rate': 0.22,
                'informal_settlement': 0.35,
                'service_access': 0.70,
                'employment_stability': 0.55,
                'social_protection': 0.40,
                'education_level': 0.70,
                'health_access': 0.65,
                'vulnerability_index': 0.45
            },
            'coastal_rural': {
                'poverty_rate': 0.30,
                'informal_settlement': 0.25,
                'service_access': 0.50,
                'employment_stability': 0.40,
                'social_protection': 0.35,
                'education_level': 0.60,
                'health_access': 0.50,
                'vulnerability_index': 0.65
            },
            'floodplain_rural': {
                'poverty_rate': 0.28,
                'informal_settlement': 0.15,
                'service_access': 0.55,
                'employment_stability': 0.45,
                'social_protection': 0.30,
                'education_level': 0.65,
                'health_access': 0.55,
                'vulnerability_index': 0.60
            },
            'char_lands': {
                'poverty_rate': 0.40,
                'informal_settlement': 0.30,
                'service_access': 0.40,
                'employment_stability': 0.30,
                'social_protection': 0.25,
                'education_level': 0.50,
                'health_access': 0.40,
                'vulnerability_index': 0.75
            },
            'haor_region': {
                'poverty_rate': 0.35,
                'informal_settlement': 0.20,
                'service_access': 0.45,
                'employment_stability': 0.35,
                'social_protection': 0.30,
                'education_level': 0.55,
                'health_access': 0.45,
                'vulnerability_index': 0.70
            },
            'hill_tracts': {
                'poverty_rate': 0.33,
                'informal_settlement': 0.15,
                'service_access': 0.40,
                'employment_stability': 0.35,
                'social_protection': 0.25,
                'education_level': 0.50,
                'health_access': 0.35,
                'vulnerability_index': 0.68
            },
            'barind_tract': {
                'poverty_rate': 0.30,
                'informal_settlement': 0.15,
                'service_access': 0.50,
                'employment_stability': 0.40,
                'social_protection': 0.30,
                'education_level': 0.60,
                'health_access': 0.50,
                'vulnerability_index': 0.62
            }
        }
        
        # Socioeconomic trends
        self.socioeconomic_trends = {
            'poverty_reduction': -0.01,  # Annual rate of reduction
            'urbanization_increase': 0.01,  # Annual rate of increase
            'education_improvement': 0.01,  # Annual rate of improvement
            'health_improvement': 0.01,  # Annual rate of improvement
            'infrastructure_improvement': 0.015,  # Annual rate of improvement
            'income_inequality_change': 0.002  # Annual rate of increase
        }
        
        # Social vulnerability by hazard type
        self.hazard_vulnerability = {
            'flood': {
                'urban_megacity': 0.6,  # Vulnerability score
                'urban_secondary': 0.65,
                'coastal_rural': 0.7,
                'floodplain_rural': 0.8,
                'char_lands': 0.9,
                'haor_region': 0.85,
                'hill_tracts': 0.5,
                'barind_tract': 0.4
            },
            'cyclone': {
                'urban_megacity': 0.65,
                'urban_secondary': 0.7,
                'coastal_rural': 0.9,
                'floodplain_rural': 0.6,
                'char_lands': 0.8,
                'haor_region': 0.5,
                'hill_tracts': 0.4,
                'barind_tract': 0.3
            },
            'riverbank_erosion': {
                'urban_megacity': 0.3,
                'urban_secondary': 0.4,
                'coastal_rural': 0.6,
                'floodplain_rural': 0.7,
                'char_lands': 0.9,
                'haor_region': 0.6,
                'hill_tracts': 0.3,
                'barind_tract': 0.3
            },
            'drought': {
                'urban_megacity': 0.4,
                'urban_secondary': 0.5,
                'coastal_rural': 0.6,
                'floodplain_rural': 0.7,
                'char_lands': 0.8,
                'haor_region': 0.5,
                'hill_tracts': 0.6,
                'barind_tract': 0.9
            },
            'landslide': {
                'urban_megacity': 0.5,
                'urban_secondary': 0.5,
                'coastal_rural': 0.3,
                'floodplain_rural': 0.2,
                'char_lands': 0.1,
                'haor_region': 0.2,
                'hill_tracts': 0.9,
                'barind_tract': 0.5
            }
        }

    def simulate_socioeconomic_vulnerability(self, region_type, time_period, hazard_type):
        """Simulate socioeconomic vulnerability for a specific context
        
        Args:
            region_type: Type of region (urban megacity, coastal rural, etc.)
            time_period: Years from baseline (2025)
            hazard_type: Type of hazard being considered
            
        Returns:
            Dictionary with socioeconomic vulnerability metrics
        """
        # Get baseline regional profile
        if region_type in self.regional_profiles:
            baseline_profile = self.regional_profiles[region_type]
        else:
            # Default to floodplain rural if region type not found
            baseline_profile = self.regional_profiles['floodplain_rural']
            
        # Apply time trends to vulnerability factors
        evolved_profile = self._apply_time_evolution(baseline_profile, time_period)
        
        # Get hazard-specific vulnerability
        if hazard_type in self.hazard_vulnerability and region_type in self.hazard_vulnerability[hazard_type]:
            hazard_vulnerability = self.hazard_vulnerability[hazard_type][region_type]
        else:
            # Default vulnerability if hazard or region not found
            hazard_vulnerability = 0.6
            
        # Apply time evolution to hazard vulnerability
        # Assume vulnerability decreases with time due to adaptation and development
        hazard_vulnerability *= max(0.5, 1 - 0.01 * time_period)
        
        # Calculate vulnerability components
        economic_vulnerability = self._calculate_economic_vulnerability(evolved_profile)
        social_vulnerability = self._calculate_social_vulnerability(evolved_profile)
        physical_vulnerability = self._calculate_physical_vulnerability(evolved_profile)
        livelihood_vulnerability = self._calculate_livelihood_vulnerability(evolved_profile, hazard_type)
        
        # Calculate overall vulnerability (weighted average)
        overall_vulnerability = (
            economic_vulnerability * 0.25 +
            social_vulnerability * 0.25 +
            physical_vulnerability * 0.25 +
            livelihood_vulnerability * 0.25
        )
        
        # Apply hazard-specific adjustment
        hazard_adjusted_vulnerability = overall_vulnerability * hazard_vulnerability
        
        # Calculate coping capacity (inverse of vulnerability factors and positively correlated with development)
        coping_capacity = 1 - (
            overall_vulnerability * 0.7 +
            (1 - (evolved_profile['education_level'] + evolved_profile['health_access'] + 
                 evolved_profile['social_protection'] + evolved_profile['employment_stability']) / 4) * 0.3
        )
        
        # Calculate adaptive capacity (longer-term ability to adjust to changing conditions)
        adaptive_capacity = (
            evolved_profile['education_level'] * 0.3 +
            evolved_profile['employment_stability'] * 0.2 +
            evolved_profile['social_protection'] * 0.2 +
            (1 - evolved_profile['poverty_rate']) * 0.3
        )
        
        # Calculate socioeconomic resilience (combines coping and adaptive capacity)
        socioeconomic_resilience = (coping_capacity * 0.4 + adaptive_capacity * 0.6)
        
        # Calculate final vulnerability score (vulnerability reduced by resilience)
        final_vulnerability = hazard_adjusted_vulnerability * (1 - socioeconomic_resilience * 0.5)
        
        # Prepare detailed results
        vulnerability_results = {
            'economic_vulnerability': economic_vulnerability,
            'social_vulnerability': social_vulnerability,
            'physical_vulnerability': physical_vulnerability,
            'livelihood_vulnerability': livelihood_vulnerability,
            'overall_vulnerability': overall_vulnerability,
            'hazard_specific_vulnerability': hazard_vulnerability,
            'hazard_adjusted_vulnerability': hazard_adjusted_vulnerability,
            'coping_capacity': coping_capacity,
            'adaptive_capacity': adaptive_capacity,
            'socioeconomic_resilience': socioeconomic_resilience,
            'final_vulnerability_score': final_vulnerability,
            'evolved_profile': evolved_profile
        }
        
        return vulnerability_results
        
    def _apply_time_evolution(self, baseline_profile, time_period):
        """Apply time evolution to the baseline profile"""
        evolved_profile = dict(baseline_profile)
        
        # Apply trend rates over time
        evolved_profile['poverty_rate'] = max(
            0.05,  # Minimum poverty rate
            baseline_profile['poverty_rate'] + self.socioeconomic_trends['poverty_reduction'] * time_period
        )
        
        evolved_profile['informal_settlement'] = max(
            0.05,  # Minimum informal settlement rate
            baseline_profile['informal_settlement'] + 
            (self.socioeconomic_trends['infrastructure_improvement'] * -0.5) * time_period
        )
        
        evolved_profile['service_access'] = min(
            0.98,  # Maximum service access
            baseline_profile['service_access'] + 
            self.socioeconomic_trends['infrastructure_improvement'] * time_period
        )
        
        evolved_profile['employment_stability'] = min(
            0.9,  # Maximum employment stability
            baseline_profile['employment_stability'] + 0.005 * time_period
        )
        
        evolved_profile['social_protection'] = min(
            0.8,  # Maximum social protection
            baseline_profile['social_protection'] + 0.007 * time_period
        )
        
        evolved_profile['education_level'] = min(
            0.95,  # Maximum education level
            baseline_profile['education_level'] + 
            self.socioeconomic_trends['education_improvement'] * time_period
        )
        
        evolved_profile['health_access'] = min(
            0.95,  # Maximum health access
            baseline_profile['health_access'] + 
            self.socioeconomic_trends['health_improvement'] * time_period
        )
        
        # Vulnerability index improves with development
        evolved_profile['vulnerability_index'] = max(
            0.2,  # Minimum vulnerability index
            baseline_profile['vulnerability_index'] - 0.008 * time_period
        )
        
        return evolved_profile
        
    def _calculate_economic_vulnerability(self, profile):
        """Calculate economic vulnerability based on profile"""
        # Economic vulnerability is influenced by poverty, employment stability, and service access
        economic_vulnerability = (
            profile['poverty_rate'] * 0.5 +
            (1 - profile['employment_stability']) * 0.3 +
            (1 - profile['service_access']) * 0.2
        )
        
        return economic_vulnerability
        
    def _calculate_social_vulnerability(self, profile):
        """Calculate social vulnerability based on profile"""
        # Social vulnerability is influenced by education, health access, social protection
        social_vulnerability = (
            (1 - profile['education_level']) * 0.4 +
            (1 - profile['health_access']) * 0.4 +
            (1 - profile['social_protection']) * 0.2
        )
        
        return social_vulnerability
        
    def _calculate_physical_vulnerability(self, profile):
        """Calculate physical vulnerability based on profile"""
        # Physical vulnerability is influenced by informal settlement and service access
        physical_vulnerability = (
            profile['informal_settlement'] * 0.6 +
            (1 - profile['service_access']) * 0.4
        )
        
        return physical_vulnerability
        
    def _calculate_livelihood_vulnerability(self, profile, hazard_type):
        """Calculate livelihood vulnerability based on profile and hazard"""
        # Base livelihood vulnerability from employment stability and poverty
        base_vulnerability = (
            (1 - profile['employment_stability']) * 0.5 +
            profile['poverty_rate'] * 0.5
        )
        
        # Hazard-specific adjustments
        if hazard_type == 'flood' or hazard_type == 'cyclone':
            # More severe impact on rural coastal and char areas
            if 'coastal' in profile or 'char' in profile:
                hazard_multiplier = 1.2
            else:
                hazard_multiplier = 1.0
        elif hazard_type == 'drought':
            # More severe impact on agricultural regions
            if 'rural' in profile or 'barind' in profile:
                hazard_multiplier = 1.3
            else:
                hazard_multiplier = 0.9
        else:
            hazard_multiplier = 1.0
            
        return base_vulnerability * hazard_multiplier
        
    def generate_population_data(self, region_type, division, population_size):
        """Generate synthetic population data for simulation
        
        Args:
            region_type: Type of region (urban megacity, coastal rural, etc.)
            division: Administrative division
            population_size: Size of population to generate
            
        Returns:
            Dictionary with population characteristics
        """
        # Get regional profile
        if region_type in self.regional_profiles:
            profile = self.regional_profiles[region_type]
        else:
            profile = self.regional_profiles['floodplain_rural']
            
        # Population distribution
        population_data = {
            'below_poverty_line': int(profile['poverty_rate'] * population_size),
            'informal_housing': int(profile['informal_settlement'] * population_size),
            'education_levels': {
                'no_education': int((1 - profile['education_level']) * 0.4 * population_size),
                'primary': int((1 - profile['education_level']) * 0.3 * population_size + 
                              profile['education_level'] * 0.2 * population_size),
                'secondary': int(profile['education_level'] * 0.5 * population_size),
                'tertiary': int(profile['education_level'] * 0.3 * population_size)
            },
            'employment': {
                'unemployed': int((1 - profile['employment_stability']) * 0.3 * population_size),
                'informal': int((1 - profile['employment_stability']) * 0.4 * population_size + 
                               profile['employment_stability'] * 0.3 * population_size),
                'formal': int(profile['employment_stability'] * 0.7 * population_size)
            },
            'social_protection_access': int(profile['social_protection'] * population_size),
            'healthcare_access': int(profile['health_access'] * population_size)
        }
        
        # Age distribution
        population_data['age_distribution'] = {
            'children_0_14': int(self.demographics['age_structure']['children_0_14'] * population_size),
            'working_age_15_64': int(self.demographics['age_structure']['working_age_15_64'] * population_size),
            'elderly_65_plus': int(self.demographics['age_structure']['elderly_65_plus'] * population_size)
        }
        
        # Gender distribution
        gender_ratio = self.demographics['gender']['gender_ratio']
        male_population = int((gender_ratio / (1 + gender_ratio)) * population_size)
        female_population = population_size - male_population
        
        population_data['gender_distribution'] = {
            'male': male_population,
            'female': female_population
        }
        
        return population_data
