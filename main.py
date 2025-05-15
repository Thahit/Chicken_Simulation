from src.Cage import Cage
from src.Chicken import RandomChicken
from src.Chicken import FollowerChicken
from src.utils import calculate_avg_adj_list, visualize_graph, read_all_weeks, create_graph_from_adj_matrix
import random
import numpy as np

def run_simulation(use_follower_chickens=False, height=8, width=12, n_chicken=20, analyze_only_chicken=False,
                   n_steps=1000, visual=False, adj_matrix_interval=5, pygames_grid=True, groups=False):
    """
    Run a chicken simulation with either RandomChickens or FollowerChickens.
    
    Args:
        use_follower_chickens: If True, use FollowerChickens with social relationships, else use RandomChickens
        height: Height of the cage
        width: Width of the cage
        n_chicken: Number of chickens to simulate
        analyze_only_chicken: If True, only analyze chicken relationships, ignore resources
        
    Returns:
        tuple: (avg_adj_list, names, df) - Results of the simulation
    """
    # Create an empty cage first
    cage = Cage(width=width, height=height, chickens=[], 
                food_positions=[(9, 4), (8, height-3)], 
                water_positions=[(width-3, height-4)], 
                bath_positions=[(width-7, 0),(width-6, 0),(width-5, 0)])
    
    # Create chickens based on the specified type with reference to the cage
    if use_follower_chickens:
        chickens = [FollowerChicken(random.randint(0, width-1), random.randint(0, height-1), cage) 
                    for _ in range(n_chicken)]
        
        # Assign social relationships
        if groups:
            assign_social_relationships_even_vs_odd(chickens)
        else:
            assign_social_relationships(chickens)
    else:
        chickens = [RandomChicken(random.randint(0, width-1), random.randint(0, height-1), cage) 
                    for _ in range(n_chicken)]
    
    # Add chickens to the cage
    cage.chickens = chickens
    #this fcks up the names....
    cage.all_object_names = [f"chicken_{i}" for i in range(len(cage.chickens))] + \
                [f"food_{i}" for i in range(len(cage.food_sources))] +   \
                [f"water_{i}" for i in range(len(cage.water_sources))] + \
                [f"bath_{i}" for i in range(len(cage.bathing_areas))]
    
    # Run simulation
    if pygames_grid:
        adj_lists = cage.simulate_visual(n_steps, adj_matrix_interval=adj_matrix_interval, visual=visual)
    else:
        adj_lists = cage.simulate(n_steps, adj_matrix_interval=5, visual=visual)
    
    # Process results
    avg_adj_list = calculate_avg_adj_list(adj_lists)
    names = cage.all_object_names
    
    print("Analysis")
    df = read_all_weeks(adj_lists, week_size=5)
     
    visualize_graph(avg_adj_list, names, min_weight=.11,
                    max_size=n_chicken if analyze_only_chicken else None)
    # Create graph visualization
    create_graph_from_adj_matrix(avg_adj_list, all_object_names=names, 
                              clustering_method='louvain', 
                              max_size=n_chicken if analyze_only_chicken else None)
    
    #find_roles(avg_adj_list, max_size=n_chicken if analyze_only_chicken else None)
    return avg_adj_list, names, df

def assign_social_relationships_even_vs_odd(chickens):
    """
    Assign friendships and enmities based on even and odd indices.

    Even-indexed chickens are friends with all other even-indexed chickens,
    and odd-indexed chickens are friends with all other odd-indexed chickens.
    Chickens at even indices and odd indices are enemies.

    Args:
        chickens: List of FollowerChicken instances
    """
    n_chicken = len(chickens)

    for i in range(n_chicken):
        if i % 2 == 0:
            for j in range(i + 1, n_chicken):
                if j % 2 == 0:  # Same parity, even index -> friendship
                    chickens[i].add_friend(chickens[j])
                    chickens[j].add_friend(chickens[i])  
        else:
            for j in range(i + 1, n_chicken):
                if j % 2 != 0:  
                    chickens[i].add_friend(chickens[j])
                    chickens[j].add_friend(chickens[i]) 
    
    for i in range(n_chicken):
        for j in range(i + 1, n_chicken):
            if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                chickens[i].add_enemy(chickens[j])
                chickens[j].add_enemy(chickens[i])  

    print("\nSocial Relationship Statistics:")
    friend_counts = [len(chicken.friends) for chicken in chickens]
    enemy_counts = [len(chicken.enemies) for chicken in chickens]
    for chicken_id in range(len(chickens)):
        print(f"Chicken {chickens[chicken_id].id} has friends: {[c.id for c in chickens[chicken_id].friends]} and enemies {[c.id for c in chickens[chicken_id].enemies]}")
    print(f"Average friends per chicken: {sum(friend_counts)/n_chicken:.2f}")
    print(f"Average enemies per chicken: {sum(enemy_counts)/n_chicken:.2f}")
    print(f"Most popular chicken has {max(friend_counts)} friends")
    print(f"Most hated chicken has {max(enemy_counts)} enemies")
    print(f"Most antisocial chicken has {min(friend_counts)} friends and {min(enemy_counts)} enemies")


