import csv
from functools import reduce

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



MediaAlunos = list(map(lambda x: {
    'nome': x['nome'],
    'faltas': x['faltas'],
    'media': round(min(sum(x['notas']) / len(x['notas'])+ 1 if x['extra'] == 1 else sum(x['notas']) / len(x['notas']),10),2)
},alunos))
aprovadosMedia = list(filter(lambda x: x['media'] >=7 and x['faltas'] <15, MediaAlunos))
recuperacao = list(filter(lambda x: x['media'] <7 and x['faltas'] < 15, MediaAlunos))

reprovadoFalta = list(filter(
    lambda x: x['faltas'] >= 15,
    MediaAlunos
))

with open('final.csv', 'r') as arquivo_final:
    leitor_final = csv.DictReader(arquivo_final, delimiter=';')
    dados_final = list(leitor_final)

alunosFinal = list(map(
    lambda x: {
        'nome': x['nome'],
        'faltas': x['faltas'],
        'media': float(x['media']),
        'notaFinal': float(x['nota5'])
    }, 
    dados_final))
aprovadosMediaStatus = list(map(
    lambda x: {
        'nome': x['nome'],
        'media': x['media'],
        'faltas': x['faltas'],
        'status': 'Aprovado por média'
    },
    aprovadosMedia
))
reprovadoFaltaStatus = list(map(lambda x: {
    'nome': x['nome'],
    'faltas': x['faltas'],
    'media': x['media'],
    'status': 'Reprovado por falta'
}, reprovadoFalta))

AprovadoouReprovado = list(map(lambda x: {

    'nome': x['nome'],
    'media': round((x['media'] + x['notaFinal'])/2,2),
    'faltas': x['faltas'],
    'status': 'Aprovado' if (x['media'] + x['notaFinal']) / 2>=5 else 'reprovado'


}, alunosFinal))

lauread = reduce(
    lambda maior, atual:
        atual if atual['media'] > maior['media'] else maior,
    MediaAlunos
)

laureado = {
    'nome': lauread['nome'],
    'media': lauread['media'],
    'faltas': '',
    'status': 'Laureado'
}

resultadoFinal = (aprovadosMediaStatus + reprovadoFaltaStatus + AprovadoouReprovado + [laureado])
with open('resultado.csv', 'w') as arquivo:
    campos = ['nome', 'faltas', 'media', 'status']
    gerarArquivo = csv.DictWriter(arquivo,fieldnames = campos, delimiter =';')
    gerarArquivo.writeheader()
    gerarArquivo.writerows(resultadoFinal)
    
    
    
    
    
    
    
    