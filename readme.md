# Chicken Social Network Simulation

## Overview

This project is an agent-based simulation developed for the course **"Applied Network Science: Animal Social Networks"**. The simulation addresses a key question in animal behavior research: whether social relationships in chickens can be detected through proximity data, even when they exist.

Inspired by the paper **"Do laying hens form stable social networks? A case study"**, this simulation demonstrates that even when chickens have clear social relationships (friendships and enmities), these relationships may not be detectable with limited observational data points - mirroring real-world research constraints.

## Research Question

The simulation tests whether social network structures can be reliably detected from proximity-based interaction data, particularly when:
- Data collection periods are limited
- Chickens have underlying social preferences (friends/enemies)
- Environmental factors (food, water, dust baths) influence movement patterns

## How It Works

### Chicken Types
The simulation includes three types of chickens with different behavioral models:

1. **RandomChicken**: Moves completely randomly around the cage
2. **WeightedRandomChicken**: Motivated by resources (food, water, dust baths) and avoids recently visited locations, but has no social preferences
3. **FollowerChicken**: Motivated by resources, location memory, AND social relationships - will seek out friends and avoid enemies

### Data Generation
The simulation generates an **adjacency matrix** where entry (i,j) represents the percentage of time chicken i spent near chicken j out of all the time chicken i was interacting with others. This mirrors real-world data collection methods used in animal behavior studies.

### Social Relationship Assignment
When using FollowerChickens, the simulation creates realistic social structures:
- Mutual friendships and enmities
- Complex relationships (e.g., one-way friendships, bullying dynamics)
- Varying levels of sociability among individuals
- Two modes: random social networks or even/odd group-based relationships

## Installation & Setup

### Requirements
- Python 3.7 or higher
- Required packages:
```bash
pip install numpy matplotlib networkx pandas seaborn pygame
```

### Running the Simulation
```bash
python main.py
```

## Configuration

### Key Parameters
The simulation parameters are set to match the original study conditions:

```python
HEIGHT = 10          # Cage height (grid units)
WIDTH = 18           # Cage width (grid units)  
N_CHICKEN = 20       # Number of chickens (matches study)
N_STEPS = 1800       # Simulation steps
INTERVAL = 10        # Data collection interval
USE_FOLLOWER_CHICKENS = True  # Enable social relationships
GROUPS = False       # Use random vs. group-based social structure
```

### Behavioral Parameters (Advanced)
Each chicken type has internal parameters that affect behavior:

**All Chickens:**
- `food`, `water`, `clean`: Internal need levels (0-100+)
- Energy consumption rates: food (-0.8/step), water (-1.0/step), cleanliness (-0.1/step)

**WeightedRandomChicken & FollowerChicken:**
- `memory_decay = 100`: How quickly chickens "forget" visited locations
- Resource attraction weights: hunger (7.0), thirst (8.0), cleanliness (1.0)

**FollowerChicken Social Parameters:**
- `friend_attraction = 2.5`: Strength of attraction to friends
- `enemy_repulsion = 3.0`: Strength of avoidance of enemies  
- `social_distance_factor = 5.0`: How quickly social effects decay with distance

### Behavioral Modes
- Set `USE_FOLLOWER_CHICKENS = False` for RandomChicken movement (purely random)
- Set `USE_FOLLOWER_CHICKENS = True` for FollowerChicken behavior (resource + social motivated)
- Set `GROUPS = True` for even/odd group-based social relationships
- Set `VISUAL = True` to enable pygame real-time visualization (slower but useful for debugging)

**Note**: The simulation uses FollowerChickens by default. To test WeightedRandomChicken behavior, you would need to modify the chicken creation code in `run_simulation()`.

## Output & Analysis

### Generated Data
The simulation produces several types of output:

1. **Real-time Visualization**: Pygame-based grid showing chickens moving in real-time (for debugging and demonstration)
2. **Adjacency Matrices**: Time-series of interaction matrices collected every `INTERVAL` steps
3. **Average Adjacency Matrix**: Overall interaction patterns across the entire simulation
4. **Custom Network Analysis**: Graph representations and clustering analysis built from adjacency matrices
5. **Temporal Analysis**: Week-by-week interaction patterns

### Interpreting Results
- **High adjacency values**: Chickens spending significant time together
- **Network clusters**: Potential social groups or resource-based gatherings
- **Temporal stability**: Whether relationships persist over time
- **Comparison between modes**: How social motivations affect detectable network patterns

The key insight is that even when FollowerChickens have clear friend/enemy relationships programmed into them, these may not be clearly visible in the resulting adjacency matrices - demonstrating that **the original study likely didn't have sufficient data points to conclude that chickens don't form social groups**. The absence of detectable social structure doesn't necessarily mean social relationships don't exist.

## Project Structure
```
├── main.py              # Main simulation script
├── requirements.txt     # Python dependencies
├── img/                 # Generated visualizations
├── src/
│   ├── Cage.py         # Cage environment and simulation logic
│   ├── Chicken.py      # Chicken behavior classes (RandomChicken, FollowerChicken, etc.)
│   ├── Bath.py         # Bathing area objects
│   ├── Consumable.py   # Food and water resources
│   ├── Food.py         # Food source objects
│   ├── GridObject.py   # Base grid object class
│   ├── Water.py        # Water source objects  
│   └── utils.py        # Analysis and visualization utilities
└── README.md           # This file
```

## Academic Context

This simulation demonstrates important methodological considerations in animal behavior research:
- The difficulty of inferring social relationships from spatial proximity data
- The impact of environmental factors on apparent social networks
- The importance of sufficient data collection periods
- The challenge of distinguishing between resource-driven and socially-driven interactions

## Usage Examples

### Basic Simulation (Resource-motivated only)
```python
python main.py
# Set USE_FOLLOWER_CHICKENS = False in the script
```

### Social Network Simulation
```python
python main.py  
# Set USE_FOLLOWER_CHICKENS = True in the script
```

### Group-based Social Structure
```python
python main.py
# Set GROUPS = True for even/odd chicken groupings
```

## Expected Runtime
- Standard simulation: ~30 seconds to 2 minutes depending on visualization settings
- With visual display enabled: Significantly longer
- Data collection occurs every 10 steps by default

## Troubleshooting

If you encounter import errors, ensure all required packages are installed:
```bash
pip install --upgrade numpy matplotlib networkx pandas seaborn
```

For visualization issues, try setting `VISUAL = False` in main.py to disable real-time graphics.

---

*This project was developed for academic purposes to explore the challenges of detecting animal social networks through observational data.*

