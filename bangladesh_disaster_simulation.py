import geopandas as gpd
import networkx as nx
import numpy as np
import scipy.stats as stats
import torch
import mesa
import folium
import plotly.express as px

class HazardModel:
    """Model individual disaster hazards with specific characteristics"""
    def __init__(self, hazard_type, return_periods, intensity_scales,
                 spatial_patterns, seasonal_profile, climate_sensitivity):
        # Initialize hazard-specific parameters
        self.hazard_type = hazard_type
        self.return_periods = return_periods
        self.intensity_scales = intensity_scales
        self.spatial_patterns = spatial_patterns
        self.seasonal_profile = seasonal_profile
        self.climate_sensitivity = climate_sensitivity
        
        # Hazard-specific model configurations
        self.configs = {
            'flood': {
                'monsoon_timing': {'start_month': 6, 'end_month': 9},
                'flash_flood_regions': ['haor_basins', 'northeastern_hills'],
                'river_systems': ['brahmaputra_jamuna', 'ganges_padma', 'meghna'],
                'urban_drainage_efficiency': 0.6,  # efficiency factor for urban drainage
                'polder_drainage_capacity': 30  # mm/day drainage capacity
            },
            'cyclone': {
                'bay_genesis_probability': {
                    # Monthly cyclogenesis probability distribution
                    1: 0.02, 2: 0.03, 3: 0.07, 4: 0.09, 5: 0.14, 
                    6: 0.05, 7: 0.01, 8: 0.01, 9: 0.03, 10: 0.10,
                    11: 0.12, 12: 0.04
                },
                'surge_amplification_factor': 1.2,  # amplification due to coastal bathymetry
                'wind_decay_rate': 0.15,  # inland decay rate per km
                'track_probability': {
                    'west': 0.40,  # probability of westward track
                    'northwest': 0.35,  # probability of northwestward track
                    'north': 0.25  # probability of northward track
                }
            },
            'geophysical': {
                'fault_systems': {
                    'dauki': {'slip_rate': 2.3, 'max_magnitude': 7.8},
                    'madhupur': {'slip_rate': 0.8, 'max_magnitude': 6.5}
                },
                'liquefaction_susceptibility': {
                    'very_high': ['delta_sediments', 'coastal_lowlands'],
                    'high': ['river_floodplains', 'reclaimed_areas'],
                    'moderate': ['alluvial_fans', 'piedmont_areas'],
                    'low': ['tertiary_hills', 'uplifted_terraces']
                },
                'landslide_thresholds': {
                    'chittagong_hills': {'rainfall_24hr': 200, 'slope_threshold': 25}
                },
                'erosion_rates': {
                    'jamuna': 70,  # meters/year max
                    'padma': 45,   # meters/year max
                    'meghna': 30   # meters/year max
                }
            }
        }
        
    def generate_events(self, year, climate_effects=None):
        """Generate hazard events based on return periods and seasonal patterns
        
        Args:
            year: Simulation year
            climate_effects: Climate change effects to apply
            
        Returns:
            List of hazard events with characteristics
        """
        events = []
        
        # Apply climate effects if provided
        intensity_multiplier = 1.0
        frequency_multiplier = 1.0
        if climate_effects:
            intensity_multiplier += climate_effects.get('intensity_change', 0)
            frequency_multiplier += climate_effects.get('frequency_change', 0)
        
        # Generate events based on return periods and random sampling
        for return_period in self.return_periods:
            # Annual exceedance probability = 1/return_period
            annual_prob = 1.0 / return_period * frequency_multiplier
            
            # Simulate occurrence based on probability
            if stats.uniform.rvs() < annual_prob:
                # Sample month based on seasonal profile
                month = self._sample_month_from_profile()
                
                # Generate intensity based on return period
                base_intensity = self._intensity_from_return_period(return_period)
                adjusted_intensity = base_intensity * intensity_multiplier
                
                # Create event with spatial footprint
                event = {
                    'type': self.hazard_type,
                    'year': year,
                    'month': month,
                    'return_period': return_period,
                    'intensity': adjusted_intensity,
                    'spatial_footprint': self._generate_spatial_footprint(adjusted_intensity)
                }
                
                # Add hazard-specific attributes
                self._add_hazard_specific_attributes(event)
                
                events.append(event)
        
        return events
    
    def _sample_month_from_profile(self):
        """Sample a month based on the seasonal profile"""
        if self.hazard_type == 'flood':
            if self.seasonal_profile == 'monsoon':
                # Higher probability during monsoon months (June-September)
                probabilities = [0.01, 0.01, 0.02, 0.05, 0.10, 0.20, 0.25, 0.20, 0.10, 0.04, 0.01, 0.01]
            else:
                # Uniform distribution for other flood types
                probabilities = [1/12] * 12
        elif self.hazard_type == 'cyclone':
            # Bi-modal distribution with peaks in pre and post monsoon
            probabilities = [0.02, 0.03, 0.07, 0.09, 0.14, 0.05, 0.01, 0.01, 0.03, 0.10, 0.12, 0.04]
        else:
            # Default uniform distribution
            probabilities = [1/12] * 12
            
        # Sample month (1-12) based on probabilities
        return stats.rv_discrete(values=(range(1, 13), probabilities)).rvs()
    
    def _intensity_from_return_period(self, return_period):
        """Calculate hazard intensity based on return period"""
        # Use logarithmic relationship between return period and intensity
        # I = a * ln(RP) + b where a,b are hazard-specific
        if self.hazard_type == 'flood':
            a, b = 0.8, 1.0  # Coefficients for flood depth
            return a * np.log(return_period) + b
        elif self.hazard_type == 'cyclone':
            a, b = 15, 120  # Coefficients for wind speed
            return a * np.log(return_period) + b
        else:
            # Default relationship
            a, b = 0.5, 1.0
            return a * np.log(return_period) + b
    
    def _generate_spatial_footprint(self, intensity):
        """Generate spatial footprint for the hazard event"""
        # Placeholder for spatial footprint generation
        # In a full implementation, this would generate a GeoDataFrame or raster
        if self.spatial_patterns == 'riverine':
            return {'type': 'riverine', 'affected_rivers': ['brahmaputra', 'ganges', 'meghna']}
        elif self.spatial_patterns == 'coastal':
            return {'type': 'coastal', 'affected_coast': ['chittagong', 'khulna', 'barisal']}
        else:
            return {'type': 'generic', 'coverage': 'national'}
    
    def _add_hazard_specific_attributes(self, event):
        """Add hazard-specific attributes to the event"""
        if self.hazard_type == 'flood':
            event['flood_type'] = 'riverine' if event['month'] in [6, 7, 8, 9] else 'flash'
            event['duration'] = stats.gamma.rvs(5, scale=3) if event['flood_type'] == 'riverine' else stats.gamma.rvs(2, scale=1)
            event['depth'] = event['intensity']  # Intensity is depth for floods
            
        elif self.hazard_type == 'cyclone':
            event['wind_speed'] = event['intensity']  # Intensity is wind speed for cyclones
            event['storm_surge'] = 0.05 * event['wind_speed'] * self.configs['cyclone']['surge_amplification_factor']
            event['track_direction'] = self._sample_from_dict(self.configs['cyclone']['track_probability'])
            event['rainfall_intensity'] = 10 * np.log(event['wind_speed']) - 40  # mm/hr
            event['duration'] = stats.gamma.rvs(2, scale=12)  # Hours
            
        elif self.hazard_type == 'geophysical':
            if event['type'] == 'earthquake':
                event['magnitude'] = event['intensity']
                event['depth'] = stats.gamma.rvs(2, scale=10)  # km
                event['fault'] = 'dauki' if stats.uniform.rvs() < 0.6 else 'madhupur'
            elif event['type'] == 'landslide':
                event['volume'] = stats.lognorm.rvs(s=1.5, scale=1000)  # cubic meters
                event['slope'] = stats.uniform.rvs(low=25, high=60)  # degrees
                
    def _sample_from_dict(self, probability_dict):
        """Sample a key from a dictionary of probabilities"""
        keys = list(probability_dict.keys())
        probabilities = list(probability_dict.values())
        return keys[stats.rv_discrete(values=(range(len(keys)), probabilities)).rvs()]

