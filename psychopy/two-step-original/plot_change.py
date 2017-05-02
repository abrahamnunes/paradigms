import numpy as np
import matplotlib.pyplot as plt

np.random.seed(seed=15)

nsteps = 201
paths = np.zeros([nsteps, 2])
r = np.zeros([nsteps, 2])
paths[0,:] = np.array([0.6, 0.4])

for i in range(1, nsteps):
    dx = np.random.normal(loc=0, scale=1, size=2)
    paths[i,:] = np.maximum(np.minimum(paths[i-1] + 0.025*dx, 0.8), 0.1)

    r[i, 0] = np.random.binomial(1, p=paths[i, 0])
    r[i, 1] = np.random.binomial(1, p=paths[i, 1])



# STIM 1, 1 TRIAL
fig, ax = plt.subplots(figsize=(5,5))
ax.plot(np.arange(1), paths[:1, 0], c='b', lw=1.5)
ax.scatter(np.arange(1), paths[:1, 0], c='b', lw=1.5)

ax.set_ylabel('Chance of Winning')
ax.set_xlabel('Trial')
ax.set_ylim([0, 1])
ax.set_xlim([-0.1, 10])
plt.savefig('chances_1stim_trial1.png')


# STIM 1, 6 TRIAL
fig, ax = plt.subplots(figsize=(5,5))
ax.plot(np.arange(6), paths[:6, 0], c='b', lw=1.5)
ax.scatter(np.arange(6), paths[:6, 0], c='b', lw=1.5)

ax.set_ylabel('Chance of Winning')
ax.set_xlabel('Trial')
ax.set_ylim([0, 1])
ax.set_xlim([-0.1, 10])
plt.savefig('chances_1stim_trial6.png')

# STIM 1 60, Rewards
fig, ax = plt.subplots(figsize=(5,5))
ax.plot(np.arange(60), paths[:60, 0], c='b', lw=1.5)
ax.set_ylabel('Chance of Winning')
ax.set_xlabel('Trial')
ax.set_ylim([0, 1])
ax.set_xlim([-1, 60])
plt.savefig('chances_1stim_trial60.png')

# STIM 1 60, Rewards
fig, ax = plt.subplots(figsize=(5,5))
ax.plot(np.arange(60), paths[:60, 0], c='b', lw=1.5)
ax.scatter(np.arange(0, 60, 1), r[np.arange(0, 60, 1), 0]-0.1, c='k')
ax.set_ylabel('Chance of Winning')
ax.set_xlabel('Trial')
ax.set_ylim([0, 1])
ax.set_xlim([-1, 60])
plt.savefig('chances_1stim_trial60_rewards.png')

# STIM 1 WHOLE
fig, ax = plt.subplots(figsize=(5,5))
ax.plot(np.arange(nsteps), paths[:, 0], c='b', lw=1.5)
ax.set_ylabel('Chance of Winning')
ax.set_xlabel('Trial')
ax.set_ylim([0, 1])
ax.set_xlim([-1, nsteps])
plt.savefig('chances_1stim_whole.png')

# STIM 1 WHOLE, Rewards
fig, ax = plt.subplots(figsize=(5,5))
ax.plot(np.arange(nsteps), paths[:, 0], c='b', lw=1.5)
ax.scatter(np.arange(0, nsteps, 3), r[np.arange(0, nsteps, 3), 0]-0.1, c='k')
ax.set_ylabel('Chance of Winning')
ax.set_xlabel('Trial')
ax.set_ylim([0, 1])
ax.set_xlim([-1, nsteps])
plt.savefig('chances_1stim_whole_rewards.png')

# 2STIM
fig, ax = plt.subplots(figsize=(5,5))
ax.plot(np.arange(nsteps), paths[:, 0], c='b', lw=1.5)
ax.plot(np.arange(nsteps), paths[:, 1], c='r', lw=1.5)
ax.set_ylabel('Chance of Winning')
ax.set_xlabel('Trial')
ax.set_ylim([0, 1])
ax.set_xlim([-1, nsteps])
plt.savefig('chances_2stim_whole_rewards.png')

plt.show()
