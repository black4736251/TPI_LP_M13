# Loja de carrinhos

Programa que permite comprar, vender e manipular a quantidade de carrinhos.

## Como executar

1. Instalar dependências:
```
pip install -r requirements.txt
```

2. Iniciar o programa:
```
python main.py
```
Ou em alguns sistemas:
```
python3 main.py
```

## Estrutura do projeto

```
.
├── databases
│   └── database.db
├── images
│   ├── program
│   │   ├── bugatti_bolide.png
│   │   ├── cart.png
│   │   ├── eye.png
│   │   ├── mazda_mx-5.png
│   │   └── nissan_gt-r.png
│   └── readme
│       ├── cart.png
│       ├── login.png
│       ├── shop.png
│       └── stock.png
├── main.py
├── README.md
├── reports
│   └── sales.csv
├── requirements.txt
├── sounds
│   ├── click.mp3
│   ├── close.mp3
│   ├── information.mp3
│   ├── login.mp3
│   ├── purchase.mp3
│   ├── shop.mp3
│   ├── stock.mp3
│   └── warning.mp3
└── sources
    ├── cart.py
    ├── config.py
    ├── database.py
    ├── login.py
    ├── shop.py
    ├── start.py
    ├── stock.py
    └── utils.py
```

## Capturas de ecrã

### Iniciar sessão
<p align="center">
  <img src="images/readme/login.png" width="900" height="900" alt="Iniciar sessão">
</p>

### Loja
<p align="center">
  <img src="images/readme/shop.png" width="900" height="900" alt="Loja">
</p>

### Carrinho de compras
<p align="center">
  <img src="images/readme/cart.png" width="900" height="900" alt="Carrinho de compras">
</p>

### Manipular quantidades
<p align="center">
  <img src="images/readme/stock.png" width="900" height="900" alt="Manipular quantidades">
</p>