from conexao import Connection
import re


class Pessoa:
    def __init__(self, cpf, nome):
        if len(cpf) == 11:
            valor = cpf.zfill(11)
            cpf =  '{}.{}.{}-{}'.format(valor[:3], valor[3:6], valor[6:9], valor[9:]) 
        
        self.cpf = cpf
        self.nome = nome

    def getData(self, format = False):
        cpf = self.cpf
        if format == True:
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")

        return (cpf, self.nome)


class PessoaBanco:
    def getSqlAll(self):
        return "SELECT pessoa.*, CASE WHEN COUNT(veiculo.pescpf) < 3 THEN 'Sim' ELSE 'Não' END FROM norktown.pessoa LEFT JOIN norktown.veiculo USING (pescpf) GROUP BY pescpf, pesnome;"

    def getSqlBusca(self):
        return "SELECT * FROM norktown.pessoa WHERE pescpf = %s /*%s*/;"

    def getSqlInsert(self):
        return "INSERT INTO norktown.pessoa (pescpf, pesnome) VALUES (%s, %s);"
    
    def getSqlUpdate(self):
        return "UPDATE norktown.pessoa SET pesnome = %s WHERE pescpf = %s;"

    def getSqlDelete(self):
        return "DELETE FROM norktown.pessoa WHERE pescpf = %s /*%s*/;"

    def getSqlDisponiveis(self):
        return "SELECT * FROM (SELECT pessoa.*, COUNT(veiculo.pescpf) FROM norktown.pessoa LEFT JOIN norktown.veiculo USING (pescpf) GROUP BY pessoa.pescpf, pesnome) pessoa WHERE pessoa.count < 3"

    def validas(self):
        cnx = Connection()
        pessoas = cnx.query(self.getSqlDisponiveis())
        cnx.close()
        return pessoas

    def all(self):
        cnx = Connection()
        pessoas = cnx.query(self.getSqlAll())
        cnx.close()
        return pessoas

    def refresh(self, cpf):
        cnx = Connection()
        pessoa = cnx.query(self.getSqlBusca(), (cpf, ''))
        cnx.close()
        return Pessoa(pessoa[0][0], pessoa[0][1])

    def insert(self, Pessoa):
        cnx = Connection()
        cnx.execute(self.getSqlInsert(), Pessoa.getData(True))
        cnx.commit()
        cnx.close()
    
    def update(self, Pessoa):
        cnx = Connection()
        data = Pessoa.getData(True)
        cnx.execute(self.getSqlUpdate(), (data[1], data[0]))
        cnx.commit()
        cnx.close()

    def delete(self, Pessoa):
        cnx = Connection()
        cnx.execute(self.getSqlDelete(), Pessoa.getData(True))
        cnx.commit()
        cnx.close()

