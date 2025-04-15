"""
ExposureModel class: Models exposed assets, population, and economic activities
"""

import numpy as np
import networkx as nx

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
            
        # Calculate exposed critical infrastructure
        exposed_infrastructure = {}
        for infra_type, count in self.critical_facilities.items():
            # Simulate exposure based on spatial distribution
            exposed_infrastructure[infra_type] = int(count * exposure_ratio * 0.8)  # Slightly lower ratio
            
        # Calculate exposed agricultural land
        exposed_agriculture = {}
        for crop_type, area in self.agricultural_data.items():
            # Different crops have different exposure rates
            if 'rice' in crop_type:
                crop_exposure = exposure_ratio * 1.2  # Rice more exposed in flood plains
            elif 'aquaculture' in crop_type:
                crop_exposure = exposure_ratio * 1.5  # Aquaculture more exposed in coastal areas
            else:
                crop_exposure = exposure_ratio * 0.9
                
            exposed_agriculture[crop_type] = int(area * crop_exposure)
            
        # Return all exposed elements
        return {
            'population': exposed_population,
            'buildings': exposed_buildings,
            'infrastructure': exposed_infrastructure,
            'agriculture': exposed_agriculture,
            'exposure_ratio': exposure_ratio
        }
