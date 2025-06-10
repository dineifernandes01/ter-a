# testedinei

API em Flask com SQLite para gerenciamento de usuários, depósitos, rendimentos e sistema de comissões em rede.

## Funcionalidades

- Cadastro com referência de indicação
- Depósitos com distribuição de comissões até 5 níveis
- Saques com validação
- Rendimento percentual
- Histórico por usuário

## Como executar

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

- `POST /cadastro`
- `POST /depositar`
- `POST /sacar`
- `POST /aplicar_rendimento`
- `GET /painel_usuario/<user_id>`
