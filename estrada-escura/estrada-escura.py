import sys

def main(): 
  # Leitura rápida: lê toda a entrada de uma vez e quebra em tokens
  # Chamar input() centenas de milhares de vezes é causa comum de TLE
  dados = sys.stdin.buffer.read().split()
  pos = 0
  saida = []
  
  while True: 
    nmr_juncoes = int(dados[pos])         # número de junções
    nmr_estradas = int(dados[pos + 1])    # número de estradas
    pos += 2
    
    if nmr_juncoes == 0 and nmr_estradas == 0:
      break     # linha "0 0" encerra a entrada
    
    # Cada estrada é uma trinca (x, y, z). O fatiamento com passo 3
    # pega o 1º, o 2º e o 3º valor de cada trinca, montando três
    # lista paralelas sem precisar de um laço explícito em Python
    fim = pos + 3 * nmr_estradas
    origens = list(map(int, dados[pos:fim:3]))
    destinos = list(map(int, dados[pos + 1:fim:3]))
    comprimentos = list(map(int, dados[pos + 2:fim:3]))
    pos = fim
    
    # Custo de manter todas as estradas iluminadas
    comprimento_total = sum(comprimentos)
    
    # Kruskal, passo 1: processar as estradas da mais curta para a mais longa
    # Ordenar os índices pelo comprimento é mais rápido que ordenar tuplas,
    # pos cada comparação olha apenas um número inteiro 
    ordem = sorted(range(nmr_estradas), key=comprimentos.__getitem__)
    
    # Union-Find (DSU): no início, cada junção é seu próprio componente
    pai = list(range(nmr_juncoes))
    altura = [0] * nmr_juncoes
    
    def encontrar(x): 
      # Sobe até a raiz do componente de x
      # Compressão de caminho (por halving): cada nó visitado passa a
      # apontar para o avô, achatando a árvore e deixando as próximas
      # buscas praticamente O(1)
      while pai[x] != x:
        pai[x] = pai[pai[x]]
        x = pai[x]
      return x
    
    comprimento_arvore = 0          # soma das estradas que continuam iluminadas
    arestas_usadas = 0
    necessarias = nmr_juncoes - 1   # uma árvore geradora com 'nmr_juncoes' de vértices tem 'nmr_juncoes' - 1 arestas 
    
    # Kruskal, passo 2: de forma gulosa, manter cada estrada que liga
    # dois componentes que ainda estão separados
    for i in ordem: 
      a = encontrar(origens[i])
      b = encontrar(destinos[i])
      if a == b: 
        continue    # mesmo componente: a estrada fecharia um ciclo
      
      # União por altura (rank): pendura a árvore mais baixa na main alta 
      if altura[a] < altura[b]: 
        a, b = b, a
      pai[b] = a
      if altura[a] == altura[b]:
        altura[a] += 1
        
      comprimento_arvore += comprimentos[i]
      arestas_usadas += 1
      if arestas_usadas == necessarias:
        break # árvore completa: qualquer estrada restantes formaria um ciclo 
      
    # Economia = o que se pegava antes - o que ainda se pega 
    saida.append(comprimento_total - comprimento_arvore)
    
  # Escrita rápida: imprime todas as respostas de uma vez só
  sys.stdout.write("\n".join(map(str, saida)) + "\n")

main()