import sys
import re

def tokenize(input_string):
    reconhecidos = []
    linha = 1
    mo = re.finditer(r'(?P<SELECT>\bselect\b)|(?P<WHERE>\bwhere\b)|(?P<LIMIT>\blimit\b)|(?P<VAR>\?[A-Za-z_]\w*)|(?P<NUM>\d+)|(?P<NOME>[A-Za-z_][\w\-]*:[A-Za-z_][\w\-]*(?:/[A-Za-z0-9_\-./]*)?)|(?P<STRING>"(?:[^"\\]|\\.)*"(?:@[a-zA-Z\-]+)?)|(?P<BRACE_A>\{)|(?P<RBRACE_F>\})|(?P<PONTO>\.)|(?P<VIRGULA>,)|(?P<PONTO_VIRGULA>;)|(?P<DOIS_PONTOS>:)|(?P<IDEN>[A-Za-z_][\w\-]*)|(?P<SKIP>[ \t]+)|(?P<NEWLINE>\n)|(?P<COMMENT>#.*)|(?P<ERRO>.)', input_string)
    for m in mo:
        dic = m.groupdict()
        if dic['SELECT']:
            t = ("SELECT", dic['SELECT'], linha, m.span())

        elif dic['WHERE']:
            t = ("WHERE", dic['WHERE'], linha, m.span())
    
        elif dic['LIMIT']:
            t = ("LIMIT", dic['LIMIT'], linha, m.span())
    
        elif dic['VAR']:
            t = ("VAR", dic['VAR'], linha, m.span())
    
        elif dic['NUM']:
            t = ("NUM", dic['NUM'], linha, m.span())
    
        elif dic['NOME']:
            t = ("NOME", dic['NOME'], linha, m.span())
    
        elif dic['STRING']:
            t = ("STRING", dic['STRING'], linha, m.span())
    
        elif dic['BRACE_A']:
            t = ("BRACE_A", dic['BRACE_A'], linha, m.span())
    
        elif dic['RBRACE_F']:
            t = ("RBRACE_F", dic['RBRACE_F'], linha, m.span())
    
        elif dic['PONTO']:
            t = ("PONTO", dic['PONTO'], linha, m.span())
    
        elif dic['VIRGULA']:
            t = ("VIRGULA", dic['VIRGULA'], linha, m.span())
    
        elif dic['PONTO_VIRGULA']:
            t = ("PONTO_VIRGULA", dic['PONTO_VIRGULA'], linha, m.span())
    
        elif dic['DOIS_PONTOS']:
            t = ("DOIS_PONTOS", dic['DOIS_PONTOS'], linha, m.span())
    
        elif dic['IDEN']:
            t = ("IDEN", dic['IDEN'], linha, m.span())
    
        elif dic['SKIP']:
            t = ("SKIP", dic['SKIP'], linha, m.span())
    
        elif dic['NEWLINE']:
            t = ("NEWLINE", dic['NEWLINE'], linha, m.span())
    
        elif dic['COMMENT']:
            t = ("COMMENT", dic['COMMENT'], linha, m.span())
    
        elif dic['ERRO']:
            t = ("ERRO", dic['ERRO'], linha, m.span())
    
        else:
            t = ("UNKNOWN", m.group(), linha, m.span())
        if not dic['SKIP'] and t[0] != 'UNKNOWN': reconhecidos.append(t)
    return reconhecidos

for linha in sys.stdin:
    for tok in tokenize(linha):
        print(tok)
