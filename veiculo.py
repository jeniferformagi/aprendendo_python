from conexao import Connection
from pessoa import PessoaBanco
from propriedades import Enumerator

class Carro:
    def __init__(self, id, nome, cor, tipo, cpf):
        self.id = id
        self.nome = nome
        self.cor = cor
        self.tipo = tipo
        self.cpf = cpf

    def getData(self):
         return (self.id, self.nome, self.cor, self.tipo, self.cpf)


class CarroBanco:
    def getSqlIndice(self):
        return "SELECT COUNT(pescpf) + 1 AS next FROM norktown.veiculo WHERE pescpf = %s GROUP BY pescpf /*%s*/"

    def getSqlAll(self):
        return "SELECT veiculo.*, pesnome FROM norktown.veiculo LEFT JOIN norktown.pessoa USING (pescpf);"

    def getSqlBusca(self):
        return "SELECT veiculo.*, pesnome FROM norktown.veiculo LEFT JOIN norktown.pessoa USING (pescpf) WHERE veiid = %s AND veiculo.pescpf = %s;"

    def getSqlInsert(self):
        return "INSERT INTO norktown.veiculo (veiid, veinome, veicor, veitipo, pescpf) VALUES (%s, %s, %s, %s, %s);"
    
    def getSqlUpdate(self):
        return "UPDATE norktown.veiculo SET veinome = %s, veicor = %s, veitipo = %s WHERE veiid = %s AND pescpf = %s;"

    def getSqlDelete(self):
        return "DELETE FROM norktown.veiculo WHERE veiid = %s AND pescpf = %s;"

    def getNextIndice(self, cpf):
        cnx = Connection()
        indice = cnx.query(self.getSqlIndice(), (cpf, ''))
        cnx.close()
        try:
            index = indice[0]
        except IndexError:
            index = 1
        return index

    def all(self):
        cnx = Connection()
        carros = cnx.query(self.getSqlAll())
        cnx.close()
        return carros

    def allConsulta(self):
        enum = Enumerator()
        all = self.all()
        carros = []

        for item in all:
            car = [item[0], item[1], enum.getCor(item[2]), enum.getTipo(item[3]), item[4], item[5]]
            carros.append(car)

        return carros

    def refresh(self, id, cpf):
        cnx = Connection()
        carro = cnx.query(self.getSqlBusca(), (id, cpf))
        cnx.close()
        return Carro(carro[0][0], carro[0][1], carro[0][2], carro[0][3], carro[0][4])

    def insert(self, Carro):
        cnx = Connection()
        cnx.execute(self.getSqlInsert(), Carro.getData())
        cnx.commit()
        cnx.close()
    
    def update(self, Carro):
        cnx = Connection()
        data = Carro.getData()
        cnx.execute(self.getSqlUpdate(), (data[1], data[2], data[3], data[0], data[4]))
        cnx.commit()
        cnx.close()

    def delete(self, Carro):
        cnx = Connection()
        data = Carro.getData()
        cnx.execute(self.getSqlDelete(), (data[0], data[4]))
        cnx.commit()
        cnx.close()