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

mediaCalcular = lambda nota:sum(nota) / len(nota)
menor = lambda x,y: x if x< y else y
mediadafinal = lambda media, final: (media + final) /2

MediaAlunos = list(map(lambda x: {
    'nome': x['nome'],
    'faltas': x['faltas'],
    'media': round(menor(mediaCalcular(x ['notas']) + 1 if x['extra'] == 1 else mediaCalcular(x['notas']),10),2)
},alunos))
aprovadosMedia = list(filter(lambda apm: apm['media'] >=7, filter(lambda x :  x['faltas'] <15, MediaAlunos)))
print(aprovadosMedia)
recuperacao = list(filter(lambda x: x['media'] <7, filter(lambda x : x['faltas'] < 15, MediaAlunos)))

reprovadoFalta = list(filter(
    lambda alunoRepr: alunoRepr['faltas'] >= 15,
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
        'status': 'Aprovado por media'
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
    'media': round(mediadafinal(x['media'], x['notaFinal']),2),
    'faltas': x['faltas'],
    'status': 'Aprovado' if mediadafinal(x['media'], x['notaFinal'])>=5 else 'reprovado'


}, alunosFinal))

maiorMedia = max(map(lambda x: x['media'], MediaAlunos))

laureados = list(map(lambda x: {
    'nome': x['nome'],
    'media': x['media'],
    'faltas': x['faltas'],
    'status': 'Laureado'
}, filter(lambda x: x['media'] == maiorMedia, MediaAlunos)))

resultadoFinal = (aprovadosMediaStatus + reprovadoFaltaStatus + AprovadoouReprovado + laureados)
with open('resultado.csv', 'w', newline = '') as arquivo:
    campos = ['nome', 'faltas', 'media', 'status']
    gerarArquivo = csv.DictWriter(arquivo,fieldnames = campos, delimiter =';')
    gerarArquivo.writeheader()
    gerarArquivo.writerows(resultadoFinal)
    
contagemAprovadosMedia = reduce(lambda contFinal, estado : contFinal+1 if estado['status'] == 'Aprovado por media' else contFinal, aprovadosMediaStatus,0)
contagemAprovados = reduce(lambda contFinal, estado : contFinal+1 if estado['status'] == 'Aprovado' else contFinal, AprovadoouReprovado,0)
contagemReprovados = reduce(lambda contFinal, estado : contFinal+1 if estado['status'] == 'reprovado' else contFinal, AprovadoouReprovado,0)
contagemReprovadosFalta = reduce(lambda contFinal, estado : contFinal+1 if estado['status'] == 'Reprovado por falta' else contFinal, reprovadoFaltaStatus,0)
contagemTotal = sum(map(lambda cont: 1, alunos))

porcentagem = lambda x,y: round(x * 100 / y,2)

Relatorio = [
    {
        'status': 'Aprovados por media',
        'quantidade': contagemAprovadosMedia,
        'porcentagem': f'{porcentagem(contagemAprovadosMedia, contagemTotal)}%'
    },
    {
        'status': 'Aprovados na final',
        'quantidade': contagemAprovados,
        'porcentagem': f'{porcentagem(contagemAprovados, contagemTotal)}%'
    },
    {
        'status': 'Reprovados na final',
        'quantidade': contagemReprovados,
        'porcentagem': f'{porcentagem(contagemReprovados, contagemTotal)}%'
    },
    {
        'status': 'Reprovados por falta',
        'quantidade': contagemReprovadosFalta,
        'porcentagem': f'{porcentagem(contagemReprovadosFalta, contagemTotal)}%'
    },
    {
        'status': 'Total de alunos',
        'quantidade': contagemTotal,
        'porcentagem': '100%'
    }
]

with open('relatorio.csv', 'w', newline='') as arquivo:
    campos = ['status', 'quantidade', 'porcentagem']
    gerarRelatorio = csv.DictWriter(arquivo, fieldnames=campos, delimiter=';')
    gerarRelatorio.writeheader()
    gerarRelatorio.writerows(Relatorio)