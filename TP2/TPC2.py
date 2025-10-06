import re

def markdown_para_html(texto):
    linhas = texto.split('\n')
    resultado = []
    lista_ativa = False

    for linha in linhas:
        linha = linha.strip()

        # Cabeçalhos
        if linha.startswith('### '):
            resultado.append(f"<h3>{linha[4:]}</h3>")
        elif linha.startswith('## '):
            resultado.append(f"<h2>{linha[3:]}</h2>")
        elif linha.startswith('# '):
            resultado.append(f"<h1>{linha[2:]}</h1>")
        
        # Lista numerada
        elif re.match(r'^\d+\.\s', linha):
            if not lista_ativa:
                resultado.append("<ol>")
                lista_ativa = True
            item = re.sub(r'^\d+\.\s', '', linha)
            resultado.append(f"<li>{item}</li>")
        else:
            if lista_ativa:
                resultado.append("</ol>")
                lista_ativa = False
            # Bold
            linha = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', linha)
            # Itálico
            linha = re.sub(r'\*(.*?)\*', r'<i>\1</i>', linha)
            # Link
            linha = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', linha)
            # Imagem
            linha = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', linha)

            if linha:
                resultado.append(linha)

    # Fechar lista caso o texto termine com ela
    if lista_ativa:
        resultado.append("</ol>")

    return '\n'.join(resultado)


# Exemplo de uso
md_texto = """
# Exemplo de Cabeçalho

Este é um **texto em negrito** e um *texto em itálico*.

1. Primeiro item
2. Segundo item
3. Terceiro item

Como pode ser consultado em [página da UC](http://www.uc.pt)

Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com)
"""

html = markdown_para_html(md_texto)
print(html)
