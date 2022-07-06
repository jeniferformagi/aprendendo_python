from flask import Flask, render_template, request, redirect
from pessoa import Pessoa
from veiculo import Carro
from pessoa import PessoaBanco
from veiculo import CarroBanco
from propriedades import Enumerator

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/pessoas/', methods=['GET', 'POST'])
def viewPessoas():
    pessBanco = PessoaBanco()
    pessoas = pessBanco.all()
    if request.method == 'GET' and request.args.get('cpfPessoa') != None and request.args.get('nomePessoa'):
        return render_template('pessoas.html', content = pessoas, caminhoUrl = './save/?cpfPessoa=' + request.args.get('cpfPessoa'), tituloBotao = 'Salvar', cpfPessoa = request.args.get('cpfPessoa'), nomePessoa = request.args.get('nomePessoa'), propriedade = 'disabled')
    else:
        return render_template('pessoas.html', content = pessoas, caminhoUrl = './include/', tituloBotao = 'Incluir', cpfPessoa = '', nomePessoa = '', propriedade = '')


@app.route('/pessoas/include/', methods=['GET', 'POST'])
def insertPessoa():
    if request.method == 'POST' and request.form.get("cpf") != None and request.form.get("name") != None:
        cpf = request.form.get("cpf")
        nome = request.form.get("name")

        pessoa = Pessoa(cpf, nome)

        pessoaSql = PessoaBanco()
        pessoaSql.insert(pessoa)

    return redirect('/pessoas/')


@app.route('/pessoas/save/', methods=['GET', 'POST'])
def savePessoa():
    if request.method == 'POST' and request.args.get('cpfPessoa') != None and request.form.get("name") != None:
        cpf = request.args.get('cpfPessoa')
        nome = request.form.get("name")

        pessoa = Pessoa(cpf, nome)

        pessoaSql = PessoaBanco()
        pessoaSql.update(pessoa)

    return redirect('/pessoas/')


@app.route('/pessoas/delete/', methods=['GET', 'POST'])
def deletePessoa():
    if request.method == 'GET' and request.args.get('cpfPessoa') != None:
        cpf = request.args.get('cpfPessoa')

        pessoa = Pessoa(cpf, '')

        pessoaSql = PessoaBanco()
        pessoaSql.delete(pessoa)

    return redirect('/pessoas/')



@app.route('/carros/', methods=['GET', 'POST'])
def viewCarros():
    carBanco = CarroBanco()
    pessoas = PessoaBanco()
    enum = Enumerator()

    id = request.args.get('id')
    cpf = request.args.get('cpf')

    if request.method == 'GET' and id != None and cpf != None:
        pessoa = pessoas.refresh(cpf)
        carro = carBanco.refresh(id, cpf)

        data = carro.getData()

        cores = enum.getColors()
        cores[data[2] - 1].append('selected')

        tipos = enum.getTypes()
        tipos[data[3] - 1].append('selected')

        tables = [[pessoa.getData(True)], cores, tipos]
        definicoes = ['./save/?id=' + id + '&cpf=' + cpf, 'Salvar', 'disabled', data[1]]
    else:
        tables = [pessoas.validas(), enum.getColors(), enum.getTypes()]
        definicoes = ['./include/', 'Incluir', '', '']

    return render_template('carros.html', content = carBanco.allConsulta(), tabelas = tables, dados = definicoes)



@app.route('/carros/include/', methods=['GET', 'POST'])
def insertCarro():
    cpf = request.form.get("cpf")
    nome = request.form.get("name")
    cor = request.form.get("cor")
    tipo = request.form.get("tipo")

    if request.method == 'POST' and cpf != None and nome != None and cor != None and tipo != None:
        banco = CarroBanco()

        carro = Carro(banco.getNextIndice(cpf), nome, cor, tipo, cpf)
        banco.insert(carro)

    return redirect('/carros/')



@app.route('/carros/save/', methods=['GET', 'POST'])
def updateCarro():
    id = request.args.get("id")
    cpf = request.args.get("cpf")

    if request.method == 'POST' and id != None and cpf != None:
        nome = request.form.get("name")
        cor = request.form.get("cor")
        tipo = request.form.get("tipo")

        carro = Carro(id, nome, cor, tipo, cpf)

        banco = CarroBanco()
        banco.update(carro)

    return redirect('/carros/')



@app.route('/carros/delete/', methods=['GET', 'POST'])
def deleteCarro():
    id = request.args.get('id')
    cpf = request.args.get('cpf')
    
    if request.method == 'GET' and id != None and cpf != None:

        carro = Carro(id, '', '', '', cpf)

        carroSql = CarroBanco()
        carroSql.delete(carro)

    return redirect('/carros/')