import json
import os
from datetime import datetime
from typing import List, Dict

class MaquinaVending:
    def __init__(self, ficheiro_stock="stock.json"):
        self.ficheiro_stock = ficheiro_stock
        self.stock: List[Dict] = []
        self.saldo = 0  # em cêntimos
        self.moedas_disponiveis = {
            "2e": 200, "1e": 100, "50c": 50, "20c": 20,
            "10c": 10, "5c": 5, "2c": 2, "1c": 1
        }
        self.carregar_stock()
    
    def carregar_stock(self):
        """Carrega o stock do ficheiro JSON"""
        try:
            if os.path.exists(self.ficheiro_stock):
                with open(self.ficheiro_stock, 'r', encoding='utf-8') as f:
                    self.stock = json.load(f)
                data_atual = datetime.now().strftime("%Y-%m-%d")
                print(f"maq: {data_atual}, Stock carregado, Estado atualizado.")
            else:
                # Criar stock inicial se o ficheiro não existir
                self.stock = [
                    {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
                    {"cod": "A24", "nome": "água 1.5L", "quant": 5, "preco": 1.0},
                    {"cod": "B15", "nome": "coca-cola", "quant": 10, "preco": 1.5},
                    {"cod": "B16", "nome": "ice tea", "quant": 7, "preco": 1.3},
                    {"cod": "C01", "nome": "snickers", "quant": 12, "preco": 1.2},
                    {"cod": "C02", "nome": "kit kat", "quant": 8, "preco": 1.1},
                    {"cod": "D10", "nome": "batatas fritas", "quant": 6, "preco": 0.9},
                ]
                self.guardar_stock()
                print(f"maq: {datetime.now().strftime('%Y-%m-%d')}, Stock inicial criado.")
        except Exception as e:
            print(f"maq: Erro ao carregar stock: {e}")
            self.stock = []
    
    def guardar_stock(self):
        """Guarda o stock no ficheiro JSON"""
        try:
            with open(self.ficheiro_stock, 'w', encoding='utf-8') as f:
                json.dump(self.stock, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"maq: Erro ao guardar stock: {e}")
    
    def listar_produtos(self):
        """Lista todos os produtos disponíveis"""
        if not self.stock:
            print("maq: Stock vazio. Não há produtos disponíveis.")
            return
        
        print("maq:")
        print(f"{'cod':<6} | {'nome':<20} | {'quantidade':<10} | {'preço':<6}")
        print("-" * 50)
        for produto in self.stock:
            print(f"{produto['cod']:<6} | {produto['nome']:<20} | "
                  f"{produto['quant']:<10} | {produto['preco']:.2f}€")
    
    def processar_moedas(self, moedas_str: str):
        """Processa as moedas inseridas pelo utilizador"""
        moedas = moedas_str.replace(",", " ").replace(".", "").split()
        valor_adicionado = 0
        
        for moeda in moedas:
            moeda = moeda.strip().lower()
            if moeda in self.moedas_disponiveis:
                valor_adicionado += self.moedas_disponiveis[moeda]
            else:
                print(f"maq: Moeda inválida ignorada: {moeda}")
        
        self.saldo += valor_adicionado
        self.mostrar_saldo()
    
    def mostrar_saldo(self):
        """Mostra o saldo atual"""
        euros = self.saldo // 100
        centimos = self.saldo % 100
        if euros > 0:
            print(f"maq: Saldo = {euros}e{centimos:02d}c" if centimos > 0 else f"maq: Saldo = {euros}e")
        else:
            print(f"maq: Saldo = {centimos}c")
    
    def encontrar_produto(self, codigo: str) -> Dict:
        """Encontra um produto pelo código"""
        for produto in self.stock:
            if produto['cod'].upper() == codigo.upper():
                return produto
        return None
    
    def selecionar_produto(self, codigo: str):
        """Seleciona e dispensa um produto"""
        produto = self.encontrar_produto(codigo)
        
        if not produto:
            print(f"maq: Produto com código '{codigo}' não existe.")
            return
        
        if produto['quant'] <= 0:
            print(f"maq: Produto '{produto['nome']}' esgotado.")
            return
        
        preco_centimos = int(produto['preco'] * 100)
        
        if self.saldo < preco_centimos:
            print("maq: Saldo insuficiente para satisfazer o seu pedido")
            euros_saldo = self.saldo // 100
            centimos_saldo = self.saldo % 100
            euros_preco = preco_centimos // 100
            centimos_preco = preco_centimos % 100
            
            saldo_str = f"{euros_saldo}e{centimos_saldo:02d}c" if euros_saldo > 0 else f"{centimos_saldo}c"
            preco_str = f"{euros_preco}e{centimos_preco:02d}c" if euros_preco > 0 else f"{centimos_preco}c"
            print(f"maq: Saldo = {saldo_str}; Pedido = {preco_str}")
            return
        
        # Dispensar produto
        produto['quant'] -= 1
        self.saldo -= preco_centimos
        print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
        self.mostrar_saldo()
    
    def calcular_troco(self) -> List[tuple]:
        """Calcula o troco usando o menor número de moedas"""
        troco = []
        valor_restante = self.saldo
        
        moedas_ordenadas = sorted(self.moedas_disponiveis.items(), 
                                  key=lambda x: x[1], reverse=True)
        
        for moeda_nome, moeda_valor in moedas_ordenadas:
            quantidade = valor_restante // moeda_valor
            if quantidade > 0:
                troco.append((quantidade, moeda_nome))
                valor_restante -= quantidade * moeda_valor
        
        return troco
    
    def dar_troco(self):
        """Calcula e mostra o troco"""
        if self.saldo == 0:
            return
        
        troco = self.calcular_troco()
        troco_str = ", ".join([f"{qtd}x {moeda}" for qtd, moeda in troco])
        print(f"maq: Pode retirar o troco: {troco_str}.")
    
    def adicionar_stock(self, codigo: str, nome: str, quantidade: int, preco: float):
        """Adiciona ou atualiza produto no stock"""
        produto = self.encontrar_produto(codigo)
        
        if produto:
            # Produto já existe, atualizar quantidade
            produto['quant'] += quantidade
            print(f"maq: Stock atualizado. '{produto['nome']}' agora tem {produto['quant']} unidades.")
        else:
            # Produto novo
            novo_produto = {
                "cod": codigo.upper(),
                "nome": nome,
                "quant": quantidade,
                "preco": preco
            }
            self.stock.append(novo_produto)
            print(f"maq: Produto '{nome}' adicionado ao stock com sucesso.")
    
    def executar(self):
        """Executa o loop principal da máquina"""
        print("maq: Bom dia. Estou disponível para atender o seu pedido.")
        
        while True:
            try:
                comando = input(">> ").strip()
                
                if not comando:
                    continue
                
                partes = comando.split(maxsplit=1)
                cmd = partes[0].upper()
                
                if cmd == "LISTAR":
                    self.listar_produtos()
                
                elif cmd == "MOEDA":
                    if len(partes) < 2:
                        print("maq: Por favor, especifique as moedas (ex: MOEDA 1e, 50c, 20c)")
                        continue
                    self.processar_moedas(partes[1])
                
                elif cmd == "SELECIONAR":
                    if len(partes) < 2:
                        print("maq: Por favor, especifique o código do produto")
                        continue
                    self.selecionar_produto(partes[1])
                
                elif cmd == "SALDO":
                    self.mostrar_saldo()
                
                elif cmd == "ADICIONAR":
                    # Formato: ADICIONAR A23 água 10 0.7
                    if len(partes) < 2:
                        print("maq: Formato: ADICIONAR <codigo> <nome> <quantidade> <preco>")
                        continue
                    try:
                        args = partes[1].split()
                        if len(args) < 4:
                            print("maq: Formato: ADICIONAR <codigo> <nome> <quantidade> <preco>")
                            continue
                        codigo = args[0]
                        preco = float(args[-1])
                        quantidade = int(args[-2])
                        nome = " ".join(args[1:-2])
                        self.adicionar_stock(codigo, nome, quantidade, preco)
                    except ValueError:
                        print("maq: Erro nos valores. Verifique quantidade e preço.")
                
                elif cmd == "AJUDA":
                    print("maq: Comandos disponíveis:")
                    print("  LISTAR - Lista todos os produtos")
                    print("  MOEDA <moedas> - Insere moedas (ex: MOEDA 1e, 50c, 20c)")
                    print("  SELECIONAR <codigo> - Seleciona um produto")
                    print("  SALDO - Mostra o saldo atual")
                    print("  ADICIONAR <cod> <nome> <quant> <preco> - Adiciona stock")
                    print("  SAIR - Termina e devolve o troco")
                
                elif cmd == "SAIR":
                    self.dar_troco()
                    self.guardar_stock()
                    print("maq: Até à próxima")
                    break
                
                else:
                    print(f"maq: Comando '{cmd}' não reconhecido. Digite AJUDA para ver comandos.")
            
            except KeyboardInterrupt:
                print("\nmaq: Encerrando...")
                self.guardar_stock()
                break
            except Exception as e:
                print(f"maq: Erro: {e}")

if __name__ == "__main__":
    maquina = MaquinaVending()
    maquina.executar()
