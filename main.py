from model.falling_bird_env import *

env = FallingBird(randomPositions=True, FPS=500)
model = PPO('MlpPolicy', env, verbose=1)
env.render_mode = 'human'  # If you want to see the games


# env.render_mode = None - If just want to train the model

def create_and_save_model(version, FPS=500):
    new_model_path = os.path.join('trained_models', 'Saved_models_v' + str(version))
    model.learn(total_timesteps=FPS * 10)
    model.save(new_model_path)


def load_and_test_model(version, env, lib):
    path = os.path.join('trained_models', 'Saved_models_v' + str(version))
    model = lib.load(path, env=env)
    obs = env.reset()  # Zresetuj środowisko
    done = False
    while not done:
        action, _ = model.predict(obs)  # Wygeneruj akcję na podstawie obserwacji
        obs, reward, done, info = env.step(action)  # Wykonaj akcję w środowisku
        env.render()  # Wyświetl środowisko


#create_and_save_model(version=4)
#for i in range(5):
#    load_and_test_model(3, env, PPO)

# TODO:
#  1. Try to create selfmade models and test them
#  2. Try to change rewards system
#  3. Print part exists in update_gamestate()
#  4. Try to bind q key press event to stop learning model
