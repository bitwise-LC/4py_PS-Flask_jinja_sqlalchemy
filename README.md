# Prazo Certo

Sistema web para cadastro de produtos, organização por categorias e controle de lotes e datas de validade.

O projeto utiliza Flask, Jinja, Flask-SQLAlchemy, SQLite, CSS e JavaScript modular. Todas as operações persistentes, validações, classificações de validade, alertas e indicadores são processados pelo backend.

## Preview

![Preview](https://github.com/user-attachments/assets/9f0cc18b-84eb-4ad2-bd11-4465383480fc)
<video src="/https://github.com/user-attachments/assets/9f0cc18b-84eb-4ad2-bd11-4465383480fc)" controls></video>

## Funcionalidades Implementadas

1. Cadastrar categoria
2. Listar categorias
3. Atualizar categoria
4. Excluir categoria
5. Cadastrar produto
6. Listar, pesquisar e filtrar produtos por categoria
7. Atualizar produto
8. Excluir produto
9. Cadastrar lote com fabricação, validade e quantidade
10. Listar, pesquisar e filtrar lotes por produto e situação de validade
11. Atualizar lote
12. Excluir lote
13. Consultar dashboard com indicadores e próximos vencimentos
14. Consultar notificações de lotes vencidos e críticos

## Arquitetura

```text
backend/
    controllers/
    models/
    repositories/
    routes/
    services/
frontend/
    static/
        css/
            style.css
        js/
            api.js
            calendario.js
            categorias.js
            dashboard.js
            estoque.js
            main.js
            notificacoes.js
            ui.js
    templates/
tests/
```

O fluxo das funcionalidades segue:

```text
Interface Jinja → API Flask → Controller → Service → Model/Repository → Banco de Dados
```

O frontend não utiliza `localStorage`, `sessionStorage` ou regras próprias de persistência e validade. O arquivo `api.js` concentra apenas a comunicação HTTP, enquanto os demais módulos cuidam exclusivamente da apresentação e das interações de cada tela.

## Como executar

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador. O banco SQLite é criado automaticamente na primeira execução.

## Testes

```powershell
python -m pytest -q
```
