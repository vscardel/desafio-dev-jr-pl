## Visão Geral
O arquivo main.py contém as funções que recebem as requisições e retornam as respostas no formato especificado. O arquivo graph.py contém a lógica que implementa os grafos e métodos relacionados. O arquivo test_objects.py contém a definição de grafos em formato json para facilitar os testes unitários, que são definidos no arquivo test.py.

## Como Executar
  1. Para obter repositório, execute o comando:
    ```  git clone https://gitlab.com/vscardel/desafio-dev-jr-pl/```
  2. Para executar o código, dentro da pasta do projeto, execute o comando:
    ``` sudo docker-compose up```
  3. Quando a aplicação for inicializada e o banco estiver aceitando conexões, é possível executar os testes unitários. Para este fim, basta executar o seguinte comando dentro da pasta do projeto: 
     ``` python3 test.py ```
