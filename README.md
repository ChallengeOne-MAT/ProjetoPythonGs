
📦 Projeto CRUD com Python e Oracle
💡 Objetivo
Desenvolver uma aplicação em Python com:

Operações CRUD completas;

Consultas filtradas;

Exportação para JSON;

Integração com banco de dados Oracle (FIAP).

O projeto foi desenvolvido com base nas tabelas criadas na disciplina Building Relational Database.

🧰 Tecnologias Utilizadas
🐍 Python 3.x

🗄️ Banco de Dados Oracle

Host: oracle.fiap.com.br:1521/orcl

🔌 cx_Oracle (biblioteca de conexão com Oracle)

📁 JSON (para exportação de dados)

📚 Requisitos para Executar o Projeto
Python instalado (Download Python)

Instalar a biblioteca cx_Oracle:

bash
Copiar
Editar
pip install cx_Oracle
Ter acesso ao banco de dados Oracle da FIAP.

Configurar credenciais no código:

python
Copiar
Editar
conn = cx_Oracle.connect("SEU_USUARIO", "SUA_SENHA", "oracle.fiap.com.br:1521/orcl")
🧪 Funcionalidades Implementadas
✅ CRUD completo para a tabela SF_USUARIO
Inserir usuário com validação de campos

Listar usuários

Buscar por CPF

Atualizar dados

Deletar usuário com proteção ao CPF do admin

🔐 Admin reservado
CPF "00000000000" e senha "admin123" são reservados para uso interno

Operações como deletar esse usuário são bloqueadas

📦 Exportação de dados para JSON
Exporta dados filtrados das tabelas:

SF_OCORRENCIA

SF_AUTORIDADE

SF_MENSAGEM

Os arquivos JSON gerados seguem o padrão:

pgsql
Copiar
Editar
ocorrencias_status_PENDENTE.json
autoridades_especialidade_TRÂNSITO.json
mensagens_remetente_JOÃO.json
🚨 Funcionalidade SOS
Usuário escolhe uma autoridade e um evento (ex: Incêndio, Assalto)

Gera um registro de SOS com:

Nome da autoridade

Telefone

Evento

Timestamp

Exporta para ocorrencias_sos.json

🧩 Organização do Projeto
O código é totalmente modularizado:

Cada operação (inserção, listagem, atualização, etc.) tem sua própria função

Conexões ao banco são abertas e fechadas com segurança

Tratamento de erros via try/except

Funções reutilizáveis e com responsabilidade única (SRP)

📸 Exemplo de Execução
bash
Copiar
Editar
> Escolha uma opção:
1 - Inserir usuário
2 - Listar usuários
3 - Buscar por CPF
4 - Atualizar usuário
5 - Deletar usuário
6 - Exportar dados (ocorrência, autoridade, mensagem)
7 - Acionar SOS
0 - Sair
Após ações bem-sucedidas, o sistema exibe mensagens como:

arduino
Copiar
Editar
Usuário inserido com sucesso!
Usuário deletado com sucesso!
Arquivo "ocorrencias_status_PENDENTE.json" exportado com sucesso!
📁 Estrutura de Arquivos JSON
Exemplo de conteúdo em ocorrencias_sos.json:
json
Copiar
Editar
{
  "status": "SOS confirmado",
  "autoridade": "Polícia",
  "telefone": "190",
  "evento": "Assalto",
  "timestamp": "2025-06-08 15:42:33"
}
✅ Boas Práticas Adotadas
Validação de CPF e campos obrigatórios

Prevenção de inserções duplicadas (admin)

Modularização e reaproveitamento de código

Interface de texto interativa e limpa

Geração de arquivos JSON formatados e legíveis

Link do cideo Projeto Python:
https://youtu.be/kbu_erxRi6s?si=LiDTqEPq6Wu2Oi-A