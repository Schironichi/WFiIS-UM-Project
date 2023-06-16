from model.falling_bird_env import *

env = FallingBird(randomPositions=True, FPS=500)
model = PPO('MlpPolicy', env, verbose=1)
env.render_mode = 'human'  # If you want to see the games


#env.render_mode = None # - If just want to train the model

def create_and_save_model(version, FPS=500):
    mean_rewards = []
    episodes = []
    new_model_path = os.path.join('trained_models', 'Saved_models_v' + str(version))
    for episode in range(3):
        # Trening modelu przez jeden epizod
        model.learn(total_timesteps=FPS * 10)

        # Ocena modelu po każdym epizodzie
        mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=10)

        # Zapisanie metryk
        mean_rewards.append(mean_reward)
        episodes.append(episode)
    model.save(new_model_path)
    plt.plot(episodes, mean_rewards)
    plt.xlabel('Episodes')
    plt.ylabel('Mean Rewards')
    plt.title('Learning Curve')
    plt.savefig('learning_curve.png')
    plt.show()


def load_and_test_model(version, env, lib):
    path = os.path.join('trained_models', 'Saved_models_v' + str(version))
    model = lib.load(path, env=env)
    obs = env.reset()  # Zresetuj środowisko
    done = False
    while not done:
        action, _ = model.predict(obs)  # Wygeneruj akcję na podstawie obserwacji
        obs, reward, done, info = env.step(action)  # Wykonaj akcję w środowisku
        env.render()  # Wyświetl środowisko


#create_and_save_model(version=7)
for i in range(100):
    load_and_test_model(version=6, env=env, lib=PPO)
