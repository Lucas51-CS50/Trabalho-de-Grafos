
# Estradas Escuras (beecrowd 1152)
 
Solução em Python para o problema [1152 – Estradas Escuras](https://judge.beecrowd.com/pt/problems/view/1152) do beecrowd, baseada no cálculo da **árvore geradora mínima** com o algoritmo de **Kruskal** e uma estrutura **Union-Find**.
 
## O problema
 
Byteland tem `m` junções ligadas por `n` estradas bidirecionais. Manter uma estrada iluminada custa 1 dólar por metro por dia. O governo quer desligar a iluminação de algumas estradas, desde que continue existindo um caminho iluminado entre quaisquer duas junções. A pergunta é: qual é a maior economia diária possível?
 
## Ideia da solução
 
Maximizar a economia equivale a minimizar o comprimento total das estradas que continuam iluminadas, porque
 
```
economia = (soma de todas as estradas) − (soma das estradas que ficam acesas)
```
 
O conjunto de estradas de menor comprimento total que mantém o grafo conexo é uma **árvore geradora mínima** (MST). Se esse conjunto tivesse um ciclo, qualquer aresta do ciclo poderia ser removida sem desconectar o grafo e sem aumentar o custo, já que os comprimentos são não negativos.
 
Para obter a MST, o algoritmo de Kruskal ordena as estradas da mais curta para a mais longa e aceita cada uma que ligue dois componentes ainda separados. Estradas que fechariam um ciclo são descartadas. A correção vem da propriedade do corte: a aresta mais leve que cruza qualquer divisão dos vértices pertence a alguma MST.
 
Para saber rapidamente se duas junções já estão conectadas, a solução usa Union-Find com compressão de caminho e união por altura (rank). Cada operação custa praticamente O(1) amortizado.
 
**Complexidade:** O(n log n) por caso de teste, dominada pela ordenação das estradas.
 
## Arquivos
 
| Arquivo | Descrição |
|---|---|
| `estrada-escura.py` | Solução do problema |
| `estresse.py` | Teste de estresse: compara a solução com uma força bruta em grafos aleatórios pequenos |
| `gerar-grande.py` | Gera `grande.txt`, uma entrada de tamanho máximo para o teste de desempenho |
| `entrada.txt` | Exemplo do enunciado |
 
O arquivo `grande.txt` é gerado localmente e não deve ser versionado (ver `.gitignore`).
 
## Como executar
 
O programa lê da entrada padrão até encontrar a linha `0 0`.
 
**Linux, macOS ou Git Bash:**
 
```bash
python3 estrada-escura.py < entrada.txt
```
 
**Windows (PowerShell):** o operador `<` não existe no PowerShell, então use o `cmd`:
 
```powershell
cmd /c "python estrada-escura.py < entrada.txt"
```
 
Saída esperada para o exemplo do enunciado:
 
```
51
```
 
## Testes
 
### 1. Exemplo do enunciado
 
Conteúdo de `entrada.txt`:
 
```
7 11
0 1 7
0 3 5
1 2 8
1 3 9
1 4 7
2 4 5
3 4 15
3 5 6
4 5 8
4 6 9
5 6 11
0 0
```
 
Saída esperada: `51`. A soma de todas as estradas é 90 e a MST tem comprimento 39.
 
### 2. Casos de borda
 
Entrada:
 
```
1 0
2 1
0 1 10
3 3
0 1 5
1 2 5
0 2 5
2 3
0 1 4
0 1 1
1 0 7
3 3
0 1 0
1 2 0
0 2 0
0 0
```
 
Saída esperada:
 
```
0
0
5
11
0
```
 
| Caso | O que testa |
|---|---|
| `1 0` | Uma junção e nenhuma estrada |
| `2 1` | Grafo que já é uma árvore: nada pode ser desligado |
| Triângulo com pesos iguais | Empates na ordenação |
| Três estradas entre as mesmas junções | Arestas paralelas, inclusive escritas em ordem inversa (`1 0`) |
| Pesos zero | Comprimento `z = 0`, permitido pelo enunciado |
 
O arquivo inteiro também verifica que o programa processa vários casos seguidos e para corretamente no `0 0`.
 
### 3. Teste de estresse
 
O script `estresse.py` gera 500 entradas aleatórias, cada uma com até 4 casos de teste em grafos pequenos (até 6 junções e 10 estradas, incluindo arestas paralelas e pesos zero). Para cada caso, compara a saída da solução com uma **força bruta** que testa todos os subconjuntos de estradas e escolhe o de menor comprimento entre os que mantêm o grafo conexo. A força bruta não usa nenhuma ideia do Kruskal, então funciona como verificação independente.
 
```bash
# Linux, macOS ou Git Bash
python3 estresse.py
```
 
```powershell
# Windows (PowerShell)
python estresse.py
```
 
Se todos os testes passarem, o script imprime:
 
```
Todos os 500 testes passaram.
```
 
Em caso de divergência, o script imprime a entrada que falhou, a saída esperada e a obtida. Como os grafos são pequenos, dá para simular o algoritmo à mão nessa entrada e encontrar o erro.
 
> O script executa `estrada-escura.py` como subprocesso, então os dois arquivos precisam estar na mesma pasta e o comando deve ser executado a partir dela.
 
### 4. Teste de desempenho
 
O limite de tempo do problema é de 3 segundos, e o caso máximo tem 200000 junções e 200000 estradas.
 
Primeiro, gere a entrada grande:
 
```bash
python gerar-grande.py
```
 
O comando não imprime nada, mas cria o arquivo `grande.txt`. Para variar o cenário, altere `m` e `n` no início de `gerar-grande.py`:
 
| Configuração | O que exercita |
|---|---|
| `m = n = 200000` | Tamanho máximo de entrada: leitura e ordenação de 200000 estradas. Há só uma estrada extra além da árvore, então a resposta é o peso de uma única aresta. |
| `m, n = 100000, 200000` | Cerca de 100000 estradas extras para o Union-Find analisar e rejeitar. |
 
Depois, meça o tempo de execução.
 
**Linux, macOS ou Git Bash:**
 
```bash
time python3 estrada-escura.py < grande.txt
```
 
**Windows (PowerShell):**
 
```powershell
Measure-Command { cmd /c "python estrada-escura.py < grande.txt" }
```
 
Observe o campo `TotalSeconds`. O `Measure-Command` esconde a saída do programa. Para ver a resposta, execute sem ele:
 
```powershell
cmd /c "python estrada-escura.py < grande.txt"
```
 
> Evite medir com `Get-Content grande.txt | python estrada-escura.py`. O `Get-Content` repassa o arquivo linha por linha pelo pipeline do PowerShell, e esse custo entra na medição. Em um dos testes, essa forma levou 5,7 s, contra 1,16 s com `cmd /c` para a mesma entrada.
 
Resultados medidos localmente (Python 3.11, Windows):
 
| Configuração | Tempo |
|---|---|
| `m = n = 200000` | ≈ 1,16 s |
| `m, n = 100000, 200000` | ≈ 0,71 s |
 
Os tempos variam entre execuções e entre máquinas. Para comparações mais confiáveis, rode cada medição algumas vezes e considere o menor tempo. Se a solução exceder o limite no juiz, submeta usando **PyPy**, quando disponível.
 
## Decisões de implementação
 
- **Leitura rápida:** toda a entrada é lida de uma vez com `sys.stdin.buffer.read().split()`, e as respostas são impressas em uma única escrita no final.
- **Listas paralelas:** origens, destinos e comprimentos ficam em três listas, e a ordenação é feita sobre os índices (`key=comprimentos.__getitem__`), o que é mais rápido que ordenar tuplas.
- **Union-Find sem classe:** as listas `pai` e `altura` e a função `encontrar` ficam locais, evitando o custo de chamadas de método em Python.
- **Parada antecipada:** o laço termina ao aceitar `m − 1` estradas, pois qualquer estrada restante formaria um ciclo.
 
