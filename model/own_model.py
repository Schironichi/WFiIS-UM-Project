# from utils.imports import Adam
# from utils.imports import Sequential
# from utils.imports import Dense, Flatten
# from utils.imports import DQNAgent
# from utils.imports import BoltzmannQPolicy
# from utils.imports import SequentialMemory
#  MODEL PART  #
"""
states = env.observation_space.shape
actions = env.action_space.n

print(states, actions)
def buildModel(states, actions):
    model = Sequential()
    model.add(Flatten(input_shape=states))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model

model = buildModel(states, actions)



print(model.summary())


#  AGENT PART  #

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=actions, nb_steps_warmup=10,
                   target_model_update=1e-2)
    return dqn


DQN = build_agent(model, actions)
DQN.compile(Adam(lr=1e-3), metrics=['mae'])
DQN.fit(env, nb_steps=50000, visualize=False, verbose=1)

"""