import numpy as np
from math import fabs 
from time import time  
  
data = open('Wiki-Vote.txt')  
N = 7115 
tax_rate = 0.8  
eps = 1e-8  
r = [1./N for i in range(N)]  
r2 = [1./N for i in range(N)]  
out_degree = [0 for i in range(N)]
in_degree = [0 for i in range(N)]
user_ID = [0 for i in range(N)]
m = [[] for i in range(N*2)]
hash_table = [-1 for i in range(N*2)]
idx = 0

  
def hash(x):  
    global idx  
    if hash_table[x] == -1:  
        hash_table[x] = idx  
        idx += 1  
    return hash_table[x]  
  
info1 = data.readline()
info2 = data.readline()
info3 = data.readline()
info4 = data.readline()

for line in data:
    in_ID, out_ID = map(int, line.split())
    x, y = map(hash, [in_ID, out_ID])
    user_ID[x] = in_ID
    user_ID[y] = out_ID  
    out_degree[x] += 1
    in_degree[y] += 1 
    m[y].append(x)  


print('data loaded')

print('start iterating...')  
  
t = 0  
begin = time()  
  
while True:  
    for i in range(N):  
        r[i] = 0  
        for in_id in m[i]:   
            r[i] += tax_rate * r2[in_id] / out_degree[in_id]  
    der = 1 - sum(r)  
    for i in range(N):  
        r[i] += der / N  
  
    error = 0  
    for i in range(N):  
        if fabs(r[i]-r2[i]) > eps:  
            error = 1  
            break  
    for i in range(N):  
        r2[i] = r[i]  
    t += 1  
    if error == 0:  
        break  
  
end = time()
ranking = np.argsort(r)
ranking = ranking[::-1]

with open('PageRank_result.txt', 'w+') as f:
   f.write(info1)
   f.write(info2)
   f.write(info3)
   f.write('# Ranking    UserID    Rank    OutDegree    InDegree\n')
   for i in range(N):
       f.write('    %d        %d    %.4e    %d        %d\n' % (i+1, user_ID[ranking[i]], r[ranking[i]], out_degree[ranking[i]], in_degree[ranking[i]]))

print('total iteration is %d' % t)
print('total time is %f' % (end - begin))