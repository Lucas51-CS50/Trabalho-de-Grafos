from heapq import heappop, heappush
import sys


# Resolução do problema do Sapo Preguiçoso (Lazy Jumping Frog)
# https://judge.beecrowd.com/en/problems/view/1384

""" 
Alunos:

Lucas Orita Almeida - RA134817


 """

# Matriz 5x5 de custos de energia para cada deslocamento (dr + 2, dc + 2)
CUSTO = (
    (7, 6, 5, 6, 7),
    (6, 3, 2, 3, 6),
    (5, 2, 0, 2, 5),
    (6, 3, 2, 3, 6),
    (7, 6, 5, 6, 7),
)

INF = 10**9


def solve():
    # Lê toda a entrada padrão de uma única vez
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    idx = 0
    total_tokens = len(tokens)
    saidas = []

    while idx < total_tokens:
        C = int(tokens[idx])
        R = int(tokens[idx + 1])
        idx += 2

        if C == 0 and R == 0:
            break

        cf = int(tokens[idx])
        rf = int(tokens[idx + 1])
        ct = int(tokens[idx + 2])
        rt = int(tokens[idx + 3])
        idx += 4

        W = int(tokens[idx])
        idx += 1

        # Adiciona 2 células de borda (padding) em cada lado para evitar checagem de limites
        cols = C + 4
        rows = R + 4
        size = cols * rows

        # 1 = água (ou borda inválida), 0 = célula seca
        agua = bytearray(b"\x01") * size
        linha_seca = b"\x00" * C
        for r in range(2, R + 2):
            inicio = r * cols + 2
            agua[inicio : inicio + C] = linha_seca

        # Marca os W retângulos alagados usando atribuição por fatia (slice)
        for _ in range(W):
            c1 = int(tokens[idx])
            r1 = int(tokens[idx + 1])
            c2 = int(tokens[idx + 2])
            r2 = int(tokens[idx + 3])
            idx += 4

            largura = c2 - c1 + 1
            bloco_agua = b"\x01" * largura
            for r in range(r1 + 1, r2 + 2):
                inicio = r * cols + (c1 + 1)
                agua[inicio : inicio + largura] = bloco_agua

        start = (rf + 1) * cols + (cf + 1)
        target = (rt + 1) * cols + (ct + 1)

        if start == target:
            saidas.append("0")
            continue

        # Pré-calcula os 24 saltos possíveis como deslocamentos lineares 1D
        movimentos = []
        for dr in (-2, -1, 0, 1, 2):
            for dc in (-2, -1, 0, 1, 2):
                if dr != 0 or dc != 0:
                    movimentos.append((dr * cols + dc, CUSTO[dr + 2][dc + 2]))

        # Dijkstra com estado empacotado em um único inteiro: (custo << 20) | pos
        dist = [INF] * size
        dist[start] = 0
        pq = [start]  # Como o custo inicial é 0, (0 << 20) | start == start

        encontrou = -1
        while pq:
            estado = heappop(pq)
            d = estado >> 20
            pos = estado & 0xFFFFF

            # Parada antecipada ao alcançar a casa da Sra. Sapa
            if pos == target:
                encontrou = d
                break

            # Como os pesos são positivos, a primeira remoção da fila é definitiva
            if agua[pos]:
                continue
            agua[pos] = 1

            for delta, peso in movimentos:
                npos = pos + delta
                if not agua[npos]:
                    nd = d + peso
                    if nd < dist[npos]:
                        dist[npos] = nd
                        heappush(pq, (nd << 20) | npos)

        if encontrou == -1:
            saidas.append("impossible")
        else:
            saidas.append(str(encontrou))

    sys.stdout.write("\n".join(saidas) + "\n")


if __name__ == "__main__":
    solve()