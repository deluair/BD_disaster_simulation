"""
EmergencyResponseModel: Models disaster response operations and effectiveness
"""

class EmergencyResponseModel:
    """Model disaster response operations and effectiveness"""
    def __init__(self):
        # Initialize emergency response parameters
        self._initialize_response_capabilities()
    
    def _initialize_response_capabilities(self):
        """Initialize emergency response capabilities and resources"""
        # Response agency capacities (rating 0-1)
        self.response_agencies = {
            'disaster_management': {
                'national': 0.8,   # Department of Disaster Management (DDM)
                'division': 0.7,   # Division level disaster management committee
                'district': 0.6,   # District level disaster management committee
                'upazila': 0.5,    # Upazila level disaster management committee
                'union': 0.4       # Union level disaster management committee
            },
            'fire_service': {
                'coverage': 0.6,    # Population coverage ratio
                'equipment': 0.5,   # Equipment adequacy
                'training': 0.7,    # Personnel training level
                'response_time': {  # Average response time in minutes
                    'urban': 20,
                    'suburban': 40,
                    'rural': 90
                }
            },
            'police': {
                'coverage': 0.8,    # Population coverage ratio
                'equipment': 0.6,   # Equipment adequacy
                'training': 0.5,    # Personnel training level for disasters
                'response_time': {  # Average response time in minutes
                    'urban': 15,
                    'suburban': 30,
                    'rural': 60
                }
            },
            'medical_services': {
                'hospital_beds_per_1000': 0.8,  # National average
                'doctors_per_1000': 0.6,        # National average
                'ambulances_per_100000': 1.2,   # National average
                'emergency_capacity': 0.4,      # Surge capacity for emergencies
                'distribution': {               # Geographical distribution
                    'urban': 0.8,
                    'suburban': 0.4,
                    'rural': 0.2
                }
            },
            'military': {
                'personnel_available': 30000,   # Number available for disaster response
                'helicopter_count': 25,         # For air operations
                'boat_count': 300,              # For water operations
                'mobilization_time_hours': 24,  # Average time to mobilize
                'equipment': 0.8,               # Equipment adequacy
                'training': 0.9                 # Personnel training level
            },
            'ngos': {
                'national_coverage': 0.7,      # Population coverage ratio
                'international_presence': 0.6,  # International NGO presence
                'coordination': 0.5,           # Coordination effectiveness
                'resources': 0.6,              # Resource adequacy
                'regional_capacity': {         # Regional capacity variations
                    'coastal': 0.8,
                    'urban': 0.7,
                    'flood_plain': 0.6,
                    'haor_basin': 0.5,
                    'hill_tracts': 0.4
                }
            }
        }
        
        # Emergency resources by type
        self.emergency_resources = {
            'evacuation_shelters': {
                'cyclone_shelters': 2500,     # Number of dedicated cyclone shelters
                'flood_shelters': 1500,       # Number of dedicated flood shelters
                'multipurpose_shelters': 3000, # Schools, community centers, etc.
                'capacity_persons': 2500000,   # Total capacity
                'capacity_adequacy': 0.6,      # Adequacy for population needs
                'accessibility': 0.5,          # Average accessibility score
                'condition': 0.7               # Physical condition/readiness
            },
            'relief_supplies': {
                'food_days': 1000000,        # Person-days of food supplies
                'water_liters': 5000000,     # Liters of emergency water
                'medical_kits': 50000,       # Emergency medical kits
                'tents': 20000,              # Emergency shelter tents
                'blankets': 200000,          # Emergency blankets
                'hygiene_kits': 100000,      # Hygiene kits
                'distribution_capacity': 0.5  # Capacity to distribute per day
            },
            'equipment': {
                'rescue_boats': 500,          # Small rescue boats
                'high_water_vehicles': 100,   # Vehicles for flood water
                'ambulances': 800,            # Emergency ambulances
                'fire_trucks': 300,           # Fire and rescue trucks
                'earth_movers': 200,          # Bulldozers, excavators
                'water_pumps': 1000,          # Water removal pumps
                'emergency_generators': 500   # Backup power generators
            },
            'telecommunications': {
                'emergency_radio_sets': 5000,   # Emergency communication devices
                'satellite_phones': 500,        # For areas without cell coverage
                'emergency_network_coverage': 0.6,  # Coverage during emergencies
                'early_warning_systems': 0.7     # Functionality of warning systems
            }
        }
        
        # Disaster-specific response effectiveness factors
        self.response_effectiveness = {
            'flood': {
                'rescue': 0.7,          # Rescue effectiveness
                'evacuation': 0.6,       # Evacuation effectiveness
                'relief': 0.6,           # Relief distribution effectiveness
                'medical': 0.5,          # Medical response effectiveness
                'restoration': 0.5       # Service restoration effectiveness
            },
            'cyclone': {
                'rescue': 0.6,          # Rescue effectiveness
                'evacuation': 0.7,       # Evacuation effectiveness
                'relief': 0.6,           # Relief distribution effectiveness
                'medical': 0.5,          # Medical response effectiveness
                'restoration': 0.4       # Service restoration effectiveness
            },
            'flash_flood': {
                'rescue': 0.5,          # Rescue effectiveness
                'evacuation': 0.4,       # Evacuation effectiveness (low due to short lead time)
                'relief': 0.5,           # Relief distribution effectiveness
                'medical': 0.5,          # Medical response effectiveness
                'restoration': 0.6       # Service restoration effectiveness
            },
            'landslide': {
                'rescue': 0.4,          # Rescue effectiveness (challenging terrain)
                'evacuation': 0.3,       # Evacuation effectiveness (challenging terrain)
                'relief': 0.4,           # Relief distribution effectiveness
                'medical': 0.4,          # Medical response effectiveness
                'restoration': 0.5       # Service restoration effectiveness
            },
            'earthquake': {
                'rescue': 0.3,          # Rescue effectiveness (limited experience)
                'evacuation': 0.4,       # Evacuation effectiveness
                'relief': 0.5,           # Relief distribution effectiveness
                'medical': 0.4,          # Medical response effectiveness
                'restoration': 0.3       # Service restoration effectiveness
            },
            'drought': {
                'rescue': 0.8,          # Rescue effectiveness (less acute need)
                'evacuation': 0.7,       # Evacuation effectiveness (longer lead time)
                'relief': 0.6,           # Relief distribution effectiveness
                'medical': 0.6,          # Medical response effectiveness
                'restoration': 0.4       # Service restoration effectiveness
            }
        }
        
        # Coordination effectiveness parameters
        self.coordination_effectiveness = {
            'inter_agency': 0.6,        # Between government agencies
            'govt_ngo': 0.5,            # Between government and NGOs
            'national_local': 0.5,      # Between national and local authorities
            'civil_military': 0.7,      # Between civilian and military resources
            'international': 0.6        # With international responders
        }
        
        # Logistics parameters
        self.logistics_parameters = {
            'transportation_disruption': {  # Scaling factors for transport disruption
                'flood': 0.7,              # High disruption
                'cyclone': 0.6,
                'earthquake': 0.8,          # Very high disruption
                'landslide': 0.7,
                'drought': 0.2              # Low disruption
            },
            'supply_chain_resilience': 0.5,  # Overall supply chain resilience
            'last_mile_delivery': 0.4,      # Last mile delivery capability
            'prepositioning': 0.6,          # Level of resource prepositioning
            'distribution_points': {         # Distribution point density
                'urban': 0.8,
                'suburban': 0.5,
                'rural': 0.3
            }
        }
    
    def simulate_response(self, disaster_impacts, available_resources):
        """Simulate emergency response operations and their effectiveness
        
        Args:
            disaster_impacts: Dictionary of disaster impacts from VulnerabilityModel
            available_resources: Dictionary of resources available for response
            
        Returns:
            Dictionary with response results and effectiveness metrics
        """
        # Extract key disaster information
        hazard_type = disaster_impacts.get('hazard_type', 'flood')
        region_type = disaster_impacts.get('region_type', 'generic')
        affected_population = disaster_impacts.get('casualties', {}).get('affected', 0)
        if affected_population == 0:
            # Estimate affected from displaced + injured + deaths
            affected_population = sum(disaster_impacts.get('casualties', {}).values())
        
        # Get base response effectiveness for this hazard type
        if hazard_type in self.response_effectiveness:
            base_effectiveness = self.response_effectiveness[hazard_type]
        else:
            # Default to flood response if hazard type not found
            base_effectiveness = self.response_effectiveness['flood']
        
        # Calculate logistics constraints based on transportation disruption
        transport_disruption = self.logistics_parameters['transportation_disruption'].get(
            hazard_type, 0.5)
        
        # Adjust for regional capacity differences
        if region_type == 'coastal':
            regional_factor = self.response_agencies['ngos']['regional_capacity']['coastal']
        elif region_type == 'riverine':
            regional_factor = self.response_agencies['ngos']['regional_capacity']['flood_plain']
        elif region_type == 'urban':
            regional_factor = self.response_agencies['ngos']['regional_capacity']['urban']
        elif region_type == 'haor':
            regional_factor = self.response_agencies['ngos']['regional_capacity']['haor_basin']
        elif region_type == 'hill_tracts':
            regional_factor = self.response_agencies['ngos']['regional_capacity']['hill_tracts']
        else:
            # Default regional factor
            regional_factor = 0.6
        
        # Calculate overall coordination effectiveness
        coordination = (
            self.coordination_effectiveness['inter_agency'] * 0.2 +
            self.coordination_effectiveness['govt_ngo'] * 0.2 +
            self.coordination_effectiveness['national_local'] * 0.2 +
            self.coordination_effectiveness['civil_military'] * 0.2 +
            self.coordination_effectiveness['international'] * 0.2
        )
        
        # Adjust response effectiveness based on available resources
        resource_adequacy = self._calculate_resource_adequacy(affected_population, available_resources)
        
        # Calculate overall response effectiveness for different operations
        response_results = {}
        for operation, base_value in base_effectiveness.items():
            # Adjust effectiveness based on multiple factors
            adjusted_effectiveness = base_value * (
                0.4 +  # Base weight
                0.2 * regional_factor +  # Regional capacity
                0.2 * resource_adequacy[operation] +  # Resource adequacy
                0.1 * coordination +  # Coordination effectiveness
                0.1 * (1 - transport_disruption)  # Transport conditions (inverse of disruption)
            )
            
            # Bound between 0.05 and 0.95
            adjusted_effectiveness = min(0.95, max(0.05, adjusted_effectiveness))
            response_results[operation] = adjusted_effectiveness
        
        # Calculate response gaps
        response_gaps = {}
        for operation, effectiveness in response_results.items():
            response_gaps[operation] = max(0, 1.0 - effectiveness)
        
        # Calculate resource consumption
        resource_consumption = self._calculate_resource_consumption(
            affected_population, available_resources, response_results)
        
        # Calculate lives saved through response operations
        potential_fatalities = disaster_impacts.get('casualties', {}).get('deaths', 0)
        additional_lives_saved = int(potential_fatalities * response_results.get('rescue', 0.5) * 0.3)
        
        # Calculate shelter needs and provision
        displaced_population = disaster_impacts.get('casualties', {}).get('displaced', 0)
        shelter_capacity = available_resources.get('shelter_capacity', 
                                                 self.emergency_resources['evacuation_shelters']['capacity_persons'])
        shelter_access_ratio = min(1.0, shelter_capacity / max(1, displaced_population))
        
        # Calculate relief provision effectiveness
        relief_needs_days = affected_population * 7  # 7 days of relief needed per person
        available_relief_days = available_resources.get('relief_days', 
                                                      self.emergency_resources['relief_supplies']['food_days'])
        relief_provision_ratio = min(1.0, available_relief_days / max(1, relief_needs_days))
        
        # Calculate medical service provision
        injured_population = disaster_impacts.get('casualties', {}).get('injuries', 0)
        medical_capacity = available_resources.get('medical_capacity', 
                                                 int(affected_population * 0.05))  # Default 5% capacity
        medical_service_ratio = min(1.0, medical_capacity / max(1, injured_population))
        
        # Return comprehensive response results
        return {
            'response_effectiveness': response_results,
            'response_gaps': response_gaps,
            'coordination_effectiveness': coordination,
            'transport_disruption': transport_disruption,
            'resource_adequacy': resource_adequacy,
            'resource_consumption': resource_consumption,
            'additional_lives_saved': additional_lives_saved,
            'shelter_access_ratio': shelter_access_ratio,
            'relief_provision_ratio': relief_provision_ratio,
            'medical_service_ratio': medical_service_ratio,
            'overall_response_score': sum(response_results.values()) / len(response_results)
        }
    
    def _calculate_resource_adequacy(self, affected_population, available_resources):
        """Calculate resource adequacy for different response operations"""
        # Default resource adequacy if no specifics provided
        default_adequacy = 0.6
        
        # Calculate adequacy for each operation type
        rescue_adequacy = available_resources.get('rescue_adequacy', default_adequacy)
        evacuation_adequacy = available_resources.get('evacuation_adequacy', default_adequacy)
        relief_adequacy = available_resources.get('relief_adequacy', default_adequacy)
        medical_adequacy = available_resources.get('medical_adequacy', default_adequacy)
        restoration_adequacy = available_resources.get('restoration_adequacy', default_adequacy)
        
        return {
            'rescue': rescue_adequacy,
            'evacuation': evacuation_adequacy,
            'relief': relief_adequacy,
            'medical': medical_adequacy,
            'restoration': restoration_adequacy
        }
    
    def _calculate_resource_consumption(self, affected_population, available_resources, response_results):
        """Calculate resources consumed during response operations"""
        # Simplified consumption based on affected population and response effectiveness
        relief_effectiveness = response_results.get('relief', 0.5)
        medical_effectiveness = response_results.get('medical', 0.5)
        
        # Calculate daily consumption
        daily_food_consumed = int(affected_population * relief_effectiveness * 1.0)  # 1 person-day per person
        daily_water_consumed = int(affected_population * relief_effectiveness * 3.0)  # 3 liters per person
        medical_kits_consumed = int(affected_population * medical_effectiveness * 0.05)  # 5% need medical kits
        
        return {
            'daily_food_person_days': daily_food_consumed,
            'daily_water_liters': daily_water_consumed,
            'medical_kits': medical_kits_consumed,
            'shelter_capacity_used': int(affected_population * response_results.get('evacuation', 0.5) * 0.7)
        }
