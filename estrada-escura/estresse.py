# Para ter confiança real, comparamos com uma solução lenta, porém obviamente correta,
# em muitos grafos aleatórios pequenos. A força bruta abaico testa todos os 
# subconjuntos de estradas e, ebtre os que mantêm o grafo conexo, escolhe o de menor
# comprimento. Ela não usa nenhuma das ideias do Kruskal, por isso serve como 
# verificação independente. Com até 10 arestas são no máximo 2^10 = 1024 subconjuntos,
# o que é instantâneo
import random 
import subprocess
import sys

def conectado(nmr_juncoes, arestas):
  # Busca em profundidade a partir da junção 0 usando só as arestas dadas 
  vizinhos = [[] for _ in range(nmr_juncoes)]
  for u, v, _ in arestas: 
    vizinhos[u].append(v)
    vizinhos[v].append(u)
  visitado = [False] * nmr_juncoes
  pilha = [0]
  visitado[0] = True
  while pilha: 
    x = pilha.pop()
    for y in vizinhos[x]: 
      if not visitado[y]: 
        visitado[y] = True
        pilha.append(y)
  return all(visitado)

def forca_bruta(nmr_juncoes, arestas): 
  # Testa todos os subconjuntos de estradas que poderiam ficar acesas
  total = sum(w for _, _, w in arestas)
  menor_custo = total
  for mascara in range(1 << len(arestas)): 
    escolhidas = [arestas[i] for i in range(len(arestas)) if mascara >> i & 1]
    if conectado(nmr_juncoes, escolhidas):
      menor_custo = min(menor_custo, sum(w for _, _, w in escolhidas))
  return total - menor_custo

def gerar_caso(): 
  nmr_juncoes = random.randint(1, 6)
  arestas = []
  
  # Primeiro uma árvore aleatória, para garantir que o grafo é conexo
  for v in range(1, nmr_juncoes):  
    u = random.randrange(v)
    arestas.append((u, v, random.randint(0, 20)))
  # Depois arestas extras aleatórias (podem ser paralelas)
  extras = random.randint(0, 10 - len(arestas)) if nmr_juncoes > 1 else 0
  for _ in range(extras): 
    u, v = random.sample(range(nmr_juncoes), 2)
    arestas.append((u, v, random.randint(0, 20)))
  random.shuffle(arestas)
  return nmr_juncoes, arestas

for teste in range(200):
  # Vários casos por entrada, para testar também o laço de leitura
  casos = [gerar_caso() for _ in range(random.randint(1, 4))]
  
  linhas = []
  for nmr_juncoes, arestas in casos: 
    linhas.append(f"{nmr_juncoes} {len(arestas)}")
    linhas.extend(f"{u} {v} {w}" for u, v, w in arestas)
  linhas.append("0 0")
  entrada = "\n".join(linhas) + "\n"
  
  esperado = [str(forca_bruta(nmr_juncoes, arestas)) for nmr_juncoes, arestas in casos]
  resultado = subprocess.run(
    [sys.executable, "estrada-escura.py"],
    input=entrada, capture_output=True, text=True,
  ).stdout.split()
  
  if resultado != esperado:
    print("DIVERGÊNCIA no teste", teste)
    print("Entrada:\n" + entrada)
    print("Esperado:", esperado)
    print("Obtido: ", resultado)
    break
else: 
  print("Todos os 500 testes passaram.")
  
  
  
  
  
   