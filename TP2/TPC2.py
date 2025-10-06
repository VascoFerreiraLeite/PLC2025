import re
import sys

def markdown_para_html(texto):
    linhas = texto.split('\n')
    resultado = []
    lista_ativa = False

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        cabecalho = re.match(r'^(#{1,3})\s+(.*)', linha)
        if cabecalho:
            nivel = len(cabecalho.group(1))
            conteudo = cabecalho.group(2)
            resultado.append(f"<h{nivel}>{conteudo}</h{nivel}>")
            continue

        if re.match(r'^\d+\.\s', linha):
            if not lista_ativa:
                resultado.append("<ol>")
                lista_ativa = True
            item = re.sub(r'^\d+\.\s', '', linha)
        else:
            if lista_ativa:
                resultado.append("</ol>")
                lista_ativa = False
            item = linha

        item = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', item)

        item = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', item)

        item = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', item)

        item = re.sub(r'\*(.*?)\*', r'<i>\1</i>', item)

        if re.match(r'^\d+\.\s', linha):
            resultado.append(f"<li>{item}</li>")
        else:
            resultado.append(item)

    if lista_ativa:
        resultado.append("</ol>")

    return '\n'.join(resultado)

entrada = sys.stdin.read()
html = markdown_para_html(entrada)
print(html)
