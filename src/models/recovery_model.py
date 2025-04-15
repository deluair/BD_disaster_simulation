"""
RecoveryModel: Models post-disaster recovery trajectories
"""

import numpy as np

class RecoveryModel:
    """Model post-disaster recovery trajectories"""
    def __init__(self):
        # Initialize recovery parameters
        self._initialize_recovery_parameters()
        
    def _initialize_recovery_parameters(self):
        """Initialize recovery parameters for different sectors and systems"""
        # Recovery rates by sector (fraction recovered per month)
        self.recovery_rates = {
            'housing': {
                'RCC': 0.10,          # 10% per month
                'semi_pucca': 0.08,   # 8% per month
                'kutcha': 0.15,       # 15% per month (easier to rebuild)
                'jhupri': 0.20        # 20% per month (easiest to rebuild)
            },
            'infrastructure': {
                'roads': 0.12,        # 12% per month
                'bridges': 0.05,      # 5% per month (more complex)
                'electricity': 0.15,  # 15% per month
                'water_supply': 0.10, # 10% per month
                'schools': 0.08,      # 8% per month
                'hospitals': 0.07,    # 7% per month
                'embankments': 0.06   # 6% per month
            },
            'livelihoods': {
                'agriculture': 0.15,  # 15% per month (depends on crop cycles)
                'fishing': 0.12,      # 12% per month
                'small_business': 0.10, # 10% per month
                'industry': 0.08,     # 8% per month
                'service_sector': 0.12 # 12% per month
            },
            'social_systems': {
                'community_networks': 0.18, # 18% per month
                'education': 0.10,    # 10% per month
                'healthcare': 0.08,   # 8% per month
                'governance': 0.07    # 7% per month
            }
        }
        
        # Economic recovery multipliers
        self.economic_recovery_multipliers = {
            'funding_level': {
                'very_low': 0.6,      # < 20% of needs
                'low': 0.8,           # 20-50% of needs
                'medium': 1.0,        # 50-80% of needs
                'high': 1.2,          # 80-100% of needs
                'very_high': 1.3      # > 100% of needs
            },
            'pre_disaster_economy': {
                'contracting': 0.8,    # Economy was already in decline
                'stable': 1.0,         # Economy was stable
                'growing': 1.2         # Economy was growing
            },
            'economic_diversity': {
                'low': 0.8,            # Low economic diversity (vulnerable)
                'medium': 1.0,         # Medium economic diversity
                'high': 1.2            # High economic diversity (resilient)
            }
        }
        
        # Governance quality impact on recovery
        self.governance_recovery_factors = {
            'coordination': {
                'poor': 0.7,
                'fair': 0.9,
                'good': 1.1,
                'excellent': 1.3
            },
            'planning_capacity': {
                'low': 0.8,
                'medium': 1.0,
                'high': 1.2
            },
            'corruption_level': {
                'high': 0.7,
                'medium': 0.9,
                'low': 1.1
            },
            'community_engagement': {
                'low': 0.8,
                'medium': 1.0,
                'high': 1.2
            }
        }
        
        # Recovery patterns (controls shape of recovery curve)
        self.recovery_patterns = {
            'linear': lambda t, max_t: t / max_t,
            'early_rapid': lambda t, max_t: np.sqrt(t / max_t),
            'late_rapid': lambda t, max_t: (t / max_t) ** 2,
            's_shaped': lambda t, max_t: 1 / (1 + np.exp(-10 * (t / max_t - 0.5)))
        }
        
        # Bangladesh-specific regional factors affecting recovery
        self.regional_recovery_factors = {
            'coastal': 0.9,        # Cyclone exposure slows recovery
            'urban': 1.1,          # Better resources, faster recovery
            'flood_plain': 0.9,    # Recurrent flooding slows recovery
            'haor_basin': 0.8,     # Seasonal challenges
            'hill_tracts': 0.8,    # Remote, challenging terrain
            'char_lands': 0.7      # Very vulnerable riverine islands
        }
        
        # Seasonal effects on recovery
        self.seasonal_recovery_factors = {
            # Months (1=January, etc.)
            1: 0.9,   # Winter - moderate
            2: 1.0,   # Winter-Spring transition - good
            3: 1.1,   # Spring - good
            4: 1.0,   # Spring-Summer transition
            5: 0.9,   # Pre-monsoon - slowing
            6: 0.7,   # Early monsoon - significant slowdown
            7: 0.6,   # Peak monsoon - major slowdown
            8: 0.6,   # Peak monsoon - major slowdown
            9: 0.7,   # Late monsoon - significant slowdown
            10: 0.9,  # Post-monsoon - improving
            11: 1.0,  # Post-monsoon - good
            12: 0.9   # Winter - moderate
        }
        
        # "Build Back Better" effectiveness (additional resilience gained during recovery)
        self.build_back_better_effectiveness = {
            'policy_strength': {
                'weak': 0.1,       # 10% improvement
                'moderate': 0.2,   # 20% improvement
                'strong': 0.3      # 30% improvement
            },
            'funding_allocation': {
                'low': 0.1,        # 10% of funds to BBB
                'medium': 0.2,     # 20% of funds to BBB
                'high': 0.3        # 30% of funds to BBB
            },
            'technical_capacity': {
                'limited': 0.6,    # Effectiveness multiplier
                'adequate': 1.0,
                'strong': 1.3
            }
        }
    
    def simulate_recovery(self, disaster_impacts, governance_quality, funding_availability):
        """Simulate post-disaster recovery trajectories
        
        Args:
            disaster_impacts: Dictionary of disaster impacts from VulnerabilityModel
            governance_quality: Dictionary with governance quality parameters
            funding_availability: Dictionary with recovery funding parameters
            
        Returns:
            Dictionary with recovery trajectories and outcomes
        """
        # Extract key impact information
        affected_sectors = {
            'housing': disaster_impacts.get('buildings', {}),
            'infrastructure': disaster_impacts.get('infrastructure', {}),
            'livelihoods': disaster_impacts.get('economic', {}),
            'casualties': disaster_impacts.get('casualties', {})
        }
        
        # Determine recovery time horizons (months)
        recovery_horizons = self._calculate_recovery_horizons(affected_sectors)
        
        # Determine funding level category
        funding_needs = self._estimate_funding_needs(disaster_impacts)
        available_funding = funding_availability.get('total_funding', funding_needs * 0.7) # Default 70% of needs
        funding_ratio = available_funding / funding_needs
        
        if funding_ratio < 0.2:
            funding_level = 'very_low'
        elif funding_ratio < 0.5:
            funding_level = 'low'
        elif funding_ratio < 0.8:
            funding_level = 'medium'
        elif funding_ratio < 1.0:
            funding_level = 'high'
        else:
            funding_level = 'very_high'
            
        funding_multiplier = self.economic_recovery_multipliers['funding_level'][funding_level]
        
        # Calculate governance effect on recovery
        coordination_level = governance_quality.get('coordination', 'fair')
        planning_capacity = governance_quality.get('planning_capacity', 'medium')
        corruption_level = governance_quality.get('corruption_level', 'medium')
        community_engagement = governance_quality.get('community_engagement', 'medium')
        
        governance_multiplier = (
            self.governance_recovery_factors['coordination'][coordination_level] * 0.3 +
            self.governance_recovery_factors['planning_capacity'][planning_capacity] * 0.3 +
            self.governance_recovery_factors['corruption_level'][corruption_level] * 0.2 +
            self.governance_recovery_factors['community_engagement'][community_engagement] * 0.2
        )
        
        # Apply regional factor
        region_type = disaster_impacts.get('region_type', 'flood_plain')
        if region_type in self.regional_recovery_factors:
            regional_multiplier = self.regional_recovery_factors[region_type]
        else:
            regional_multiplier = 1.0
            
        # Calculate "Build Back Better" improvements
        bbb_policy = funding_availability.get('bbb_policy_strength', 'moderate')
        bbb_funding = funding_availability.get('bbb_funding_allocation', 'medium')
        bbb_capacity = funding_availability.get('bbb_technical_capacity', 'adequate')
        
        bbb_improvement = (
            self.build_back_better_effectiveness['policy_strength'][bbb_policy] *
            self.build_back_better_effectiveness['funding_allocation'][bbb_funding] *
            self.build_back_better_effectiveness['technical_capacity'][bbb_capacity]
        )
        
        # Generate recovery trajectories
        recovery_trajectories = {}
        for sector, horizon in recovery_horizons.items():
            # Adjust recovery rate based on all factors
            base_trajectory = self._generate_sector_trajectory(
                sector, 
                horizon, 
                funding_multiplier, 
                governance_multiplier, 
                regional_multiplier,
                affected_sectors
            )
            
            # Apply "Build Back Better" improvements
            if bbb_improvement > 0:
                final_state = base_trajectory[-1] * (1 + bbb_improvement)
                # Ensure we don't exceed 100% recovery (or 110% with BBB)
                recovery_trajectories[sector] = [
                    min(val, final_state) for val in base_trajectory
                ]
            else:
                recovery_trajectories[sector] = base_trajectory
        
        # Calculate derived metrics
        recovery_milestones = self._calculate_recovery_milestones(recovery_trajectories)
        recovery_quality = self._assess_recovery_quality(recovery_trajectories, bbb_improvement)
        
        # Return comprehensive recovery results
        return {
            'recovery_trajectories': recovery_trajectories,
            'recovery_horizon_months': recovery_horizons,
            'recovery_milestones': recovery_milestones,
            'recovery_quality': recovery_quality,
            'funding_ratio': funding_ratio,
            'bbb_improvement': bbb_improvement,
            'total_funding_needs': funding_needs,
            'available_funding': available_funding
        }
    
    def _calculate_recovery_horizons(self, affected_sectors):
        """Calculate how long recovery will take for each sector"""
        horizons = {}
        
        # Housing recovery horizon
        housing_damages = affected_sectors.get('housing', {})
        if housing_damages:
            # Calculate weighted average recovery rate
            total_damaged = 0
            weighted_rate = 0
            for building_type, damage in housing_damages.items():
                damaged_count = damage.get('damaged_count', 0)
                total_damaged += damaged_count
                if building_type in self.recovery_rates['housing']:
                    weighted_rate += damaged_count * self.recovery_rates['housing'][building_type]
            
            if total_damaged > 0:
                avg_rate = weighted_rate / total_damaged
                horizons['housing'] = min(60, int(1.0 / avg_rate)) # Cap at 5 years
            else:
                horizons['housing'] = 0
        else:
            horizons['housing'] = 0
            
        # Infrastructure recovery horizon
        infra_damages = affected_sectors.get('infrastructure', {})
        if infra_damages:
            total_damaged = 0
            weighted_rate = 0
            for infra_type, damage in infra_damages.items():
                damaged_count = damage.get('damaged_count', 0)
                total_damaged += damaged_count
                
                # Map to our infrastructure types
                mapped_type = None
                if 'road' in infra_type.lower():
                    mapped_type = 'roads'
                elif 'bridge' in infra_type.lower():
                    mapped_type = 'bridges'
                elif 'electric' in infra_type.lower() or 'power' in infra_type.lower():
                    mapped_type = 'electricity'
                elif 'water' in infra_type.lower():
                    mapped_type = 'water_supply'
                elif 'school' in infra_type.lower():
                    mapped_type = 'schools'
                elif 'hospital' in infra_type.lower() or 'clinic' in infra_type.lower():
                    mapped_type = 'hospitals'
                elif 'embankment' in infra_type.lower() or 'levee' in infra_type.lower():
                    mapped_type = 'embankments'
                else:
                    # Default to average of all infrastructure types
                    mapped_type = 'roads'
                
                weighted_rate += damaged_count * self.recovery_rates['infrastructure'][mapped_type]
            
            if total_damaged > 0:
                avg_rate = weighted_rate / total_damaged
                horizons['infrastructure'] = min(72, int(1.0 / avg_rate)) # Cap at 6 years
            else:
                horizons['infrastructure'] = 0
        else:
            horizons['infrastructure'] = 0
            
        # Livelihoods recovery horizon
        econ_damages = affected_sectors.get('livelihoods', {})
        if econ_damages:
            # Direct losses usually recover faster than indirect
            direct_losses = econ_damages.get('direct_losses', 0)
            indirect_losses = econ_damages.get('indirect_losses', 0)
            
            # Assume different recovery rates for direct vs indirect
            direct_recovery_rate = 0.12  # 12% per month
            indirect_recovery_rate = 0.08  # 8% per month
            
            # Weighted average
            if direct_losses + indirect_losses > 0:
                weighted_rate = (direct_losses * direct_recovery_rate + 
                                indirect_losses * indirect_recovery_rate) / (direct_losses + indirect_losses)
                horizons['livelihoods'] = min(60, int(1.0 / weighted_rate)) # Cap at 5 years
            else:
                horizons['livelihoods'] = 0
        else:
            horizons['livelihoods'] = 0
            
        # Community/social recovery horizon
        # This is often tied to population displacement and casualties
        casualties = affected_sectors.get('casualties', {})
        if casualties:
            displaced = casualties.get('displaced', 0)
            deaths = casualties.get('deaths', 0)
            injuries = casualties.get('injuries', 0)
            
            # Social recovery is affected by all of these
            if deaths + injuries + displaced > 0:
                # Deaths have longest-lasting impact on social fabric
                death_weight = 5  # Each death has 5x impact on recovery time
                injury_weight = 1
                displacement_weight = 0.5
                
                social_impact = (deaths * death_weight + injuries * injury_weight + 
                                displaced * displacement_weight)
                
                # Scale to a reasonable time horizon
                horizons['social'] = min(84, int(social_impact / 1000)) # Cap at 7 years
            else:
                horizons['social'] = 0
        else:
            horizons['social'] = 0
            
        return horizons
    
    def _estimate_funding_needs(self, disaster_impacts):
        """Estimate total funding needs for recovery"""
        # Extract economic losses
        economic = disaster_impacts.get('economic', {})
        direct_losses = economic.get('direct_losses', 0)
        indirect_losses = economic.get('indirect_losses', 0)
        
        # Recovery funding typically exceeds direct losses due to:
        # 1. Building back better (not just replacing)
        # 2. Indirect losses that need addressing
        # 3. Administrative and transaction costs
        
        # Simple formula: funding needs = direct losses * 1.5 + indirect losses * 0.5
        funding_needs = direct_losses * 1.5 + indirect_losses * 0.5
        
        return funding_needs
    
    def _generate_sector_trajectory(self, sector, horizon, funding_multiplier, 
                                  governance_multiplier, regional_multiplier, affected_sectors):
        """Generate recovery trajectory for a sector"""
        if horizon == 0:
            # No damage to this sector
            return [1.0]
            
        # Choose recovery pattern based on sector
        if sector == 'housing':
            # Housing often follows an early-rapid pattern
            pattern_func = self.recovery_patterns['early_rapid']
        elif sector == 'infrastructure':
            # Infrastructure often follows S-shaped recovery
            pattern_func = self.recovery_patterns['s_shaped']
        elif sector == 'livelihoods':
            # Livelihoods often follow S-shaped recovery
            pattern_func = self.recovery_patterns['s_shaped']
        elif sector == 'social':
            # Social recovery is often late-rapid
            pattern_func = self.recovery_patterns['late_rapid']
        else:
            # Default to linear
            pattern_func = self.recovery_patterns['linear']
            
        # Create monthly timesteps
        timesteps = np.arange(0, horizon + 1)
        
        # Apply recovery pattern function
        base_trajectory = [pattern_func(t, horizon) for t in timesteps]
        
        # Apply multipliers to adjust trajectory
        adjusted_trajectory = []
        current_month = 1  # Start at January (arbitrary)
        
        for t_idx, recovery_level in enumerate(base_trajectory):
            # Apply seasonal factor based on month
            month_idx = ((current_month + t_idx - 1) % 12) + 1  # Cycle through months
            seasonal_factor = self.seasonal_recovery_factors[month_idx]
            
            # Calculate adjusted recovery
            if t_idx == 0:
                # Start at 0
                adjusted_recovery = 0
            else:
                # The increment from last month to this month is scaled by our factors
                increment = base_trajectory[t_idx] - base_trajectory[t_idx-1]
                adjusted_increment = increment * funding_multiplier * governance_multiplier * regional_multiplier * seasonal_factor
                adjusted_recovery = adjusted_trajectory[-1] + adjusted_increment
                
                # Ensure we don't exceed 100% recovery
                adjusted_recovery = min(1.0, adjusted_recovery)
                
            adjusted_trajectory.append(adjusted_recovery)
            
        return adjusted_trajectory
    
    def _calculate_recovery_milestones(self, recovery_trajectories):
        """Calculate key recovery milestones"""
        milestones = {}
        
        for sector, trajectory in recovery_trajectories.items():
            sector_milestones = {}
            
            # Find months to reach key recovery percentages
            for threshold in [0.3, 0.5, 0.7, 0.9]:
                # First month to exceed threshold
                for month, value in enumerate(trajectory):
                    if value >= threshold:
                        sector_milestones[f'{int(threshold*100)}%_recovery'] = month
                        break
                else:
                    # Never reached this threshold
                    sector_milestones[f'{int(threshold*100)}%_recovery'] = None
            
            milestones[sector] = sector_milestones
            
        return milestones
    
    def _assess_recovery_quality(self, recovery_trajectories, bbb_improvement):
        """Assess the quality of recovery based on trajectories and BBB"""
        quality_metrics = {}
        
        for sector, trajectory in recovery_trajectories.items():
            # Measure recovery speed (time to 50% recovery)
            halfway_point = None
            for month, value in enumerate(trajectory):
                if value >= 0.5:
                    halfway_point = month
                    break
            
            if halfway_point is not None:
                # Normalize to a 0-1 scale where 1 is extremely fast
                # Assume 12 months (1 year) is a "good" recovery time
                speed_score = 12 / max(1, halfway_point)
                speed_score = min(1.0, speed_score)
            else:
                speed_score = 0
                
            # Measure recovery completeness (final value)
            completeness = trajectory[-1]
            
            # Measure recovery quality (influenced by BBB)
            quality = min(1.0, completeness * (1 + bbb_improvement))
            
            quality_metrics[sector] = {
                'speed': speed_score,
                'completeness': completeness,
                'quality': quality,
                'overall_score': (speed_score * 0.3 + completeness * 0.3 + quality * 0.4)
            }
            
        # Calculate aggregate quality score
        if quality_metrics:
            overall_scores = [metrics['overall_score'] for metrics in quality_metrics.values()]
            quality_metrics['aggregate'] = {
                'overall_score': sum(overall_scores) / len(overall_scores)
            }
            
        return quality_metrics
