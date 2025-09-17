import pickle
import sys
sys.path.append('.')
from og import Agent, PLAYER_O, PLAYER_X, play

def train_with_original_method():
    print("Training using original og.py method...")
    
    # Use the exact same training as og.py
    p1 = Agent(PLAYER_X, lossval=-1)
    p2 = Agent(PLAYER_O, lossval=-1)
    
    # Train for many games
    for i in range(50000):
        if i % 5000 == 0:
            print(f'Training game: {i}')
        
        winner = play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)
    
    # Save the trained P2 (PLAYER_O) agent values
    with open('trained_agent_values.pkl', 'wb') as f:
        pickle.dump(p2.values, f)
    
    print(f"Training complete! Agent has {len(p2.values)} learned states.")
    
    # Show some example values
    print("\nSample learned values:")
    count = 0
    for state, value in list(p2.values.items())[:20]:
        print(f"State: {state} -> Value: {value:.4f}")
        count += 1
        if count >= 10:
            break

if __name__ == "__main__":
    train_with_original_method()