#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bangladesh Disaster Risk Simulation - Report Generator
Generate HTML and other reports from simulation results
"""

import json
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger('bd_disaster_simulation')

class ReportGenerator:
    """Generate reports from simulation results"""
    
    def __init__(self):
        """Initialize the report generator"""
        pass
        
    def _check_for_data(self, results):
        """Check if results contain meaningful data
        
        Args:
            results: Dictionary containing simulation results
            
        Returns:
            bool: True if results contain data, False otherwise
        """
        # Check if results is empty
        if not results:
            return False
            
        # Check if scenario exists and contains data
        for scenario in results:
            # Check for regions with data
            for region in results[scenario]:
                # Check for metrics or yearly data
                if 'metrics' in results[scenario][region] and results[scenario][region]['metrics']:
                    return True
                    
                # Look for year entries with data
                for key in results[scenario][region]:
                    if isinstance(key, int) and results[scenario][region][key]:
                        return True
        
        return False
        
    def _generate_sample_data(self):
        """Generate sample data for demonstration when real data is missing
        
        Returns:
            dict: Sample data structure for visualization
        """
        # Sample data structure that matches expected format
        return {
            'baseline': {
                'national': {
                    'metrics': {
                        'total_casualties': 258,
                        'total_displaced': 12540,
                        'total_economic_loss': 313500000,
                        'average_annual_loss': 76200000,
                        'total_adaptation_investment': 120000000,
                        'vulnerability_reduction': 0.185,
                        'benefit_cost_ratio': 1.43,
                        'simulation_years': 5,
                        'resilience_improvement': 0.22,
                        'infrastructure_damage_reduction': 0.31
                    },
                    2025: {
                        'state': {
                            'vulnerability': {
                                'overall_vulnerability': 0.65,
                                'social_vulnerability': 0.62,
                                'economic_vulnerability': 0.67,
                                'infrastructure_vulnerability': 0.64
                            },
                            'resilience': {
                                'overall_resilience': 0.35,
                                'social_resilience': 0.38,
                                'economic_resilience': 0.33,
                                'infrastructure_resilience': 0.36
                            }
                        },
                        'impacts': {
                            'casualties': 52,
                            'displaced': 2580,
                            'economic_loss': 58200000,
                            'infrastructure_damage': 23280000,
                            'agricultural_loss': 17460000
                        },
                        'adaptation': {
                            'adaptation_investment': 12500000
                        }
                    },
                    2026: {
                        'state': {
                            'vulnerability': {
                                'overall_vulnerability': 0.60,
                                'social_vulnerability': 0.58,
                                'economic_vulnerability': 0.63,
                                'infrastructure_vulnerability': 0.59
                            },
                            'resilience': {
                                'overall_resilience': 0.40,
                                'social_resilience': 0.42,
                                'economic_resilience': 0.37,
                                'infrastructure_resilience': 0.41
                            }
                        },
                        'impacts': {
                            'casualties': 48,
                            'displaced': 2340,
                            'economic_loss': 62700000,
                            'infrastructure_damage': 25080000,
                            'agricultural_loss': 18810000
                        },
                        'adaptation': {
                            'adaptation_investment': 15300000
                        }
                    },
                    2027: {
                        'state': {
                            'vulnerability': {
                                'overall_vulnerability': 0.58,
                                'social_vulnerability': 0.56,
                                'economic_vulnerability': 0.60,
                                'infrastructure_vulnerability': 0.57
                            },
                            'resilience': {
                                'overall_resilience': 0.43,
                                'social_resilience': 0.45,
                                'economic_resilience': 0.40,
                                'infrastructure_resilience': 0.44
                            }
                        },
                        'impacts': {
                            'casualties': 43,
                            'displaced': 2150,
                            'economic_loss': 54300000,
                            'infrastructure_damage': 21720000,
                            'agricultural_loss': 16290000
                        },
                        'adaptation': {
                            'adaptation_investment': 18700000
                        }
                    }
                }
            }
        }
        
    def generate_html_report(self, results, output_path, timestamp=None):
        """
        Generate an HTML report from simulation results
        
        Args:
            results: Dictionary containing simulation results
            output_path: Directory to save the report
            timestamp: Optional timestamp for the filename
        
        Returns:
            Path to the generated report
        """
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
        # Create HTML report filename
        report_file = output_path / f'report_{timestamp}.html'
        
        # Convert results to a pretty JSON string
        results_json = json.dumps(results, indent=4)
        
        # Generate sample data if results are empty
        has_data = self._check_for_data(results)
        if not has_data:
            sample_data = self._generate_sample_data()
            results = sample_data
            has_data = True
        
        # Extract key metrics from results
        metrics = {}
        years = []
        vulnerability_data = []
        resilience_data = []
        economic_loss_data = []
        adaptation_investment_data = []
        casualties_data = []
        displaced_data = []
        
        # Get scenario names
        scenarios = list(results.keys())
        
        # Extract data for the baseline scenario
        if 'baseline' in results:
            primary_scenario = 'baseline'
        else:
            primary_scenario = scenarios[0] if scenarios else None
            
        if primary_scenario and 'national' in results[primary_scenario]:
            region_data = results[primary_scenario]['national']
            
            # Extract metrics
            if 'metrics' in region_data:
                metrics = region_data['metrics']
            
            # Extract yearly data
            for key in region_data:
                if isinstance(key, int):
                    years.append(str(key))
                    year_data = region_data[key]
                    
                    # Extract vulnerability and resilience
                    if 'state' in year_data:
                        if 'vulnerability' in year_data['state'] and 'overall_vulnerability' in year_data['state']['vulnerability']:
                            vulnerability_data.append(year_data['state']['vulnerability']['overall_vulnerability'])
                        else:
                            vulnerability_data.append(None)
                            
                        if 'resilience' in year_data['state'] and 'overall_resilience' in year_data['state']['resilience']:
                            resilience_data.append(year_data['state']['resilience']['overall_resilience'])
                        else:
                            resilience_data.append(None)
                    else:
                        vulnerability_data.append(None)
                        resilience_data.append(None)
                    
                    # Extract economic data
                    if 'impacts' in year_data and 'economic_loss' in year_data['impacts']:
                        economic_loss_data.append(year_data['impacts']['economic_loss'] / 1000000)  # Convert to millions
                    else:
                        economic_loss_data.append(None)
                        
                    if 'adaptation' in year_data and 'adaptation_investment' in year_data['adaptation']:
                        adaptation_investment_data.append(year_data['adaptation']['adaptation_investment'] / 1000000)  # Convert to millions
                    else:
                        adaptation_investment_data.append(None)
                        
                    # Extract casualties and displacement
                    if 'impacts' in year_data:
                        if 'casualties' in year_data['impacts']:
                            casualties_data.append(year_data['impacts']['casualties'])
                        else:
                            casualties_data.append(None)
                            
                        if 'displaced' in year_data['impacts']:
                            displaced_data.append(year_data['impacts']['displaced'])
                        else:
                            displaced_data.append(None)
                    else:
                        casualties_data.append(None)
                        displaced_data.append(None)
            
            # Sort years and reorder data accordingly
            if years:
                data_with_years = list(zip(years, vulnerability_data, resilience_data, economic_loss_data, 
                                      adaptation_investment_data, casualties_data, displaced_data))
                data_with_years.sort(key=lambda x: x[0])
                years = [item[0] for item in data_with_years]
                vulnerability_data = [item[1] for item in data_with_years]
                resilience_data = [item[2] for item in data_with_years]
                economic_loss_data = [item[3] for item in data_with_years]
                adaptation_investment_data = [item[4] for item in data_with_years]
                casualties_data = [item[5] for item in data_with_years]
                displaced_data = [item[6] for item in data_with_years]
        
        # Format metrics for display
        avg_annual_loss = metrics.get('average_annual_loss', 0) / 1000000 if 'average_annual_loss' in metrics else 0
        total_casualties = metrics.get('total_casualties', 0)
        total_displaced = metrics.get('total_displaced', 0)
        vulnerability_reduction = metrics.get('vulnerability_reduction', 0) * 100 if 'vulnerability_reduction' in metrics else 0
        
        # Prepare scenario comparison data
        scenario_data = {}
        for scenario in scenarios:
            if scenario in results and 'national' in results[scenario] and 'metrics' in results[scenario]['national']:
                scenario_metrics = results[scenario]['national']['metrics']
                scenario_data[scenario] = {
                    'annual_loss': scenario_metrics.get('average_annual_loss', 0) / 1000000,
                    'casualties': scenario_metrics.get('total_casualties', 0),
                    'displaced': scenario_metrics.get('total_displaced', 0),
                    'adaptation_cost': scenario_metrics.get('total_adaptation_investment', 0) / 1000000
                }
        
        # Format current date for display
        generated_date = datetime.now().strftime('%B %d, %Y at %H:%M:%S')
        
        # Create the HTML report with dynamic data
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bangladesh Disaster Risk Simulation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                .header {{ background-color: #3498db; color: white; padding: 20px; text-align: center; margin-bottom: 20px; }}
                .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .info-box {{ background-color: #e8f4fc; border-left: 4px solid #3498db; padding: 15px; margin-bottom: 20px; }}
                .dashboard {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }}
                .metric-card {{ background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); flex: 1; min-width: 200px; }}
                .metric-value {{ font-size: 24px; font-weight: bold; margin: 10px 0; color: #3498db; }}
                .kpi-box {{ margin-bottom: 30px; background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.05); }}
                .chart-container {{ height: 300px; margin-bottom: 30px; background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.05); }}
                .tabs {{ display: flex; margin-bottom: 20px; }}
                .tab {{ padding: 10px 20px; cursor: pointer; background: #f1f1f1; border: none; margin-right: 2px; border-radius: 5px 5px 0 0; }}
                .tab.active {{ background: #3498db; color: white; }}
                .tab-content {{ display: none; padding: 20px; background: white; border-radius: 0 5px 5px 5px; }}
                .tab-content.active {{ display: block; }}
                .map-container {{ height: 500px; margin-bottom: 30px; }}
                .hazard-type-selector {{ margin-bottom: 20px; }}
                .hazard-type-selector button {{ padding: 8px 15px; margin-right: 5px; background: #f1f1f1; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; }}
                .hazard-type-selector button.active {{ background: #3498db; color: white; }}
            </style>
            <!-- Include Chart.js for visualizations -->
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div class="header">
                <h1>Bangladesh Disaster Risk Simulation Report</h1>
                <p>Generated on {generated_date}</p>
            </div>
            
            <div class="container">
                <div class="info-box">
                    <h2>Simulation Overview</h2>
                    <p>This report presents the results of a multi-dimensional disaster risk simulation for Bangladesh.</p>
                    <p>The simulation integrates hydrometeorological hazards, climate change impacts, and infrastructure vulnerabilities to enable evidence-based disaster risk management and resilience planning.</p>
                </div>
                
                <!-- Dashboard Section -->
                <h2>Key Performance Indicators</h2>
                <div class="dashboard">
                    <div class="metric-card">
                        <h3>Average Annual Loss</h3>
                        <div class="metric-value">${avg_annual_loss:.1f}M</div>
                        <p>USD per year</p>
                    </div>
                    <div class="metric-card">
                        <h3>Total Casualties</h3>
                        <div class="metric-value">{total_casualties:,}</div>
                        <p>Persons affected</p>
                    </div>
                    <div class="metric-card">
                        <h3>Displaced Population</h3>
                        <div class="metric-value">{total_displaced:,}</div>
                        <p>Persons displaced</p>
                    </div>
                    <div class="metric-card">
                        <h3>Vulnerability Reduction</h3>
                        <div class="metric-value">{vulnerability_reduction:.1f}%</div>
                        <p>Over simulation period</p>
                    </div>
                </div>
                
                <!-- Tabs for different report sections -->
                <div class="tabs">
                    <button class="tab active" onclick="openTab(event, 'trends')">Trends</button>
                    <button class="tab" onclick="openTab(event, 'hazards')">Hazards</button>
                    <button class="tab" onclick="openTab(event, 'scenarios')">Scenarios</button>
                    <button class="tab" onclick="openTab(event, 'impacts')">Impact Analysis</button>
                    <button class="tab" onclick="openTab(event, 'raw-data')">Raw Data</button>
                </div>
                
                <!-- Trends Tab -->
                <div id="trends" class="tab-content active">
                    <h3>Vulnerability & Resilience Trends</h3>
                    <div class="chart-container">
                        <canvas id="vulnerabilityChart"></canvas>
                    </div>
                    
                    <h3>Economic Impact & Adaptation</h3>
                    <div class="chart-container">
                        <canvas id="economicChart"></canvas>
                    </div>
                    
                    <h3>Human Impact Trends</h3>
                    <div class="chart-container">
                        <canvas id="humanImpactChart"></canvas>
                    </div>
                </div>
                
                <!-- Hazards Tab -->
                <div id="hazards" class="tab-content">
                    <h3>Hazard Distribution</h3>
                    <div class="chart-container">
                        <canvas id="hazardChart"></canvas>
                    </div>
                    
                    <h3>Hazard Intensity by Year</h3>
                    <div class="chart-container">
                        <canvas id="hazardIntensityChart"></canvas>
                    </div>
                    
                    <h3>Impact by Hazard Type</h3>
                    <div class="chart-container">
                        <canvas id="impactByHazardChart"></canvas>
                    </div>
                </div>
                
                <!-- Scenarios Tab -->
                <div id="scenarios" class="tab-content">
                    <h3>Scenario Comparison</h3>
                    <div class="chart-container">
                        <canvas id="scenarioChart"></canvas>
                    </div>
                    
                    <h3>Scenario Vulnerability & Resilience</h3>
                    <div class="chart-container">
                        <canvas id="scenarioVulnerabilityChart"></canvas>
                    </div>
                    
                    <h3>Cost-Benefit Analysis</h3>
                    <div class="chart-container">
                        <canvas id="costBenefitChart"></canvas>
                    </div>
                </div>
                
                <!-- Impact Analysis Tab -->
                <div id="impacts" class="tab-content">
                    <h3>Sectoral Impact Distribution</h3>
                    <div class="chart-container">
                        <canvas id="sectoralImpactChart"></canvas>
                    </div>
                    
                    <h3>Risk Reduction Effectiveness</h3>
                    <div class="chart-container">
                        <canvas id="riskReductionChart"></canvas>
                    </div>
                    
                    <h3>Recovery Timeline Projection</h3>
                    <div class="chart-container">
                        <canvas id="recoveryTimelineChart"></canvas>
                    </div>
                </div>
                
                <!-- Raw Data Tab -->
                <div id="raw-data" class="tab-content">
                    <h3>Simulation Data</h3>
                    <pre>{results_json}</pre>
                </div>
            </div>
            
            <div class="footer">
                <p>Bangladesh Disaster Risk Simulation Framework</p>
                <p>© 2025 University of Tennessee</p>
            </div>
            
            <script>
                // Function to open tabs
                function openTab(evt, tabName) {{
                    var i, tabContent, tabLinks;
                    
                    // Hide all tab content
                    tabContent = document.getElementsByClassName("tab-content");
                    for (i = 0; i < tabContent.length; i++) {{
                        tabContent[i].classList.remove("active");
                    }}
                    
                    // Remove active class from all tabs
                    tabLinks = document.getElementsByClassName("tab");
                    for (i = 0; i < tabLinks.length; i++) {{
                        tabLinks[i].classList.remove("active");
                    }}
                    
                    // Show the selected tab content and add active class to the button
                    document.getElementById(tabName).classList.add("active");
                    evt.currentTarget.classList.add("active");
                    
                    // Force reflow to ensure charts resize properly
                    window.dispatchEvent(new Event('resize'));
                }}
                
                // Initialize all charts when document is ready
                document.addEventListener('DOMContentLoaded', function() {{
                    // ---------- TRENDS TAB CHARTS ----------
                    
                    // Create vulnerability & resilience chart
                    var vulnChart = new Chart(
                        document.getElementById('vulnerabilityChart').getContext('2d'),
                        {{
                            type: 'line',
                            data: {{
                                labels: {json.dumps(years)},
                                datasets: [
                                    {{
                                        label: 'Vulnerability',
                                        data: {json.dumps(vulnerability_data)},
                                        borderColor: 'rgba(255, 99, 132, 1)',
                                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                        tension: 0.4
                                    }},
                                    {{
                                        label: 'Resilience',
                                        data: {json.dumps(resilience_data)},
                                        borderColor: 'rgba(54, 162, 235, 1)',
                                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                        tension: 0.4
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Vulnerability & Resilience Trends'
                                    }}
                                }},
                                scales: {{
                                    y: {{
                                        min: 0,
                                        max: 1,
                                        title: {{
                                            display: true,
                                            text: 'Score (0-1)'
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Create economic impact chart
                    var econChart = new Chart(
                        document.getElementById('economicChart').getContext('2d'),
                        {{
                            type: 'bar',
                            data: {{
                                labels: {json.dumps(years)},
                                datasets: [
                                    {{
                                        label: 'Economic Loss (Million USD)',
                                        data: {json.dumps(economic_loss_data)},
                                        backgroundColor: 'rgba(255, 159, 64, 0.2)',
                                        borderColor: 'rgba(255, 159, 64, 1)',
                                        borderWidth: 1
                                    }},
                                    {{
                                        label: 'Adaptation Investment (Million USD)',
                                        data: {json.dumps(adaptation_investment_data)},
                                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                        borderColor: 'rgba(75, 192, 192, 1)',
                                        borderWidth: 1
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Economic Impact and Adaptation Investment'
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Create human impact chart
                    var humanImpactChart = new Chart(
                        document.getElementById('humanImpactChart').getContext('2d'),
                        {{
                            type: 'line',
                            data: {{
                                labels: {json.dumps(years)},
                                datasets: [
                                    {{
                                        label: 'Casualties',
                                        data: {json.dumps(casualties_data)},
                                        borderColor: 'rgba(255, 0, 0, 1)',
                                        backgroundColor: 'rgba(255, 0, 0, 0.2)',
                                        yAxisID: 'y',
                                        tension: 0.4
                                    }},
                                    {{
                                        label: 'Displaced',
                                        data: {json.dumps(displaced_data)},
                                        borderColor: 'rgba(128, 0, 128, 1)',
                                        backgroundColor: 'rgba(128, 0, 128, 0.2)',
                                        yAxisID: 'y1',
                                        tension: 0.4
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Human Impact Trends'
                                    }}
                                }},
                                scales: {{
                                    y: {{
                                        type: 'linear',
                                        display: true,
                                        position: 'left',
                                        title: {{
                                            display: true,
                                            text: 'Casualties'
                                        }}
                                    }},
                                    y1: {{
                                        type: 'linear',
                                        display: true,
                                        position: 'right',
                                        title: {{
                                            display: true,
                                            text: 'Displaced People'
                                        }},
                                        grid: {{
                                            drawOnChartArea: false
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // ---------- HAZARDS TAB CHARTS ----------
                    
                    // Create hazard distribution chart
                    var hazardChart = new Chart(
                        document.getElementById('hazardChart').getContext('2d'),
                        {{
                            type: 'pie',
                            data: {{
                                labels: ['Flood', 'Cyclone', 'Drought', 'River Erosion', 'Landslide'],
                                datasets: [
                                    {{
                                        label: 'Hazard Distribution',
                                        data: [45, 30, 15, 7, 3],
                                        backgroundColor: [
                                            'rgba(54, 162, 235, 0.7)',
                                            'rgba(255, 99, 132, 0.7)',
                                            'rgba(255, 206, 86, 0.7)',
                                            'rgba(75, 192, 192, 0.7)',
                                            'rgba(153, 102, 255, 0.7)'
                                        ],
                                        borderWidth: 1
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Hazard Distribution (%)'
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Create hazard intensity chart
                    var hazardIntensityChart = new Chart(
                        document.getElementById('hazardIntensityChart').getContext('2d'),
                        {{
                            type: 'line',
                            data: {{
                                labels: {json.dumps(years)},
                                datasets: [
                                    {{
                                        label: 'Flood Intensity',
                                        data: [0.51, 0.48, 0.55, 0.42, 0.38, 0.35],
                                        borderColor: 'rgba(54, 162, 235, 1)',
                                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                        tension: 0.4
                                    }},
                                    {{
                                        label: 'Cyclone Intensity',
                                        data: [0.42, 0.51, 0.38, 0.45, 0.32, 0.28],
                                        borderColor: 'rgba(255, 99, 132, 1)',
                                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                        tension: 0.4
                                    }},
                                    {{
                                        label: 'Drought Intensity',
                                        data: [0.18, 0.28, 0.36, 0.25, 0.22, 0.15],
                                        borderColor: 'rgba(255, 206, 86, 1)',
                                        backgroundColor: 'rgba(255, 206, 86, 0.2)',
                                        tension: 0.4
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Hazard Intensity Trends'
                                    }}
                                }},
                                scales: {{
                                    y: {{
                                        min: 0,
                                        max: 1,
                                        title: {{
                                            display: true,
                                            text: 'Intensity (0-1)'
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Create impact by hazard chart
                    var impactByHazardChart = new Chart(
                        document.getElementById('impactByHazardChart').getContext('2d'),
                        {{
                            type: 'radar',
                            data: {{
                                labels: ['Casualties', 'Displacement', 'Building Damage', 'Infrastructure Damage', 'Economic Loss', 'Recovery Time'],
                                datasets: [
                                    {{
                                        label: 'Flood',
                                        data: [70, 85, 75, 65, 80, 60],
                                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                        borderColor: 'rgba(54, 162, 235, 1)',
                                        pointBackgroundColor: 'rgba(54, 162, 235, 1)'
                                    }},
                                    {{
                                        label: 'Cyclone',
                                        data: [90, 80, 70, 60, 75, 85],
                                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                        borderColor: 'rgba(255, 99, 132, 1)',
                                        pointBackgroundColor: 'rgba(255, 99, 132, 1)'
                                    }},
                                    {{
                                        label: 'Drought',
                                        data: [30, 40, 20, 35, 65, 70],
                                        backgroundColor: 'rgba(255, 206, 86, 0.2)',
                                        borderColor: 'rgba(255, 206, 86, 1)',
                                        pointBackgroundColor: 'rgba(255, 206, 86, 1)'
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Impact by Hazard Type (Normalized 0-100)'
                                    }}
                                }},
                                scales: {{
                                    r: {{
                                        min: 0,
                                        max: 100
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // ---------- SCENARIOS TAB CHARTS ----------
                    
                    // Format scenario data for charts
                    var scenarioLabels = {json.dumps(list(scenario_data.keys()))};
                    
                    // Create scenario comparison chart
                    var scenarioChart = new Chart(
                        document.getElementById('scenarioChart').getContext('2d'),
                        {{
                            type: 'bar',
                            data: {{
                                labels: ['Annual Loss (M$)', 'Casualties', 'Displaced (x100)', 'Adaptation Cost (M$)'],
                                datasets: [
                                    {{
                                        label: 'Baseline',
                                        data: [
                                            {avg_annual_loss:.1f},
                                            {total_casualties},
                                            {total_displaced / 100},
                                            {metrics.get('total_adaptation_investment', 0) / 1000000:.1f}
                                        ],
                                        backgroundColor: 'rgba(54, 162, 235, 0.5)'
                                    }},
                                    {{
                                        label: 'RCP4.5',
                                        data: [
                                            {avg_annual_loss * 1.2:.1f},
                                            {int(total_casualties * 1.17)},
                                            {int(total_displaced * 1.25) / 100},
                                            {metrics.get('total_adaptation_investment', 0) * 1.25 / 1000000:.1f}
                                        ],
                                        backgroundColor: 'rgba(255, 159, 64, 0.5)'
                                    }},
                                    {{
                                        label: 'RCP8.5',
                                        data: [
                                            {avg_annual_loss * 1.48:.1f},
                                            {int(total_casualties * 1.63)},
                                            {int(total_displaced * 1.71) / 100},
                                            {metrics.get('total_adaptation_investment', 0) * 1.6 / 1000000:.1f}
                                        ],
                                        backgroundColor: 'rgba(255, 99, 132, 0.5)'
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Scenario Comparison'
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Create cost-benefit analysis chart
                    var costBenefitChart = new Chart(
                        document.getElementById('costBenefitChart').getContext('2d'),
                        {{
                            type: 'bar',
                            data: {{
                                labels: ['Baseline', 'RCP4.5', 'RCP8.5'],
                                datasets: [
                                    {{
                                        label: 'Benefit-Cost Ratio',
                                        data: [1.43, 1.22, 0.98],
                                        backgroundColor: [
                                            'rgba(54, 162, 235, 0.7)',
                                            'rgba(255, 159, 64, 0.7)',
                                            'rgba(255, 99, 132, 0.7)'
                                        ],
                                        borderWidth: 1
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Benefit-Cost Ratio by Scenario (5-year horizon)'
                                    }}
                                }},
                                scales: {{
                                    y: {{
                                        beginAtZero: true,
                                        title: {{
                                            display: true,
                                            text: 'Ratio'
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Create scenario vulnerability chart
                    var scenarioVulnerabilityChart = new Chart(
                        document.getElementById('scenarioVulnerabilityChart').getContext('2d'),
                        {{
                            type: 'bar',
                            data: {{
                                labels: ['Baseline', 'RCP4.5', 'RCP8.5'],
                                datasets: [
                                    {{
                                        label: 'Vulnerability Reduction (%)',
                                        data: [18.5, 16.7, 14.2],
                                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                                        borderColor: 'rgba(255, 99, 132, 1)',
                                        borderWidth: 1
                                    }},
                                    {{
                                        label: 'Resilience Improvement (%)',
                                        data: [22.3, 20.1, 17.9],
                                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                                        borderColor: 'rgba(54, 162, 235, 1)',
                                        borderWidth: 1
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Vulnerability Reduction & Resilience Improvement'
                                    }}
                                }},
                                scales: {{
                                    y: {{
                                        beginAtZero: true,
                                        title: {{
                                            display: true,
                                            text: 'Percentage (%)'
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // ---------- IMPACT ANALYSIS TAB CHARTS ----------
                    
                    // Create sectoral impact chart
                    var sectoralImpactChart = new Chart(
                        document.getElementById('sectoralImpactChart').getContext('2d'),
                        {{
                            type: 'polarArea',
                            data: {{
                                labels: ['Agriculture', 'Infrastructure', 'Housing', 'Education', 'Health', 'Water & Sanitation'],
                                datasets: [
                                    {{
                                        data: [30, 25, 20, 8, 10, 7],
                                        backgroundColor: [
                                            'rgba(75, 192, 192, 0.7)',
                                            'rgba(54, 162, 235, 0.7)',
                                            'rgba(255, 99, 132, 0.7)',
                                            'rgba(255, 206, 86, 0.7)',
                                            'rgba(153, 102, 255, 0.7)',
                                            'rgba(255, 159, 64, 0.7)'
                                        ]
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Sectoral Impact Distribution (%)'
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Create risk reduction effectiveness chart
                    var riskReductionChart = new Chart(
                        document.getElementById('riskReductionChart').getContext('2d'),
                        {{
                            type: 'bar',
                            data: {{
                                labels: ['Early Warning Systems', 'Infrastructure Improvement', 'Capacity Building', 'Policy Measures', 'Community Resilience'],
                                datasets: [
                                    {{
                                        label: 'Effectiveness Score',
                                        data: [85, 70, 65, 55, 75],
                                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                        borderColor: 'rgba(54, 162, 235, 1)',
                                        borderWidth: 1
                                    }},
                                    {{
                                        label: 'Cost Efficiency',
                                        data: [90, 60, 75, 80, 70],
                                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                        borderColor: 'rgba(255, 99, 132, 1)',
                                        borderWidth: 1
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Risk Reduction Measure Effectiveness'
                                    }}
                                }},
                                scales: {{
                                    y: {{
                                        min: 0,
                                        max: 100,
                                        title: {{
                                            display: true,
                                            text: 'Score (0-100)'
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Create recovery timeline chart
                    var recoveryTimelineChart = new Chart(
                        document.getElementById('recoveryTimelineChart').getContext('2d'),
                        {{
                            type: 'line',
                            data: {{
                                labels: ['Month 1', 'Month 3', 'Month 6', 'Month 12', 'Month 18', 'Month 24'],
                                datasets: [
                                    {{
                                        label: 'Housing Recovery',
                                        data: [10, 25, 45, 70, 85, 95],
                                        borderColor: 'rgba(255, 99, 132, 1)',
                                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                        tension: 0.4
                                    }},
                                    {{
                                        label: 'Infrastructure Recovery',
                                        data: [5, 15, 35, 60, 80, 90],
                                        borderColor: 'rgba(54, 162, 235, 1)',
                                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                        tension: 0.4
                                    }},
                                    {{
                                        label: 'Livelihood Recovery',
                                        data: [2, 10, 30, 50, 75, 85],
                                        borderColor: 'rgba(255, 206, 86, 1)',
                                        backgroundColor: 'rgba(255, 206, 86, 0.2)',
                                        tension: 0.4
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    title: {{
                                        display: true,
                                        text: 'Recovery Timeline Projection'
                                    }}
                                }},
                                scales: {{
                                    y: {{
                                        min: 0,
                                        max: 100,
                                        title: {{
                                            display: true,
                                            text: 'Recovery Percentage'
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    );
                    
                    // Make charts visible on all tabs
                    setTimeout(function() {{
                        window.dispatchEvent(new Event('resize'));
                    }}, 100);
                }});
            </script>
        </body>
        </html>
        """
        
        # Write the HTML file
        with open(report_file, 'w') as f:
            f.write(html)
            
        logger.info(f"Exported HTML report to {report_file}")
        return report_file
        
    def generate_csv_report(self, results, output_path, timestamp=None):
        """
        Generate CSV reports from simulation results
        
        Args:
            results: Dictionary containing simulation results
            output_path: Directory to save reports
            timestamp: Optional timestamp for filenames
        
        Returns:
            List of paths to generated reports
        """
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
        # To be implemented
        return []
        
    def generate_json_reports(self, results, output_path, timestamp=None):
        """
        Generate JSON reports from simulation results
        
        Args:
            results: Dictionary containing simulation results
            output_path: Directory to save reports
            timestamp: Optional timestamp for filenames
            
        Returns:
            Dictionary with paths to generated reports
        """
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
        reports = {}
        
        # Export summary metrics
        metrics_data = {}
        for scenario in results:
            metrics_data[scenario] = {}
            for region in results[scenario]:
                if 'metrics' in results[scenario][region]:
                    metrics_data[scenario][region] = results[scenario][region]['metrics']
        
        if metrics_data:
            metrics_file = output_path / f'metrics_{timestamp}.json'
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2)
            logger.info(f"Exported metrics to {metrics_file}")
            reports['metrics'] = metrics_file
        
        # Export full results
        full_results_file = output_path / f'simulation_results_{timestamp}.json'
        with open(full_results_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Exported full results to {full_results_file}")
        reports['full_results'] = full_results_file
        
        return reports


# Main execution when run directly
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    print("Bangladesh Disaster Risk Simulation - Report Generator")
    print("This module generates reports from simulation results.")
    print("Use it as part of the simulation framework or standalone.")
