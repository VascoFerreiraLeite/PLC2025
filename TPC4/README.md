# TPC3 - Analisador Léxico

Construir um analisador léxico para uma liguagem de query com a qual se podem escrever frases do género:

```
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
```
## Resolução 

Para criar o analisador léxico foi utilizado o [Gerador de Analisadores Léxicos](gerador.py) lecionado na quarta aula teórica.
O gerador recebeu como input os [tokens](tokens.json) no formato json criados para esta linguagem e deu como output o [analisador léxico](analizadorLexico) que admite a mesma linguagem.
