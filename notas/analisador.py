import csv

with open('Pasta1.csv', 'r') as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=';')
    dados = list(leitor)
alunos = list(map(
    lambda x: {
        'nome': x['nome'],
        'extra': int(x['extra']),
        'faltas': int(x['faltas']),
        'notas': list(map(float, [x['nota1'], x['nota2'], x['nota3'], x['nota4']]))
    }, 
    dados))

#print(alunos)

MediaAlunos = list(map(lambda x: {
    'nome': x['nome'],
    'faltas': x['faltas'],
    'media': min(sum(x['notas']) / len(x['notas'])+ 1 if x['extra'] == 1 else sum(x['notas']) / len(x['notas']),10)
},alunos))

aprovadosMedia = list(filter(lambda x: x['media'] >=7 and x['faltas'] <15, MediaAlunos))
recuperacao = list(filter(lambda x: x['media'] <7, MediaAlunos))
reprovadoFalta = list(filter(
    lambda x: x['faltas'] >= 15,
    alunos
))

print("XXXXXAPROVADO POR MÉDIA: xxxxx")
print(aprovadosMedia)
print("xxxxx REPROVADO POR FALTAS:xxxxx")
print(reprovadoFalta)
print("xxxxx RECUPERAÇÃO:xxxxx")
print(recuperacao)
print("xxxxx   MÉDIA DE ALUNOS: xxxxx")
print(MediaAlunos)

with open('final.csv', 'r') as arquivo_final:
    leitor_final = csv.DictReader(arquivo_final, delimiter=';')
    dados_final = list(leitor_final)

alunosFinal = list(map(
    lambda x: {
        'nome': x['nome'],
        'notaFinal': float(x['nota5'])
    }, 
    dados_final))

resultadoFinal = list(map(
    lambda x: {
        'nome': x['nome'],
        'status': 'AprovadoFinal' if x['notaFinal'] >= 5 else 'Reprovado'
    },
    alunosFinal
))

print(resultadoFinal)
