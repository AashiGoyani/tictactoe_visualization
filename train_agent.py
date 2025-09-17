import pickle
import argparse
from game_engine import Agent, PLAYER_O, PLAYER_X

def train_and_save_agent(episodes=100000):
    print("Training agents with more exploration...")
    
    # Create two agents for self-play training
    p1 = Agent(PLAYER_X, lossval=-1)
    p2 = Agent(PLAYER_O, lossval=-1)
    
    # Increase exploration initially
    p1.epsilon = 0.3  # More exploration
    p2.epsilon = 0.3
    
    # Train through self-play
    for i in range(episodes):  # More training games
        if i % 10000 == 0:
            print(f'Training game: {i}')

        # Gradually reduce exploration
        if i > 50000:
            p1.epsilon = max(0.1, p1.epsilon * 0.99)
            p2.epsilon = max(0.1, p2.epsilon * 0.99)
        
        # Play a game between the two agents
        from game_engine import play
        winner = play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)
    
    # Save the trained agent values
    with open('trained_agent_values.pkl', 'wb') as f:
        pickle.dump(p2.values, f)
    
    print(f"Training complete! Agent has {len(p2.values)} learned states.")
    print(f"Final epsilon: {p2.epsilon:.3f}")
    print("Saved to 'trained_agent_values.pkl'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a tic-tac-toe AI agent')
    parser.add_argument('--episodes', type=int, default=100000,
                        help='Number of training episodes (default: 100000)')

    args = parser.parse_args()
    train_and_save_agent(args.episodes)