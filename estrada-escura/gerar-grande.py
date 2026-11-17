# O beecrowd dá 3 segundos, e o caso pior tem m = 200000. Este 
# script gera um caso desse tamanho, garantindo que o grafo seja
# conexo e que a soma total fique abaixo de 2^31
import random

m, n = 100000, 200000
linhas = [f"{m} {n}"]
for v in range(1, m):
  linhas.append(f"{random.randrange(v)} {v} {random.randint(0, 10000)}")
for _ in range(n - (m - 1)):
  u, v = random.sample(range(m), 2)
  linhas.append(f"{u} {v} {random.randint(0, 10000)}")
linhas.append("0 0")

with open("grande.txt", "w") as arquivo:
  arquivo.write("\n".join(linhas) + "\n")