class ExposureModel:
    """Model exposed assets, population, and economic activities"""
    def __init__(self, admin_level, population_distribution, building_inventory,
                 critical_infrastructure, economic_activities):
        # Initialize exposure parameters
        self.admin_level = admin_level
        self.population_distribution = population_distribution
        self.building_inventory = building_inventory
        self.critical_infrastructure = critical_infrastructure
        self.economic_activities = economic_activities
        
        # Initialize Bangladesh-specific exposure data
        self.total_population = 169_000_000  # 2023 estimate, will grow over time
        self.population_growth_rate = 0.01  # 1% annual growth
        self.urban_population_pct = 0.39  # 39% urban
        self.urban_growth_rate = 0.03  # 3% annual urban growth
        
        # Administrative divisions
        self.admin_divisions = {
            'division': 8,  # Divisions (highest)
            'district': 64,  # Districts (zila)
            'upazila': 495,  # Sub-districts (upazila/thana)
            'union': 4550  # Union councils (lowest formal admin)
        }
        
        # Building typology distribution
        self.building_types = {
            'RCC': 0.15,  # Reinforced concrete buildings
            'semi_pucca': 0.25,  # Semi-permanent structures
            'kutcha': 0.50,  # Traditional structures
            'jhupri': 0.10,  # Temporary structures
        }
        
        # Critical infrastructure counts
        self.critical_facilities = {
            'hospitals': 620,
            'primary_schools': 65000,
            'secondary_schools': 20300,
            'power_plants': 143,
            'bridges': 4700,
            'embankments_km': 12000,
            'cyclone_shelters': 2500,
            'telecom_towers': 35000,
        }
        
        # Economic sector distribution
        self.economic_sectors = {
            'agriculture': 0.12,  # % of GDP
            'industry': 0.33,  # % of GDP
            'services': 0.55,  # % of GDP
        }
        
        # Agricultural data
        self.agricultural_data = {
            'rice_area_ha': 11_000_000,
            'wheat_area_ha': 350_000,
            'jute_area_ha': 700_000,
            'vegetable_area_ha': 900_000,
            'aquaculture_area_ha': 830_000,
        }
        
        # Load spatial data (placeholder - in real implementation would load from files)
        self._initialize_spatial_data()
        
    def _initialize_spatial_data(self):
        """Initialize spatial datasets for exposure"""
        # In a real implementation, this would load GeoDataFrames from files
        # Here we create placeholder spatial data structures
        
        # Administrative boundaries
        self.admin_boundaries = {
            'division': self._create_dummy_geodataframe(self.admin_divisions['division']),
            'district': self._create_dummy_geodataframe(self.admin_divisions['district']),
            'upazila': self._create_dummy_geodataframe(self.admin_divisions['upazila']),
        }
        
        # Population distribution
        if self.population_distribution == 'gridded':
            # Population density grid (would be a raster in real implementation)
            self.population_grid = self._create_dummy_population_grid()
        
        # Critical infrastructure networks
        if self.critical_infrastructure == 'networked':
            # Transport network
            self.road_network = self._create_dummy_network('road', 80000)  # ~80,000 km of roads
            self.rail_network = self._create_dummy_network('rail', 3200)  # ~3,200 km of rail
            # Electricity transmission network
            self.power_grid = self._create_dummy_network('power', 12000)  # ~12,000 km of power lines
        
    def _create_dummy_geodataframe(self, num_units):
        """Create a dummy GeoDataFrame with random polygons"""
        # In a real implementation, this would load from a shapefile
        # Here we create a placeholder with attributes
        return {'num_units': num_units, 'attributes': {
            'population': np.random.gamma(shape=5, scale=50000, size=num_units),
            'area_km2': np.random.gamma(shape=5, scale=100, size=num_units),
            'building_count': np.random.gamma(shape=5, scale=10000, size=num_units),
            'poverty_rate': np.random.beta(a=2, b=5, size=num_units),
            'urban_pct': np.random.beta(a=1, b=3, size=num_units)
        }}
    
    def _create_dummy_population_grid(self, resolution_km=1):
        """Create a dummy population density grid"""
        # Bangladesh area ~147,570 km²
        grid_size = int(np.sqrt(147570) / resolution_km)
        # Create a matrix with population density values (people/km²)
        # Higher densities in certain areas (urban centers)
        base_density = np.random.gamma(shape=1, scale=500, size=(grid_size, grid_size))
        
        # Add urban centers with higher density
        num_urban_centers = 20
        for _ in range(num_urban_centers):
            x, y = np.random.randint(0, grid_size, 2)
            urban_radius = np.random.randint(5, 20)
            for i in range(max(0, x-urban_radius), min(grid_size, x+urban_radius)):
                for j in range(max(0, y-urban_radius), min(grid_size, y+urban_radius)):
                    dist = np.sqrt((i-x)**2 + (j-y)**2)
                    if dist < urban_radius:
                        # Add high density urban center with decay by distance
                        base_density[i, j] += 5000 * np.exp(-0.1 * dist)
        
        return base_density
    
    def _create_dummy_network(self, network_type, total_length_km):
        """Create a dummy network as a NetworkX graph"""
        # Create a simple random network
        if network_type == 'road':
            # More nodes for road network
            G = nx.random_geometric_graph(1000, 0.1)
        elif network_type == 'rail':
            # Fewer nodes for rail network
            G = nx.random_geometric_graph(200, 0.15)
        elif network_type == 'power':
            # Power grid with specific structure
            G = nx.random_geometric_graph(500, 0.1)
            # Add a few high-capacity transmission lines
            for _ in range(50):
                u, v = np.random.choice(list(G.nodes()), 2, replace=False)
                G.add_edge(u, v, capacity=np.random.gamma(shape=2, scale=100))
        
        # Add attributes to edges
        for u, v in G.edges():
            G[u][v]['length'] = np.random.gamma(shape=2, scale=5)  # km
            G[u][v]['capacity'] = np.random.gamma(shape=2, scale=10)
            G[u][v]['condition'] = np.random.choice(['good', 'fair', 'poor'], p=[0.5, 0.3, 0.2])
            G[u][v]['year_built'] = np.random.randint(1960, 2023)
        
        return G
        
    def get_exposed_elements(self, hazard_footprint):
        """Extract elements exposed to a specific hazard footprint
        
        Args:
            hazard_footprint: Spatial representation of hazard extent
            
        Returns:
            Dictionary of exposed elements by category
        """
        # In a real implementation, this would perform spatial overlay analysis
        # Here we simulate the exposure calculation
        
        # Get appropriate admin level for analysis
        admin_gdf = self.admin_boundaries[self.admin_level]
        
        # Simulate exposure based on hazard type and footprint
        hazard_type = hazard_footprint.get('type', 'generic')
        
        if hazard_type == 'riverine':
            # Affected rivers from the footprint
            affected_rivers = hazard_footprint.get('affected_rivers', [])
            # Simulate exposure based on proximity to affected rivers
            exposure_ratio = len(affected_rivers) / 3  # Normalize by major river systems
            exposure_ratio = min(max(exposure_ratio, 0.1), 0.5)  # Between 10% and 50% exposed
        
        elif hazard_type == 'coastal':
            # Affected coastal areas from the footprint
            affected_coast = hazard_footprint.get('affected_coast', [])
            # Simulate exposure based on affected coastal regions
            exposure_ratio = len(affected_coast) / 3  # Normalize by coastal regions
            exposure_ratio = min(max(exposure_ratio, 0.1), 0.4)  # Between 10% and 40% exposed
        
        else:
            # Generic hazard assumes lower overall exposure
            exposure_ratio = 0.1  # 10% exposure for generic hazards
        
        # Calculate exposed elements
        num_exposed_units = int(admin_gdf['num_units'] * exposure_ratio)
        
        # Simulate which units are exposed (would be based on actual spatial overlap)
        exposed_indices = np.random.choice(admin_gdf['num_units'], 
                                          size=num_exposed_units, 
                                          replace=False)
        
        # Calculate total exposed population
        exposed_population = np.sum(admin_gdf['attributes']['population'][exposed_indices])
        
        # Calculate exposed buildings by type
        exposed_buildings = {}
        total_exposed_buildings = np.sum(admin_gdf['attributes']['building_count'][exposed_indices])
        for building_type, ratio in self.building_types.items():
            exposed_buildings[building_type] = int(total_exposed_buildings * ratio)
        
        # Calculate exposed critical infrastructure (simplified)
        exposed_critical = {}
        for facility_type, count in self.critical_facilities.items():
            exposed_critical[facility_type] = int(count * exposure_ratio * np.random.uniform(0.8, 1.2))
        
        # Calculate exposed agricultural areas
        exposed_agriculture = {}
        for crop_type, area in self.agricultural_data.items():
            if hazard_type == 'riverine' and 'rice' in crop_type:
                # Rice is often in floodplains - higher exposure
                crop_exposure_ratio = exposure_ratio * 1.5
            else:
                crop_exposure_ratio = exposure_ratio
            crop_exposure_ratio = min(crop_exposure_ratio, 0.9)  # Cap at 90%
            exposed_agriculture[crop_type] = int(area * crop_exposure_ratio)
        
        # Return consolidated exposure information
        return {
            'population': exposed_population,
            'buildings': exposed_buildings,
            'critical_infrastructure': exposed_critical,
            'agriculture': exposed_agriculture,
            'admin_units': list(exposed_indices),
            'exposure_ratio': exposure_ratio
        }
    
    def update_exposure(self, year):
        """Update exposure data for the given simulation year
        
        Args:
            year: Simulation year
        """
        # Calculate years since simulation start (2025)
        years_passed = year - 2025
        
        # Update population based on growth rate
        self.total_population *= (1 + self.population_growth_rate) ** years_passed
        
        # Update urban population percentage
        urban_population_increase = years_passed * 0.005  # 0.5% increase per year
        self.urban_population_pct = min(self.urban_population_pct + urban_population_increase, 0.65)
        
        # Update agricultural areas - slight decrease due to urbanization
        for crop_type in self.agricultural_data:
            # Annual reduction rate varies by crop type
            if crop_type == 'rice_area_ha':
                reduction_rate = 0.002  # 0.2% annual reduction
            else:
                reduction_rate = 0.001  # 0.1% annual reduction
            
            self.agricultural_data[crop_type] *= (1 - reduction_rate) ** years_passed
        
        # Update building inventory - more RCC buildings over time
        rcc_increase = years_passed * 0.003  # 0.3% increase per year
        self.building_types['RCC'] = min(self.building_types['RCC'] + rcc_increase, 0.35)
        self.building_types['kutcha'] -= rcc_increase / 2
        self.building_types['semi_pucca'] -= rcc_increase / 2
        
        # Update critical facilities
        self.critical_facilities['cyclone_shelters'] += 50 * years_passed  # 50 new shelters per year
        self.critical_facilities['hospitals'] += 10 * years_passed  # 10 new hospitals per year
        self.critical_facilities['telecom_towers'] += 1000 * years_passed  # 1000 new towers per year
        
        # Update economic sector distribution - shift toward services
        service_increase = years_passed * 0.002  # 0.2% increase in service sector per year
        self.economic_sectors['services'] = min(self.economic_sectors['services'] + service_increase, 0.65)
        self.economic_sectors['agriculture'] -= service_increase / 2
        self.economic_sectors['industry'] -= service_increase / 2

