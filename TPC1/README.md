# Especificação de uma expressão regular

Especifique uma expressão regular que faça match com qualquer string binária desde que esta não contenha a substring "011".

Exemplos válidos:

1111111<br>
000001<br>
1111010101000

Exemplos inválidos:

111010110111<br>
011<br>
00000001100000000


## Suloção
```
^((01?(01|0)*)|(1+(01|0)*))$
```

<img width="716" height="264" alt="image" src="https://github.com/user-attachments/assets/935189bc-6d56-4b8f-8ef7-1b02e9d637d8" />
