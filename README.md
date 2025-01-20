# Garage API - Projecto de desenvolvimento de uma API REST com Flask

## Introdução

Este projeto consiste na criação de uma API para gestão de uma oficina automóvel. A API foi desenvolvida utilizando Flask e Flask-RESTx, com uma base de dados SQLite para armazenar informações sobre clientes, veículos, trabalhos, tarefas, faturas e configurações.

## Equipa de Desenvolvimento

O trabalho foi realizado por:

- **João Correia**
- **Lucas Silvestre**
- **Vladimiro Bonaparte**

Curso: **TPSI (Técnico/a Especialista em Tecnologias e Programação de Sistemas de Informação) - 1223**

## Objetivos do Projeto

Os objetivos principais do projeto incluem:

- Implementação de um sistema CRUD para todas as tabelas presentes no modelo de dados fornecido.
- Desenvolvimento de funcionalidades adicionais para automatizar processos da oficina.
- Criação de um sistema de relatórios para facilitar a análise dos dados.

## Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

```text
 garage_flask_api/
    |-- api/
    |   |-- __init__.py
    |   |-- client.py
    |   |-- employee.py
    |   |-- vehicle.py
    |   |-- work.py
    |   |-- task.py
    |   |-- invoice.py
    |   |-- invoice_item.py
    |   |-- setting.py
    |-- services/
    |   |-- client_service.py
    |   |-- employee_service.py
    |   |-- vehicle_service.py
    |   |-- work_service.py
    |   |-- task_service.py
    |   |-- invoice_service.py
    |   |-- invoice_item_service.py
    |   |-- setting_service.py
    |-- models/
    |   |-- client.py
    |   |-- employee.py
    |   |-- vehicle.py
    |   |-- work.py
    |   |-- task.py
    |   |-- invoice.py
    |   |-- invoice_item.py
    |   |-- setting.py
    |-- utils/
    |-- errors/
    |-- config.py
    |-- app.py
    |-- requirements.txt
```

## Funcionalidades Implementadas

- **Clientes:** Registo, edição, remoção e consulta de clientes.
- **Veículos:** Registo, edição, remoção e consulta de veículos.
- **Trabalhos:** Associação de trabalhos a veículos e gestão de status.
- **Tarefas:** Adição e gestão de tarefas associadas a trabalhos.
- **Faturas:** Geração de faturas e itens de fatura.
- **Configurações:** Definição de parâmetros configuráveis.

## Tecnologias Utilizadas

- **Backend:** Flask, Flask-RESTx
- **Base de Dados:** SQLite
- **Documentação:** Swagger (integrado com Flask-RESTx)
- **Testes:** Postman, Swagger

## Exemplo de alguns Endpoints

Alguns dos principais endpoints implementados como pedido incluem:

- `POST /api/client/` - Criar um novo cliente
- `POST /api/vehicle/` - Criar um novo veículo
- `GET /api/vehicle/` - Obter a lista de todos os veículos
- `PUT /api/work/<work_id>/status` - Atualizar status de um trabalho
- `POST /api/invoice` - Criar uma nova fatura

## Considerações Finais

O projeto foi concluído com sucesso, atingindo os objetivos propostos. As funcionalidades CRUD para todas as tabelas foram implementadas com sucesso e validadas através de testes.

A documentação da API permite uma compreensão clara das funcionalidades, garantindo que os utilizadores da API possam facilmente compreender como a utilizar nos seus sistemas.

Além disso, as boas práticas como a separação de responsabilidades ajudam a criar uma base sólida para futuras expansões, permitindo adicionar novas funcionalidades com facilidade.

Resumindo, a API apresenta uma solução simples e funcional para o workflow de uma garagem.