def assign_social_relationships(chickens):
    """
    Intelligently assign friends and enemies among chickens.
    
    The assignment follows these principles:
    1. Mutual friendships are more likely than one-way friendships
    2. Each chicken gets a varying number of friends and enemies
    3. Chickens that are friends are less likely to be enemies
    4. Some chickens may be more popular (have more friends)
    5. Some chickens may be bullies (have friends who consider them enemies)
    
    Args:
        chickens: List of FollowerChicken instances
    """
    n_chicken = len(chickens)
    
    # Create a "personality matrix" that defines social tendencies
    # Higher values mean more likely to be friends
    personality_compatibility = np.random.normal(0.5, 0.25, (n_chicken, n_chicken))
    
    # Make it symmetric but with some noise (for mutual vs one-way friendships)
    for i in range(n_chicken):
        for j in range(i+1, n_chicken):
            avg = (personality_compatibility[i, j] + personality_compatibility[j, i]) / 2
            noise = np.random.normal(0, 0.1)
            personality_compatibility[i, j] = avg + noise
            personality_compatibility[j, i] = avg - noise
    
    # Set diagonal to 0 (chickens can't be friends/enemies with themselves)
    np.fill_diagonal(personality_compatibility, 0)
    
    # Create "popularity factor" for each chicken
    popularity = np.random.normal(1.0, 0.3, n_chicken)
    
    # Create "social nature" - how many relationships each chicken tends to form
    social_nature = np.random.normal(0.3, 0.1, n_chicken)
    
    # Create "friend or enemy threshold" - how likely a chicken forms friendships vs enmities
    friend_threshold = np.random.normal(0.5, 0.2, n_chicken)
    
    # Now assign relationships
    for i in range(n_chicken):
        # Determine number of relationships this chicken will form
        total_relationships = max(1, int(n_chicken * social_nature[i]))
        
        # Get compatibility scores with all other chickens
        compat_scores = personality_compatibility[i, :] * popularity
        
        # Sort chickens by compatibility
        chicken_indices = np.argsort(-compat_scores)  # Descending order
        
        # Skip self
        chicken_indices = chicken_indices[chicken_indices != i]
        
        # Select the top chickens to form relationships with
        relationship_indices = chicken_indices[:total_relationships]
        
        for j in relationship_indices:
            # Determine if this is a friendship or enmity
            # Higher compatibility and chicken's own threshold determines this
            relationship_score = compat_scores[j]
            
            if relationship_score > friend_threshold[i]:
                # Add as friend
                chickens[i].add_friend(chickens[j])
                
                # Create potential bullies - 10% chance that a chicken's "friend" actually considers them an enemy
                if random.random() < 0.1:
                    chickens[j].add_enemy(chickens[i])
                    # Print this interesting relationship
                    print(f"Bully detected: Chicken {j} is an enemy to Chicken {i}, but Chicken {i} considers Chicken {j} a friend!")
                
                # 70% chance of mutual friendship if i considers j a friend
                elif random.random() < 0.7:
                    chickens[j].add_friend(chickens[i])
                    # Small chance (5%) that despite mutual friendship, one still considers the other an enemy
                    if random.random() < 0.05:
                        chickens[j].add_enemy(chickens[i])
                        print(f"Complex relationship: Chickens {i} and {j} are friends, but {j} also considers {i} an enemy!")
            else:
                # Add as enemy
                chickens[i].add_enemy(chickens[j])
                
                # 30% chance of mutual enmity
                if random.random() < 0.3:
                    chickens[j].add_enemy(chickens[i])
    
    # Print relationship statistics
    print("\nSocial Relationship Statistics:")
    friend_counts = [len(chicken.friends) for chicken in chickens]
    enemy_counts = [len(chicken.enemies) for chicken in chickens]
    for chicken_id in range(len(chickens)):
        print(f"Chicken {chickens[chicken_id].id} has friends: {[c.id for c in chickens[chicken_id].friends]} and enemies {[c.id for c in chickens[chicken_id].enemies]}")
    print(f"Average friends per chicken: {sum(friend_counts)/n_chicken:.2f}")
    print(f"Average enemies per chicken: {sum(enemy_counts)/n_chicken:.2f}")
    print(f"Most popular chicken has {max(friend_counts)} friends")
    print(f"Most hated chicken has {max(enemy_counts)} enemies")
    print(f"Most antisocial chicken has {min(friend_counts)} friends and {min(enemy_counts)} enemies")


if __name__ == "__main__":
    seed = 0 
    random.seed(seed)
    np.random.seed(seed)

    # Parameters
    HEIGHT = 10
    WIDTH = 18
    N_CHICKEN = 20
    ANALYZE_ONLY_CHICKEN = False
    USE_FOLLOWER_CHICKENS = True  # Set to False to use the original RandomChicken behavior
    N_STEPS=1800 
    VISUAL = False
    INTERVAL = 10
    GROUPS = False
    print(f"Need {3*(60/5)*5=} observations and have {N_STEPS/INTERVAL=}")
    # Run the simulation
    avg_adj_list, names, df = run_simulation(
        use_follower_chickens=USE_FOLLOWER_CHICKENS,
        height=HEIGHT,
        width=WIDTH,
        n_chicken=N_CHICKEN,
        analyze_only_chicken=ANALYZE_ONLY_CHICKEN,
        n_steps = N_STEPS,
        visual=VISUAL,
        adj_matrix_interval= INTERVAL,
        groups=GROUPS,
    )
    
    