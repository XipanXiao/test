import numpy as np
from numpy import savetxt
from scipy.optimize import linprog

N = 100

def v(X, Y):
  a, b, c = X
  d, e, f = Y
  r = (a - d) * (b - e) * (c - f)
  if r > 0:
      return -1
  if r < 0:
      return 1
#  print('(%d, %d, %d) vs (%d, %d, %d)' % (a, b, c, d, e, f))
  return 0


def gen_all_combinations(N):
  for a in range(1, N-1):
    for b in range(1, N-a):
      yield (a, b, N-a-b)


strategies = list(gen_all_combinations(N))
num_strategies = len(strategies)
print(num_strategies)

M = np.zeros((num_strategies, num_strategies))
for i in range(0, num_strategies):
  for j in range(0, num_strategies):
    M[j][i] = v(strategies[i], strategies[j]) + 1

c = np.ones((num_strategies, 1))
bounds = []
for i in range(0, num_strategies):
  bounds.append((0, None))

res = linprog(c, A_ub=-M, b_ub=-c, bounds=bounds)
s_u = np.sum(res.x, axis=0)
print("Value of the game: " + str(1.0/s_u - 1))
x = res.x / s_u
print(x.shape)
x = np.reshape(x, (num_strategies, 1))
print(x.shape)

strategy_and_prob = np.concatenate([strategies, x], axis=-1)
print(strategy_and_prob.shape)
print(strategy_and_prob)
savetxt('stratgies.csv', strategy_and_prob, delimiter=',')