class VulnerabilityModel:
    """Model vulnerability of different exposure elements to hazards"""
    def __init__(self):
        # Initialize vulnerability curves and damage functions
        self._initialize_vulnerability_functions()
    
    def _initialize_vulnerability_functions(self):
        """Initialize vulnerability functions for different elements and hazards"""
        # Building damage functions by building type and hazard
        self.building_vulnerability = {
            # Flood vulnerability functions - maps depth (m) to damage ratio
            'flood': {
                'RCC': {
                    'damage_function': lambda depth: min(0.9, max(0, 0.1 * depth ** 1.25)),
                    'threshold': 0.3,  # Damage begins at 0.3m depth
                    'collapse_threshold': 3.0  # Potential collapse at 3m depth
                },
                'semi_pucca': {
                    'damage_function': lambda depth: min(0.95, max(0, 0.2 * depth ** 1.5)),
                    'threshold': 0.2,
                    'collapse_threshold': 2.5
                },
                'kutcha': {
                    'damage_function': lambda depth: min(1.0, max(0, 0.3 * depth ** 1.7)),
                    'threshold': 0.1,
                    'collapse_threshold': 2.0
                },
                'jhupri': {
                    'damage_function': lambda depth: min(1.0, max(0, 0.5 * depth ** 2.0)),
                    'threshold': 0.05,
                    'collapse_threshold': 1.5
                }
            },
            # Cyclone vulnerability functions - maps wind speed (km/h) to damage ratio
            'cyclone': {
                'RCC': {
                    'damage_function': lambda wind: min(0.9, max(0, 0.0001 * (wind - 80) ** 2 if wind > 80 else 0)),
                    'threshold': 80,  # Damage begins at 80 km/h
                    'collapse_threshold': 250  # Potential collapse at 250 km/h
                },
                'semi_pucca': {
                    'damage_function': lambda wind: min(0.95, max(0, 0.0002 * (wind - 60) ** 2 if wind > 60 else 0)),
                    'threshold': 60,
                    'collapse_threshold': 200
                },
                'kutcha': {
                    'damage_function': lambda wind: min(1.0, max(0, 0.0004 * (wind - 40) ** 2 if wind > 40 else 0)),
                    'threshold': 40,
                    'collapse_threshold': 150
                },
                'jhupri': {
                    'damage_function': lambda wind: min(1.0, max(0, 0.0008 * (wind - 30) ** 2 if wind > 30 else 0)),
                    'threshold': 30,
                    'collapse_threshold': 120
                }
            },
            # Earthquake vulnerability functions - maps PGA (g) to damage ratio
            'earthquake': {
                'RCC': {
                    'damage_function': lambda pga: min(0.9, max(0, 1.5 * pga ** 1.8)),
                    'threshold': 0.1,  # Damage begins at 0.1g
                    'collapse_threshold': 0.6  # Potential collapse at 0.6g
                },
                'semi_pucca': {
                    'damage_function': lambda pga: min(0.95, max(0, 2.0 * pga ** 1.5)),
                    'threshold': 0.08,
                    'collapse_threshold': 0.4
                },
                'kutcha': {
                    'damage_function': lambda pga: min(1.0, max(0, 2.5 * pga ** 1.3)),
                    'threshold': 0.05,
                    'collapse_threshold': 0.3
                },
                'jhupri': {
                    'damage_function': lambda pga: min(1.0, max(0, 3.0 * pga ** 1.2)),
                    'threshold': 0.03,
                    'collapse_threshold': 0.2
                }
            }
        }
        
        # Critical infrastructure vulnerability functions
        self.infrastructure_vulnerability = {
            # Hospital vulnerability to different hazards
            'hospitals': {
                'flood': lambda depth: min(0.8, max(0, 0.15 * depth ** 1.3)),
                'cyclone': lambda wind: min(0.7, max(0, 0.00007 * (wind - 100) ** 2 if wind > 100 else 0)),
                'earthquake': lambda pga: min(0.9, max(0, 1.3 * pga ** 1.7))
            },
            # Schools vulnerability
            'schools': {
                'flood': lambda depth: min(0.9, max(0, 0.2 * depth ** 1.5)),
                'cyclone': lambda wind: min(0.8, max(0, 0.00009 * (wind - 80) ** 2 if wind > 80 else 0)),
                'earthquake': lambda pga: min(0.95, max(0, 1.8 * pga ** 1.5))
            },
            # Bridge vulnerability
            'bridges': {
                'flood': lambda depth: min(0.7, max(0, 0.05 * depth ** 2.5)),  # Scour damage
                'cyclone': lambda wind: min(0.4, max(0, 0.00003 * (wind - 120) ** 2 if wind > 120 else 0)),
                'earthquake': lambda pga: min(0.85, max(0, 1.2 * pga ** 1.8))
            },
            # Embankment vulnerability
            'embankments': {
                'flood': lambda depth: min(1.0, max(0, 0.1 * depth ** 2.2)),
                'cyclone': lambda wind: min(0.6, max(0, 0.00004 * wind ** 1.5)),  # Wave action
                'earthquake': lambda pga: min(0.7, max(0, 1.0 * pga ** 1.6))  # Liquefaction
            },
            # Power infrastructure vulnerability
            'power_infrastructure': {
                'flood': lambda depth: min(0.95, max(0, 0.25 * depth ** 1.2)),
                'cyclone': lambda wind: min(0.9, max(0, 0.0001 * (wind - 60) ** 2 if wind > 60 else 0)),
                'earthquake': lambda pga: min(0.8, max(0, 1.3 * pga ** 1.4))
            },
            # Telecom infrastructure vulnerability
            'telecom': {
                'flood': lambda depth: min(0.9, max(0, 0.2 * depth ** 1.3)),
                'cyclone': lambda wind: min(0.95, max(0, 0.00015 * (wind - 70) ** 2 if wind > 70 else 0)),
                'earthquake': lambda pga: min(0.75, max(0, 1.1 * pga ** 1.5))
            }
        }
        
        # Agricultural vulnerability by crop type and hazard
        self.agricultural_vulnerability = {
            'rice': {
                'flood': lambda depth, duration: min(1.0, max(0, (0.2 * depth + 0.05 * duration))),
                'cyclone': lambda wind: min(1.0, max(0, 0.003 * wind - 0.15 if wind > 50 else 0)),
                'drought': lambda severity: min(1.0, max(0, 0.8 * severity))
            },
            'wheat': {
                'flood': lambda depth, duration: min(1.0, max(0, (0.3 * depth + 0.07 * duration))),
                'cyclone': lambda wind: min(1.0, max(0, 0.0025 * wind - 0.1 if wind > 40 else 0)),
                'drought': lambda severity: min(1.0, max(0, 0.7 * severity))
            },
            'jute': {
                'flood': lambda depth, duration: min(1.0, max(0, (0.15 * depth + 0.04 * duration))),
                'cyclone': lambda wind: min(1.0, max(0, 0.0035 * wind - 0.12 if wind > 45 else 0)),
                'drought': lambda severity: min(1.0, max(0, 0.9 * severity))
            },
            'vegetables': {
                'flood': lambda depth, duration: min(1.0, max(0, (0.35 * depth + 0.08 * duration))),
                'cyclone': lambda wind: min(1.0, max(0, 0.004 * wind - 0.1 if wind > 35 else 0)),
                'drought': lambda severity: min(1.0, max(0, 0.85 * severity))
            },
            'aquaculture': {
                'flood': lambda depth, duration: min(1.0, max(0, (0.1 * depth + 0.02 * duration))),  # Flooding can be less damaging for aquaculture
                'cyclone': lambda wind: min(1.0, max(0, 0.0015 * wind - 0.05 if wind > 60 else 0)),  # Primarily damage to structures
                'drought': lambda severity: min(1.0, max(0, 0.95 * severity))  # Very sensitive to water availability
            }
        }
        
        # Social vulnerability multipliers
        self.social_vulnerability_multipliers = {
            'poverty': lambda poverty_rate: 1.0 + poverty_rate * 0.5,  # 50% increase at 100% poverty rate
            'gender': {'female': 1.2, 'male': 1.0},  # 20% higher vulnerability for women
            'age': lambda age: 1.3 if age < 14 or age > 65 else 1.0,  # 30% higher for children and elderly
            'disability': 1.5,  # 50% higher for persons with disabilities
            'education': lambda edu_years: max(1.0, 1.4 - 0.03 * edu_years),  # Lower with education
            'social_capital': lambda social_index: max(0.7, 1.5 - social_index)  # Lower with social connections
        }
        
        # Functional vulnerability (duration of disruption in days)
        self.functional_disruption = {
            'hospitals': {
                'low_damage': lambda: max(0, np.random.gamma(shape=2.0, scale=2.0)),
                'medium_damage': lambda: max(0, np.random.gamma(shape=5.0, scale=6.0)),
                'high_damage': lambda: max(0, np.random.gamma(shape=10.0, scale=15.0))
            },
            'schools': {
                'low_damage': lambda: max(0, np.random.gamma(shape=3.0, scale=5.0)),
                'medium_damage': lambda: max(0, np.random.gamma(shape=7.0, scale=7.0)),
                'high_damage': lambda: max(0, np.random.gamma(shape=12.0, scale=15.0))
            },
            'power': {
                'low_damage': lambda: max(0, np.random.gamma(shape=1.0, scale=1.0)),
                'medium_damage': lambda: max(0, np.random.gamma(shape=3.0, scale=2.0)),
                'high_damage': lambda: max(0, np.random.gamma(shape=7.0, scale=5.0))
            },
            'water': {
                'low_damage': lambda: max(0, np.random.gamma(shape=2.0, scale=1.5)),
                'medium_damage': lambda: max(0, np.random.gamma(shape=5.0, scale=3.0)),
                'high_damage': lambda: max(0, np.random.gamma(shape=10.0, scale=6.0))
            },
            'transport': {
                'low_damage': lambda: max(0, np.random.gamma(shape=1.0, scale=2.0)),
                'medium_damage': lambda: max(0, np.random.gamma(shape=4.0, scale=5.0)),
                'high_damage': lambda: max(0, np.random.gamma(shape=8.0, scale=10.0))
            },
            'telecom': {
                'low_damage': lambda: max(0, np.random.gamma(shape=1.0, scale=1.0)),
                'medium_damage': lambda: max(0, np.random.gamma(shape=2.0, scale=2.0)),
                'high_damage': lambda: max(0, np.random.gamma(shape=5.0, scale=3.0))
            },
        }
    
    def calculate_damages(self, exposed_elements, hazard_event):
        """Calculate physical and functional damages for exposed elements
        
        Args:
            exposed_elements: Dictionary of exposed elements from ExposureModel
            hazard_event: Hazard event properties including type and intensity
            
        Returns:
            Dictionary of damages by element type
        """
        damages = {
            'buildings': {},
            'casualties': {
                'deaths': 0,
                'injuries': 0,
                'displaced': 0
            },
            'infrastructure': {},
            'agriculture': {},
            'economic': {
                'direct_losses': 0,
                'indirect_losses': 0
            },
            'functional_disruption': {}
        }
        
        hazard_type = hazard_event['type']
        
        # Get hazard intensity parameters
        if hazard_type == 'flood':
            intensity = hazard_event['depth']  # Water depth in meters
            duration = hazard_event.get('duration', 3)  # Duration in days, default 3
        elif hazard_type == 'cyclone':
            intensity = hazard_event['wind_speed']  # Wind speed in km/h
            storm_surge = hazard_event.get('storm_surge', 0)  # Storm surge height in meters
        elif hazard_type == 'earthquake':
            intensity = hazard_event['magnitude'] / 10  # Approximate PGA from magnitude
        else:
            # Default generic intensity scaling
            intensity = hazard_event['intensity']
        
        # 1. Calculate building damages
        for building_type, count in exposed_elements['buildings'].items():
            if hazard_type in self.building_vulnerability and building_type in self.building_vulnerability[hazard_type]:
                damage_function = self.building_vulnerability[hazard_type][building_type]['damage_function']
                damage_ratio = damage_function(intensity)
                damages['buildings'][building_type] = {
                    'count': count,
                    'damage_ratio': damage_ratio,
                    'damaged_count': int(count * damage_ratio)
                }
        
        # 2. Calculate casualties based on building damage and time of day
        total_damaged_buildings = sum(d['damaged_count'] for d in damages['buildings'].values())
        total_buildings = sum(exposed_elements['buildings'].values())
        if total_buildings > 0:
            overall_damage_ratio = total_damaged_buildings / total_buildings
            
            # Casualty calculation depends on hazard type and population density
            if hazard_type == 'flood':
                # Slower onset allows evacuation if warning is available
                fatality_rate = 0.0001 + 0.001 * intensity ** 2
                injury_rate = 0.001 + 0.005 * intensity ** 1.5
                displacement_rate = 0.01 + 0.1 * intensity
            elif hazard_type == 'cyclone':
                # Depends on wind speed and if there's a storm surge
                fatality_rate = 0.0001 * (intensity / 100) ** 2
                if 'storm_surge' in hazard_event:
                    fatality_rate += 0.001 * hazard_event['storm_surge'] ** 2
                injury_rate = 0.001 * (intensity / 80) ** 1.8
                displacement_rate = 0.005 * (intensity / 60) ** 1.5
            elif hazard_type == 'earthquake':
                # Building collapse is primary cause of casualties
                fatality_rate = 0.001 * intensity ** 2.5 * overall_damage_ratio
                injury_rate = 0.01 * intensity ** 2 * overall_damage_ratio
                displacement_rate = 0.05 * intensity ** 1.5 * overall_damage_ratio
            else:
                # Generic hazard
                fatality_rate = 0.0001 * intensity * overall_damage_ratio
                injury_rate = 0.001 * intensity * overall_damage_ratio
                displacement_rate = 0.01 * intensity * overall_damage_ratio
            
            # Calculate casualties
            damages['casualties']['deaths'] = int(exposed_elements['population'] * fatality_rate)
            damages['casualties']['injuries'] = int(exposed_elements['population'] * injury_rate)
            damages['casualties']['displaced'] = int(exposed_elements['population'] * displacement_rate)
        
        # 3. Calculate infrastructure damages
        for infra_type, count in exposed_elements['critical_infrastructure'].items():
            # Map the infrastructure types to our vulnerability categories
            vulnerability_key = None
            if 'hospital' in infra_type:
                vulnerability_key = 'hospitals'
            elif 'school' in infra_type:
                vulnerability_key = 'schools'
            elif 'bridge' in infra_type:
                vulnerability_key = 'bridges'
            elif 'embankment' in infra_type:
                vulnerability_key = 'embankments'
            elif 'power' in infra_type:
                vulnerability_key = 'power_infrastructure'
            elif 'telecom' in infra_type:
                vulnerability_key = 'telecom'
            
            if vulnerability_key and vulnerability_key in self.infrastructure_vulnerability:
                if hazard_type in self.infrastructure_vulnerability[vulnerability_key]:
                    damage_function = self.infrastructure_vulnerability[vulnerability_key][hazard_type]
                    damage_ratio = damage_function(intensity)
                    damages['infrastructure'][infra_type] = {
                        'count': count,
                        'damage_ratio': damage_ratio,
                        'damaged_count': int(count * damage_ratio)
                    }
                    
                    # Calculate functional disruption
                    if vulnerability_key in self.functional_disruption:
                        if damage_ratio < 0.2:
                            disruption_days = self.functional_disruption[vulnerability_key]['low_damage']()
                        elif damage_ratio < 0.5:
                            disruption_days = self.functional_disruption[vulnerability_key]['medium_damage']()
                        else:
                            disruption_days = self.functional_disruption[vulnerability_key]['high_damage']()
                        
                        damages['functional_disruption'][infra_type] = {
                            'mean_disruption_days': disruption_days,
                            'total_service_days_lost': int(count * damage_ratio * disruption_days)
                        }
        
        # 4. Calculate agricultural damages
        for crop_type, area in exposed_elements['agriculture'].items():
            # Map crop type to our vulnerability categories
            vulnerability_key = None
            if 'rice' in crop_type:
                vulnerability_key = 'rice'
            elif 'wheat' in crop_type:
                vulnerability_key = 'wheat'
            elif 'jute' in crop_type:
                vulnerability_key = 'jute'
            elif 'vegetable' in crop_type:
                vulnerability_key = 'vegetables'
            elif 'aquaculture' in crop_type:
                vulnerability_key = 'aquaculture'
            else:
                vulnerability_key = 'rice'  # Default if no match
            
            if vulnerability_key and vulnerability_key in self.agricultural_vulnerability:
                if hazard_type == 'flood' and 'flood' in self.agricultural_vulnerability[vulnerability_key]:
                    damage_function = self.agricultural_vulnerability[vulnerability_key]['flood']
                    damage_ratio = damage_function(intensity, hazard_event.get('duration', 3))
                elif hazard_type == 'cyclone' and 'cyclone' in self.agricultural_vulnerability[vulnerability_key]:
                    damage_function = self.agricultural_vulnerability[vulnerability_key]['cyclone']
                    damage_ratio = damage_function(intensity)
                elif hazard_type == 'drought' and 'drought' in self.agricultural_vulnerability[vulnerability_key]:
                    damage_function = self.agricultural_vulnerability[vulnerability_key]['drought']
                    damage_ratio = damage_function(intensity)
                else:
                    # Generic damage model
                    damage_ratio = min(0.9, max(0, 0.2 * intensity))
                
                damages['agriculture'][crop_type] = {
                    'area_ha': area,
                    'damage_ratio': damage_ratio,
                    'damaged_area_ha': int(area * damage_ratio)
                }
        
        # 5. Calculate economic losses
        # Direct losses from physical damages
        building_losses = self._calculate_building_losses(damages['buildings'])
        infrastructure_losses = self._calculate_infrastructure_losses(damages['infrastructure'])
        agriculture_losses = self._calculate_agriculture_losses(damages['agriculture'])
        
        damages['economic']['direct_losses'] = building_losses + infrastructure_losses + agriculture_losses
        
        # Indirect losses (simplified as a function of direct losses and functional disruption)
        disruption_factor = sum(d.get('total_service_days_lost', 0) for d in damages['functional_disruption'].values()) / 100
        indirect_loss_multiplier = min(3.0, max(0.2, 0.5 + 0.1 * disruption_factor))
        damages['economic']['indirect_losses'] = damages['economic']['direct_losses'] * indirect_loss_multiplier
        
        return damages
    
    def _calculate_building_losses(self, building_damages):
        """Calculate economic losses from building damages"""
        # Average values in BDT (Bangladesh Taka)
        building_values = {
            'RCC': 5000000,  # 50 lakh per building
            'semi_pucca': 1500000,  # 15 lakh per building
            'kutcha': 500000,  # 5 lakh per building
            'jhupri': 100000,  # 1 lakh per building
        }
        
        total_loss = 0
        for building_type, damage in building_damages.items():
            if building_type in building_values:
                avg_value = building_values[building_type]
                total_loss += damage['damaged_count'] * avg_value * damage['damage_ratio']
        
        return total_loss
    
    def _calculate_infrastructure_losses(self, infrastructure_damages):
        """Calculate economic losses from infrastructure damages"""
        # Average values in BDT (Bangladesh Taka)
        infrastructure_values = {
            'hospitals': 100000000,  # 10 crore per hospital
            'primary_schools': 10000000,  # 1 crore per primary school
            'secondary_schools': 20000000,  # 2 crore per secondary school
            'power_plants': 5000000000,  # 500 crore per power plant
            'bridges': 50000000,  # 5 crore per bridge
            'embankments_km': 10000000,  # 1 crore per km
            'cyclone_shelters': 20000000,  # 2 crore per shelter
            'telecom_towers': 5000000,  # 50 lakh per tower
        }
        
        total_loss = 0
        for infra_type, damage in infrastructure_damages.items():
            value_key = next((key for key in infrastructure_values.keys() if key in infra_type), None)
            if value_key:
                avg_value = infrastructure_values[value_key]
                total_loss += damage['damaged_count'] * avg_value * damage['damage_ratio']
        
        return total_loss
    
    def _calculate_agriculture_losses(self, agriculture_damages):
        """Calculate economic losses from agricultural damages"""
        # Average yield values in BDT per hectare
        agriculture_values = {
            'rice_area_ha': 150000,  # 1.5 lakh per hectare per season
            'wheat_area_ha': 120000,  # 1.2 lakh per hectare per season
            'jute_area_ha': 200000,  # 2 lakh per hectare per season
            'vegetable_area_ha': 300000,  # 3 lakh per hectare per season
            'aquaculture_area_ha': 500000,  # 5 lakh per hectare per season
        }
        
        total_loss = 0
        for crop_type, damage in agriculture_damages.items():
            if crop_type in agriculture_values:
                avg_value = agriculture_values[crop_type]
                total_loss += damage['damaged_area_ha'] * avg_value * damage['damage_ratio']
        
        return total_loss

class ClimateChangeModel:
    """Model climate change impacts on disaster profiles"""
    def __init__(self):
        # Initialize climate change scenarios and impact parameters
        self._initialize_climate_scenarios()
        
    def _initialize_climate_scenarios(self):
        """Initialize climate change scenarios based on IPCC projections"""
        # Base year for projections
        self.base_year = 2025
        
        # Define climate change scenarios (based on IPCC AR6)
        self.scenarios = {
            # Intermediate-low emissions scenario
            'RCP4.5': {
                'temperature_increase': {
                    # Yearly temperature increase in °C by decade
                    2030: 0.8,
                    2040: 1.1,
                    2050: 1.4
                },
                'precipitation_change': {
                    # Seasonal precipitation change factors by decade
                    # Values: [pre-monsoon, monsoon, post-monsoon, winter]
                    2030: [0.05, 0.08, 0.04, -0.02],
                    2040: [0.08, 0.12, 0.06, -0.03],
                    2050: [0.10, 0.15, 0.08, -0.05]
                },
                'sea_level_rise': {
                    # Sea level rise in meters by decade
                    2030: 0.12,
                    2040: 0.22,
                    2050: 0.32
                },
                'cyclone_intensity_factor': {
                    # Cyclone intensity increase factor by decade
                    2030: 0.05,
                    2040: 0.08,
                    2050: 0.12
                },
                'drought_frequency_factor': {
                    # Drought frequency increase factor by decade
                    2030: 0.10,
                    2040: 0.15,
                    2050: 0.20
                },
                'extreme_rainfall_factor': {
                    # Extreme rainfall intensity increase factor by decade
                    2030: 0.07,
                    2040: 0.12,
                    2050: 0.18
                }
            },
            # High emissions scenario
            'RCP8.5': {
                'temperature_increase': {
                    # Yearly temperature increase in °C by decade
                    2030: 1.0,
                    2040: 1.6,
                    2050: 2.2
                },
                'precipitation_change': {
                    # Seasonal precipitation change factors by decade
                    # Values: [pre-monsoon, monsoon, post-monsoon, winter]
                    2030: [0.07, 0.11, 0.06, -0.04],
                    2040: [0.12, 0.18, 0.09, -0.08],
                    2050: [0.18, 0.25, 0.12, -0.12]
                },
                'sea_level_rise': {
                    # Sea level rise in meters by decade
                    2030: 0.15,
                    2040: 0.30,
                    2050: 0.45
                },
                'cyclone_intensity_factor': {
                    # Cyclone intensity increase factor by decade
                    2030: 0.08,
                    2040: 0.15,
                    2050: 0.25
                },
                'drought_frequency_factor': {
                    # Drought frequency increase factor by decade
                    2030: 0.15,
                    2040: 0.25,
                    2050: 0.35
                },
                'extreme_rainfall_factor': {
                    # Extreme rainfall intensity increase factor by decade
                    2030: 0.10,
                    2040: 0.20,
                    2050: 0.30
                }
            },
            # Very low emissions scenario
            'RCP2.6': {
                'temperature_increase': {
                    # Yearly temperature increase in °C by decade
                    2030: 0.6,
                    2040: 0.8,
                    2050: 0.9
                },
                'precipitation_change': {
                    # Seasonal precipitation change factors by decade
                    # Values: [pre-monsoon, monsoon, post-monsoon, winter]
                    2030: [0.03, 0.05, 0.02, -0.01],
                    2040: [0.05, 0.07, 0.03, -0.02],
                    2050: [0.06, 0.08, 0.04, -0.02]
                },
                'sea_level_rise': {
                    # Sea level rise in meters by decade
                    2030: 0.10,
                    2040: 0.18,
                    2050: 0.24
                },
                'cyclone_intensity_factor': {
                    # Cyclone intensity increase factor by decade
                    2030: 0.03,
                    2040: 0.05,
                    2050: 0.07
                },
                'drought_frequency_factor': {
                    # Drought frequency increase factor by decade
                    2030: 0.05,
                    2040: 0.08,
                    2050: 0.10
                },
                'extreme_rainfall_factor': {
                    # Extreme rainfall intensity increase factor by decade
                    2030: 0.05,
                    2040: 0.07,
                    2050: 0.09
                }
            }
        }
        
        # Regional vulnerability to climate change impacts
        # Higher values indicate greater sensitivity to climate impacts
        self.regional_sensitivity = {
            'coastal': {
                'sea_level_rise': 1.0,
                'cyclone': 1.0,
                'salinity': 1.0,
                'flood': 0.7,
                'drought': 0.5
            },
            'floodplain': {
                'sea_level_rise': 0.3,
                'cyclone': 0.6,
                'salinity': 0.5,
                'flood': 1.0,
                'drought': 0.7
            },
            'haor_basin': {
                'sea_level_rise': 0.1,
                'cyclone': 0.4,
                'salinity': 0.2,
                'flood': 0.9,
                'drought': 0.5
            },
            'barind_tract': {
                'sea_level_rise': 0.0,
                'cyclone': 0.3,
                'salinity': 0.1,
                'flood': 0.4,
                'drought': 1.0
            },
            'hill_tracts': {
                'sea_level_rise': 0.0,
                'cyclone': 0.5,
                'salinity': 0.0,
                'flood': 0.3,
                'drought': 0.6
            },
            'urban': {
                'sea_level_rise': 0.6,  # Coastal cities
                'cyclone': 0.8,
                'salinity': 0.5,
                'flood': 0.9,  # Urban flooding
                'drought': 0.7
            }
        }
        
        # Hazard-specific climate sensitivity models
        self.hazard_climate_models = {
            'flood': self._apply_flood_climate_impacts,
            'cyclone': self._apply_cyclone_climate_impacts,
            'drought': self._apply_drought_climate_impacts,
            'sea_level_rise': self._apply_slr_climate_impacts
        }
    
    def apply_climate_scenarios(self, hazards, year, scenario):
        """Modify hazard parameters based on climate projections
        
        Args:
            hazards: Dictionary of hazard models to modify
            year: Simulation year
            scenario: Climate scenario to apply (e.g., 'RCP4.5', 'RCP8.5')
            
        Returns:
            Dictionary of climate effects applied to each hazard
        """
        # Check if the scenario is valid
        if scenario not in self.scenarios:
            print(f"Warning: Unknown climate scenario '{scenario}'. Using RCP4.5 as default.")
            scenario = 'RCP4.5'
        
        # Get the decade marker for projections (rounded down to nearest decade)
        decade = (year // 10) * 10
        if decade < 2030:
            decade = 2030
        elif decade > 2050:
            decade = 2050
        
        # Get climate parameters for the specified decade and scenario
        climate_params = {
            'temperature_increase': self.scenarios[scenario]['temperature_increase'][decade],
            'precipitation_change': self.scenarios[scenario]['precipitation_change'][decade],
            'sea_level_rise': self.scenarios[scenario]['sea_level_rise'][decade],
            'cyclone_intensity_factor': self.scenarios[scenario]['cyclone_intensity_factor'][decade],
            'drought_frequency_factor': self.scenarios[scenario]['drought_frequency_factor'][decade],
            'extreme_rainfall_factor': self.scenarios[scenario]['extreme_rainfall_factor'][decade]
        }
        
        # Apply climate impacts to each hazard type
        climate_effects = {}
        for hazard_type, hazard_model in hazards.items():
            # Call the appropriate hazard-specific climate impact function
            if hazard_type in self.hazard_climate_models:
                climate_effects[hazard_type] = self.hazard_climate_models[hazard_type](hazard_model, climate_params)
            else:
                # Generic impacts for undefined hazard types
                climate_effects[hazard_type] = {
                    'intensity_change': 0.05,  # Default 5% increase in intensity
                    'frequency_change': 0.05   # Default 5% increase in frequency
                }
        
        return climate_effects
    
    def _apply_flood_climate_impacts(self, hazard_model, climate_params):
        """Apply climate change impacts to flood hazards
        
        Args:
            hazard_model: The flood hazard model to modify
            climate_params: Climate change parameters for the scenario and decade
            
        Returns:
            Dictionary of climate effects specific to floods
        """
        # Pre-monsoon and monsoon precipitation changes most relevant for flooding
        pre_monsoon_change = climate_params['precipitation_change'][0]
        monsoon_change = climate_params['precipitation_change'][1]
        
        # Calculate overall precipitation change factor (weighted toward monsoon)
        precip_change_factor = 0.3 * pre_monsoon_change + 0.7 * monsoon_change
        
        # Calculate compound impacts
        # 1. Extreme rainfall intensification
        rainfall_intensity_factor = climate_params['extreme_rainfall_factor']
        
        # 2. Sea level rise impact on drainage congestion in coastal areas
        drainage_impact = 0.5 * climate_params['sea_level_rise']
        
        # 3. Temperature impact on snowmelt contribution to riverine flooding
        snowmelt_factor = 0.1 * climate_params['temperature_increase']
        
        # Combined intensity change for floods
        intensity_change = precip_change_factor + rainfall_intensity_factor + drainage_impact + snowmelt_factor
        
        # Frequency change (more frequent flooding with climate change)
        frequency_change = 0.7 * rainfall_intensity_factor + 0.3 * precip_change_factor
        
        # Modify flood parameters based on climate impacts
        return {
            'intensity_change': intensity_change,
            'frequency_change': frequency_change,
            'duration_change': 0.5 * intensity_change,  # Longer floods with higher intensity
            'affected_parameters': {
                'precipitation': precip_change_factor,
                'extreme_rainfall': rainfall_intensity_factor,
                'drainage': drainage_impact,
                'snowmelt': snowmelt_factor
            }
        }
    
    def _apply_cyclone_climate_impacts(self, hazard_model, climate_params):
        """Apply climate change impacts to cyclone hazards
        
        Args:
            hazard_model: The cyclone hazard model to modify
            climate_params: Climate change parameters for the scenario and decade
            
        Returns:
            Dictionary of climate effects specific to cyclones
        """
        # Direct cyclone intensity modification
        intensity_factor = climate_params['cyclone_intensity_factor']
        
        # Sea surface temperature impact on cyclogenesis
        sst_impact = 0.8 * climate_params['temperature_increase'] / 2.0  # Half of global mean surface temperature
        
        # Sea level rise impact on storm surge height
        surge_amplification = climate_params['sea_level_rise']
        
        # Combined intensity change
        intensity_change = intensity_factor + sst_impact
        
        # Frequency change (complex relationship - may be fewer but more intense cyclones)
        # Current science suggests slight decrease in frequency but increase in intensity
        frequency_change = -0.05 + 0.1 * sst_impact  # Net small increase
        
        # Modify cyclone parameters based on climate impacts
        return {
            'intensity_change': intensity_change,
            'frequency_change': frequency_change,
            'storm_surge_amplification': surge_amplification,
            'rainfall_intensity_increase': 0.3 + intensity_change,  # More intense rainfall in cyclones
            'affected_parameters': {
                'wind_speed': intensity_change,
                'sea_surface_temperature': sst_impact,
                'storm_surge': surge_amplification
            }
        }
    
    def _apply_drought_climate_impacts(self, hazard_model, climate_params):
        """Apply climate change impacts to drought hazards
        
        Args:
            hazard_model: The drought hazard model to modify
            climate_params: Climate change parameters for the scenario and decade
            
        Returns:
            Dictionary of climate effects specific to droughts
        """
        # Winter and pre-monsoon precipitation changes most relevant for drought
        winter_change = climate_params['precipitation_change'][3]  # Negative value represents decrease
        pre_monsoon_change = climate_params['precipitation_change'][0]
        
        # Temperature increase impacts evapotranspiration and soil moisture
        evapotranspiration_factor = 0.15 * climate_params['temperature_increase']
        
        # Calculate drought intensity change
        # Negative precipitation change (drying) increases drought intensity
        intensity_change = -1.0 * winter_change + evapotranspiration_factor - 0.5 * pre_monsoon_change
        
        # Drought frequency change 
        frequency_change = climate_params['drought_frequency_factor']
        
        # Modify drought parameters based on climate impacts
        return {
            'intensity_change': intensity_change,
            'frequency_change': frequency_change,
            'duration_change': 0.7 * intensity_change,  # Longer droughts with higher intensity
            'affected_parameters': {
                'winter_precipitation': winter_change,
                'evapotranspiration': evapotranspiration_factor,
                'soil_moisture': -0.8 * intensity_change
            }
        }
    
    def _apply_slr_climate_impacts(self, hazard_model, climate_params):
        """Apply sea level rise impacts
        
        Args:
            hazard_model: The SLR hazard model to modify
            climate_params: Climate change parameters for the scenario and decade
            
        Returns:
            Dictionary of climate effects specific to sea level rise
        """
        # Direct sea level rise value
        slr = climate_params['sea_level_rise']
        
        # Salinity intrusion factor (how far inland saltwater moves)
        salinity_intrusion = 2.0 * slr  # Simplified: 1m SLR causes 2km inland intrusion
        
        # Coastal erosion acceleration
        erosion_factor = 5.0 * slr  # Simplified: coastal retreat amplified by SLR
        
        # Area permanently inundated
        # Bangladesh has large areas below 5m elevation
        inundation_area_km2 = 500 * slr  # Simplified: ~500 km² per meter of SLR
        
        return {
            'sea_level_rise_m': slr,
            'salinity_intrusion_km': salinity_intrusion,
            'coastal_erosion_amplification': erosion_factor,
            'permanent_inundation_km2': inundation_area_km2,
            'affected_parameters': {
                'inundation_depth': slr,
                'groundwater_salinity': 0.5 * slr,
                'coastal_flooding_frequency': 2.0 * slr
            }
        }

class EarlyWarningModel:
    """Model forecast, warning dissemination, and response"""
    def __init__(self):
        # Initialize early warning system parameters
        self._initialize_early_warning_systems()
    
    def _initialize_early_warning_systems(self):
        """Initialize early warning system capabilities by hazard and region"""
        # Forecast skill by hazard type and lead time
        # Values represent error reduction compared to climatology (0.0-1.0 scale)
        # Higher values indicate better forecasts
        self.forecast_skill = {
            'flood': {
                # Lead time in days
                1: 0.85,  # 1-day ahead forecast skill
                3: 0.70,  # 3-day ahead forecast skill
                5: 0.55,  # 5-day ahead forecast skill
                7: 0.40,  # 7-day ahead forecast skill
                10: 0.25   # 10-day ahead forecast skill
            },
            'flash_flood': {
                # Lead time in hours
                1: 0.70,  # 1-hour ahead forecast skill
                3: 0.55,  # 3-hour ahead forecast skill
                6: 0.40,  # 6-hour ahead forecast skill
                12: 0.25,  # 12-hour ahead forecast skill
                24: 0.15   # 24-hour ahead forecast skill
            },
            'cyclone': {
                # Lead time in hours
                24: 0.80,  # 24-hour ahead forecast skill
                48: 0.70,  # 48-hour ahead forecast skill
                72: 0.55,  # 72-hour ahead forecast skill
                96: 0.45,  # 96-hour ahead forecast skill
                120: 0.35  # 120-hour ahead forecast skill
            },
            'storm_surge': {
                # Lead time in hours
                6: 0.75,  # 6-hour ahead forecast skill
                12: 0.65,  # 12-hour ahead forecast skill
                24: 0.50,  # 24-hour ahead forecast skill
                36: 0.35,  # 36-hour ahead forecast skill
                48: 0.25   # 48-hour ahead forecast skill
            },
            'drought': {
                # Lead time in months
                0.5: 0.65,  # 2-week ahead forecast skill
                1: 0.55,    # 1-month ahead forecast skill
                2: 0.45,    # 2-month ahead forecast skill
                3: 0.35,    # 3-month ahead forecast skill
                6: 0.25     # 6-month ahead forecast skill
            }
        }
        
        # Warning dissemination systems and coverage
        self.dissemination_systems = {
            'sirens': {
                'coverage': 0.15,  # % of population covered
                'reliability': 0.80,  # % of time system works as intended
                'comprehension': 0.95,  # % of people who understand meaning
                'lead_time': 0.1,  # hours required to activate
                'urban_bias': 0.7,  # higher coverage in urban areas
                'placement': ['coastal', 'flood_prone']
            },
            'sms': {
                'coverage': 0.70,  # % of population with mobile phones
                'reliability': 0.85,  # % of time system works as intended
                'comprehension': 0.80,  # % of people who understand meaning
                'lead_time': 0.2,  # hours required to activate
                'urban_bias': 0.6,  # higher coverage in urban areas
                'literacy_dependent': True
            },
            'radio': {
                'coverage': 0.85,  # % of population with access
                'reliability': 0.90,  # % of time system works as intended
                'comprehension': 0.85,  # % of people who understand meaning
                'lead_time': 0.5,  # hours required to activate
                'urban_bias': 0.2,  # small urban bias
                'literacy_dependent': False
            },
            'television': {
                'coverage': 0.60,  # % of population with access
                'reliability': 0.85,  # % of time system works as intended
                'comprehension': 0.90,  # % of people who understand meaning
                'lead_time': 0.5,  # hours required to activate
                'urban_bias': 0.5,  # moderate urban bias
                'electricity_dependent': True
            },
            'volunteer_network': {
                'coverage': 0.55,  # % of population covered
                'reliability': 0.75,  # % of time system works as intended
                'comprehension': 0.95,  # % of people who understand meaning
                'lead_time': 1.0,  # hours required to activate
                'urban_bias': -0.3,  # better in rural areas
                'training_dependent': True
            },
            'mosque_announcements': {
                'coverage': 0.90,  # % of population covered
                'reliability': 0.70,  # % of time system works as intended
                'comprehension': 0.95,  # % of people who understand meaning
                'lead_time': 1.0,  # hours required to activate
                'urban_bias': -0.1,  # slightly better in rural areas
                'time_of_day_dependent': True
            }
        }
        
        # Evacuation behavior parameters by demographic
        self.evacuation_behavior = {
            'compliance_base_rate': 0.65,  # Base compliance rate
            'gender_factor': {
                'male': 1.0,
                'female': 0.85  # Lower due to care responsibilities and mobility constraints
            },
            'age_factor': {
                'child': 1.1,  # Higher as part of family units
                'adult': 1.0,
                'elderly': 0.75  # Lower due to mobility and attachment to property
            },
            'income_factor': {
                'low': 0.85,  # Lower due to livelihood concerns and lack of transport
                'medium': 1.0,
                'high': 1.1  # Higher due to better resources and transportation
            },
            'previous_experience': {
                'none': 0.9,  # Lower without prior experience
                'false_alarm': 0.7,  # Much lower after false alarms
                'minor_impact': 1.1,  # Higher after experiencing minor impacts
                'major_impact': 1.3  # Much higher after experiencing major impacts
            },
            'warning_specificity_factor': {
                'generic': 0.8,
                'location_specific': 1.0,
                'impact_based': 1.2  # Higher for impact-based forecasts
            },
            'warning_lead_time_factor': {
                'very_short': 0.8,  # Less than 3 hours
                'short': 0.9,  # 3-12 hours
                'adequate': 1.1,  # 12-48 hours
                'long': 1.0  # More than 48 hours (decreases due to uncertainty)
            },
            'livelihood_factor': {
                'agriculture': 0.8,  # Lower due to crop/livestock concerns
                'fishing': 0.85,  # Lower due to boat/equipment concerns
                'business': 0.9,  # Lower due to property protection
                'service': 1.0,
                'government': 1.1  # Higher due to awareness
            }
        }
        
        # Regional early warning system development level (0.0-1.0 scale)
        self.regional_ews_capacity = {
            'coastal': 0.8,  # High capacity due to cyclone preparedness program
            'urban': 0.7,  # Good capacity in urban centers
            'flood_plain': 0.6,  # Moderate capacity in major flood plains
            'haor_basin': 0.5,  # Lower capacity in flash flood prone areas
            'char_lands': 0.4,  # Low capacity in river islands
            'hill_tracts': 0.4,  # Low capacity in remote hill areas
            'barind_tract': 0.5   # Moderate capacity in drought prone areas
        }
        
        # Impact of false alarms on future compliance
        self.false_alarm_effect = {
            'decay_rate': 0.15,  # Compliance reduction per false alarm
            'recovery_time': 3,   # Years to recover from false alarm
            'minimum_compliance': 0.3  # Floor on compliance even after many false alarms
        }
    
    def simulate_warning_process(self, hazard_event, system_capabilities):
        """Simulate the early warning process for a hazard event
        
        Args:
            hazard_event: Dictionary with hazard properties
            system_capabilities: Dictionary with EWS capabilities and resources
            
        Returns:
            Dictionary with warning process results
        """
        # Extract relevant hazard information
        hazard_type = hazard_event['type']
        hazard_intensity = hazard_event['intensity']
        region_type = hazard_event['spatial_footprint'].get('type', 'generic')
        
        # Determine whether warning is possible based on hazard type
        if hazard_type not in self.forecast_skill:
            # No warning system for this hazard type
            warning_possible = False
            forecast_lead_time = 0
            forecast_accuracy = 0
        else:
            # Warning is possible
            warning_possible = True
            
            # Determine available lead time (hazard-specific)
            if hazard_type == 'flood':
                # Riverine floods have longer lead times
                available_lead_times = [1, 3, 5, 7, 10]  # days
                if 'duration' in hazard_event and hazard_event['duration'] > 2:
                    # For longer-duration floods, we have more lead time
                    forecast_lead_time = np.random.choice([5, 7, 10], p=[0.3, 0.4, 0.3])
                else:
                    forecast_lead_time = np.random.choice([1, 3, 5], p=[0.3, 0.4, 0.3])
                    
            elif hazard_type == 'flash_flood':
                # Flash floods have very short lead times
                available_lead_times = [1, 3, 6, 12, 24]  # hours
                forecast_lead_time = np.random.choice([1, 3, 6], p=[0.5, 0.3, 0.2])
                
            elif hazard_type == 'cyclone':
                # Cyclones typically have days of lead time
                available_lead_times = [24, 48, 72, 96, 120]  # hours
                forecast_lead_time = np.random.choice([48, 72, 96], p=[0.3, 0.4, 0.3])
                
            elif hazard_type == 'storm_surge':
                # Storm surge follows cyclone but with less lead time
                available_lead_times = [6, 12, 24, 36, 48]  # hours
                forecast_lead_time = np.random.choice([12, 24, 36], p=[0.3, 0.4, 0.3])
                
            elif hazard_type == 'drought':
                # Droughts have longest lead times but highest uncertainty
                available_lead_times = [0.5, 1, 2, 3, 6]  # months
                forecast_lead_time = np.random.choice([0.5, 1, 2], p=[0.3, 0.4, 0.3])
            
            else:
                # Generic hazard
                forecast_lead_time = 1  # Default 1 day lead time
                available_lead_times = [1]
            
            # Determine forecast accuracy based on lead time and hazard type
            # Find the closest available lead time
            closest_lead_time = min(available_lead_times, key=lambda x: abs(x - forecast_lead_time))
            base_forecast_skill = self.forecast_skill[hazard_type][closest_lead_time]
            
            # Adjust forecast skill based on system capabilities
            technology_factor = system_capabilities.get('technology_level', 0.5)
            training_factor = system_capabilities.get('staff_training', 0.5)
            data_factor = system_capabilities.get('observation_network', 0.5)
            
            # Calculate modified forecast accuracy
            forecast_accuracy = base_forecast_skill * (
                0.7 + 0.1 * technology_factor + 0.1 * training_factor + 0.1 * data_factor)
            forecast_accuracy = min(0.95, max(0.1, forecast_accuracy))  # Bounded between 0.1 and 0.95
        
        # If warning is not possible, return early
        if not warning_possible:
            return {
                'warning_issued': False,
                'reason': 'No warning system available for this hazard type',
                'lead_time': 0,
                'population_reached': 0,
                'evacuation_rate': 0,
                'lives_saved': 0
            }
        
        # Determine warning decision (could be a false alarm or missed warning)
        # Based on forecast accuracy and random chance
        actual_hazard_occurs = True  # We know this hazard will occur in the simulation
        warning_threshold = system_capabilities.get('warning_threshold', 0.5)
        forecast_probability = np.random.beta(forecast_accuracy * 10, (1 - forecast_accuracy) * 10)
        
        # Decide whether to issue warning based on forecast probability and threshold
        warning_issued = forecast_probability >= warning_threshold
        
        # If no warning issued, return early
        if not warning_issued:
            return {
                'warning_issued': False,
                'reason': 'Forecast probability below threshold',
                'forecast_probability': forecast_probability,
                'warning_threshold': warning_threshold,
                'lead_time': forecast_lead_time,
                'population_reached': 0,
                'evacuation_rate': 0,
                'lives_saved': 0
            }
        
        # Warning is issued - calculate dissemination effectiveness
        # Get regional warning system capacity
        if region_type == 'coastal':
            region_capacity = self.regional_ews_capacity['coastal']
        elif region_type == 'riverine':
            region_capacity = self.regional_ews_capacity['flood_plain']
        elif 'urban' in region_type:
            region_capacity = self.regional_ews_capacity['urban']
        else:
            # Default to average capacity
            region_capacity = np.mean(list(self.regional_ews_capacity.values()))
        
        # Calculate warning dissemination effectiveness
        # Use the available dissemination systems based on system capabilities
        available_systems = []
        if system_capabilities.get('sirens', False):
            available_systems.append('sirens')
        if system_capabilities.get('sms', False):
            available_systems.append('sms')
        if system_capabilities.get('radio', False):
            available_systems.append('radio')
        if system_capabilities.get('television', False):
            available_systems.append('television')
        if system_capabilities.get('volunteer_network', False):
            available_systems.append('volunteer_network')
        if system_capabilities.get('mosque_announcements', False):
            available_systems.append('mosque_announcements')
        
        # If no systems specified, use all systems with reduced effectiveness
        if not available_systems:
            available_systems = list(self.dissemination_systems.keys())
            system_effectiveness_factor = 0.7  # Reduced effectiveness
        else:
            system_effectiveness_factor = 1.0
        
        # Calculate population reached by warning
        population_reached_by_system = {}
        total_population = system_capabilities.get('affected_population', 1000000)
        urban_ratio = system_capabilities.get('urban_population_ratio', 0.4)
        rural_ratio = 1.0 - urban_ratio
        
        for system in available_systems:
            system_info = self.dissemination_systems[system]
            base_coverage = system_info['coverage']
            
            # Adjust for urban/rural bias
            urban_bias = system_info.get('urban_bias', 0)
            urban_coverage = base_coverage * (1 + urban_bias)
            rural_coverage = base_coverage * (1 - urban_bias)
            
            # Overall population covered by this system
            system_coverage = urban_coverage * urban_ratio + rural_coverage * rural_ratio
            system_coverage = min(1.0, max(0.0, system_coverage))  # Bound between 0 and 1
            
            # Adjust for reliability
            effective_coverage = system_coverage * system_info['reliability'] * system_effectiveness_factor
            
            # Calculate population reached by this system
            population_reached_by_system[system] = int(total_population * effective_coverage)
        
        # Calculate total population reached (accounting for overlap between systems)
        # Using probabilistic method to account for overlap
        cumulative_probability_unreached = 1.0
        for system, reached in population_reached_by_system.items():
            probability_reached_by_system = reached / total_population
            cumulative_probability_unreached *= (1.0 - probability_reached_by_system)
        
        overall_probability_reached = 1.0 - cumulative_probability_unreached
        population_reached = int(total_population * overall_probability_reached)
        
        # Calculate warning comprehension
        comprehension_rates = [self.dissemination_systems[s]['comprehension'] for s in available_systems]
        avg_comprehension = np.mean(comprehension_rates) if comprehension_rates else 0.5
        
        # Adjust for message clarity and consistency
        message_clarity = system_capabilities.get('message_clarity', 0.5)
        message_consistency = system_capabilities.get('message_consistency', 0.5)
        
        effective_comprehension = avg_comprehension * (
            0.7 + 0.15 * message_clarity + 0.15 * message_consistency)
        effective_comprehension = min(0.95, max(0.2, effective_comprehension))
        
        # Calculate population that both received and understood the warning
        population_informed = int(population_reached * effective_comprehension)
        
        # Calculate evacuation behavior based on warning lead time and other factors
        # Determine lead time category
        if hazard_type in ['cyclone', 'storm_surge', 'flash_flood']:
            # Convert hours to appropriate category
            if forecast_lead_time < 3:
                lead_time_category = 'very_short'
            elif forecast_lead_time < 12:
                lead_time_category = 'short'
            elif forecast_lead_time < 48:
                lead_time_category = 'adequate'
            else:
                lead_time_category = 'long'
        else:
            # For slower onset hazards (using days)
            if forecast_lead_time < 0.125:  # Less than 3 hours
                lead_time_category = 'very_short'
            elif forecast_lead_time < 0.5:  # Less than 12 hours
                lead_time_category = 'short'
            elif forecast_lead_time < 2:  # Less than 48 hours
                lead_time_category = 'adequate'
            else:
                lead_time_category = 'long'
        
        # Get lead time factor
        lead_time_factor = self.evacuation_behavior['warning_lead_time_factor'][lead_time_category]
        
        # Determine warning specificity
        if system_capabilities.get('impact_based_forecasting', False):
            specificity = 'impact_based'
        elif system_capabilities.get('location_specific_warnings', False):
            specificity = 'location_specific'
        else:
            specificity = 'generic'
        
        # Get warning specificity factor
        specificity_factor = self.evacuation_behavior['warning_specificity_factor'][specificity]
        
        # Get previous experience factor
        previous_experience = system_capabilities.get('previous_experience', 'none')
        experience_factor = self.evacuation_behavior['previous_experience'][previous_experience]
        
        # Calculate base evacuation rate
        base_evacuation_rate = self.evacuation_behavior['compliance_base_rate']
        
        # Calculate adjusted evacuation rate
        evacuation_rate = base_evacuation_rate * lead_time_factor * specificity_factor * experience_factor
        evacuation_rate = min(0.95, max(0.05, evacuation_rate))  # Bound between 0.05 and 0.95
        
        # Calculate evacuated population
        evacuated_population = int(population_informed * evacuation_rate)
        
        # Calculate lives saved based on hazard intensity and evacuation
        # Assume baseline fatality rate without evacuation based on hazard intensity
        if hazard_type == 'flood':
            baseline_fatality_rate = 0.0001 + 0.001 * hazard_intensity ** 2
        elif hazard_type == 'cyclone':
            baseline_fatality_rate = 0.0001 * (hazard_intensity / 100) ** 2
            if 'storm_surge' in hazard_event:
                baseline_fatality_rate += 0.001 * hazard_event['storm_surge'] ** 2
        elif hazard_type == 'flash_flood':
            baseline_fatality_rate = 0.0005 + 0.002 * hazard_intensity ** 2
        else:
            # Generic hazard
            baseline_fatality_rate = 0.0001 * hazard_intensity
        
        # Calculate lives saved through evacuation
        potential_fatalities = int(total_population * baseline_fatality_rate)
        lives_saved = int(potential_fatalities * (evacuated_population / total_population) * 0.9)
        # Assuming 90% of potential fatalities among evacuees are prevented
        
        # Return comprehensive warning process results
        return {
            'warning_issued': warning_issued,
            'forecast_lead_time': forecast_lead_time,
            'forecast_accuracy': forecast_accuracy,
            'hazard_type': hazard_type,
            'hazard_intensity': hazard_intensity,
            'region_type': region_type,
            'dissemination_systems': available_systems,
            'total_population': total_population,
            'population_reached': population_reached,
            'population_informed': population_informed,
            'evacuation_rate': evacuation_rate,
            'evacuated_population': evacuated_population,
            'potential_fatalities': potential_fatalities,
            'lives_saved': lives_saved,
            'warning_effectiveness': lives_saved / potential_fatalities if potential_fatalities > 0 else 0
        }

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

class RecoveryModel:
    """Model post-disaster recovery trajectories"""
    def __init__(self):
        pass
    def simulate_recovery(self, disaster_impacts, governance_quality, funding_availability):
        # Project recovery timelines and outcomes
        pass

class TransboundaryModel:
    """Model cross-border disaster dimensions"""
    def __init__(self):
        pass
    def simulate_transboundary_effects(self, upstream_conditions, cooperation_level):
        # Calculate impacts of cross-border factors
        pass

class ResilienceModel:
    """Model resilience investments and effectiveness"""
    def __init__(self):
        pass
    def simulate_resilience_building(self, investment_patterns, implementation_quality):
        # Calculate resilience improvements over time
        pass

class GovernanceModel:
    """Model disaster governance effectiveness"""
    def __init__(self, institutional_arrangements, coordination_mechanisms,
                 resource_allocation, transparency_level):
        # Initialize governance parameters
        self.institutional_arrangements = institutional_arrangements
        self.coordination_mechanisms = coordination_mechanisms
        self.resource_allocation = resource_allocation
        self.transparency_level = transparency_level

class SocioeconomicModel:
    """Model socioeconomic dimensions of disaster risk"""
    def __init__(self):
        pass
    def calculate_differential_impacts(self, hazard_exposure, demographic_profile):
        # Calculate socially differentiated disaster impacts
        pass

class TechnologyModel:
    """Model technology applications in disaster management"""
    def __init__(self):
        pass
    def simulate_technology_adoption(self, digital_infrastructure, skill_levels):
        # Calculate technology impact on disaster management
        pass

class DisasterDataHandler:
    """Handle disaster data loading and preprocessing"""
    def __init__(self):
        pass
    def load_historical_data(self, sources):
        # Load and preprocess historical disaster data
        pass

    def integrate_realtime_data(self, api_connections):
        # Set up connections to real-time data sources
        pass

class DisasterResultsAnalyzer:
    """Analyze and visualize disaster simulation results"""
    def __init__(self):
        pass
    def generate_risk_metrics(self):
        # Calculate disaster risk indicators
        pass

    def analyze_spatial_patterns(self):
        # Analyze spatial distributions of impacts
        pass

class BangladeshDisasterSimulation:
    """Main simulation environment integrating all components"""
    def __init__(self, config):
        # Initialize simulation with configuration parameters
        self.config = config
        self.hazards = self._initialize_hazards(config)
        self.exposure = ExposureModel(**config['exposure'])
        self.vulnerability = VulnerabilityModel()
        self.climate = ClimateChangeModel()
        self.early_warning = EarlyWarningModel()
        self.response = EmergencyResponseModel()
        self.recovery = RecoveryModel()
        self.transboundary = TransboundaryModel()
        self.resilience = ResilienceModel()
        self.governance = GovernanceModel(**config['governance'])
        self.socioeconomic = SocioeconomicModel()
        self.technology = TechnologyModel()
        self.data_handler = DisasterDataHandler()
        self.results_analyzer = DisasterResultsAnalyzer()

    def _initialize_hazards(self, config):
        # Initialize hazard models based on configuration
        hazard_models = {}
        for hazard_type, hazard_config in config['hazards'].items():
            hazard_models[hazard_type] = HazardModel(**hazard_config)
        return hazard_models
        
    def run_simulation(self, years=25, scenarios=None):
        # Execute multi-year simulation across scenarios
        print("Running simulation...")
        start_year = 2025
        end_year = 2050
        if scenarios is None:
            scenarios = ['RCP4.5', 'RCP8.5'] # Example scenarios

        for year in range(start_year, end_year + 1):
            for scenario in scenarios:
                print(f"Simulating year {year} under scenario {scenario}...")

                # 1. Apply climate change effects
                self.climate.apply_climate_scenarios(self.hazards, year, scenario)

                # 2. Generate hazard events
                for hazard_type, hazard_model in self.hazards.items():
                    # Example: Generate a hazard event based on the hazard model
                    hazard_intensity = hazard_model.intensity_scales # Placeholder

                    # 3. Model exposure and vulnerability
                    # Calculate damages based on exposure and vulnerability
                    damages = self.vulnerability.calculate_damages(self.exposure, hazard_intensity)

                    # 4. Simulate early warning and response
                    self.early_warning.simulate_warning_process(hazard_intensity, {})
                    self.response.simulate_response(damages, {})

                    # 5. Simulate recovery
                    self.recovery.simulate_recovery(damages, self.governance, {})

                    # 6. Analyze the results
                    self.results_analyzer.generate_risk_metrics()
                    self.results_analyzer.analyze_spatial_patterns()

if __name__ == '__main__':
    # Example usage
    config = {
        'hazards': {
            'flood': {
                'hazard_type': 'flood',
                'return_periods': [10, 20, 50, 100],
                'intensity_scales': {'depth': 'meters', 'velocity': 'm/s'},
                'spatial_patterns': 'riverine',
                'seasonal_profile': 'monsoon',
                'climate_sensitivity': {'rainfall': 0.1, 'sea_level_rise': 0.2}
            },
            'cyclone': {
                'hazard_type': 'cyclone',
                'return_periods': [5, 10, 20, 50],
                'intensity_scales': {'wind_speed': 'km/h', 'storm_surge': 'meters'},
                'spatial_patterns': 'coastal',
                'seasonal_profile': 'pre_monsoon_post_monsoon',
                'climate_sensitivity': {'sea_surface_temperature': 0.15}
            }
        },
        'exposure': {
            'admin_level': 'upazila',
            'population_distribution': 'gridded',
            'building_inventory': 'typology_based',
            'critical_infrastructure': 'networked',
            'economic_activities': 'sectoral'
        },
        'governance': {
            'institutional_arrangements': 'centralized',
            'coordination_mechanisms': 'tiered',
            'resource_allocation': 'formula_based',
            'transparency_level': 'moderate'
        }
    }

    simulation = BangladeshDisasterSimulation(config)
    simulation.run_simulation()
