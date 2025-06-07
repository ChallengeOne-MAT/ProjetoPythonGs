## Projeto CRUD com Python e Banco de Dados Oracle

**Objetivo:** Desenvolver uma aplicação em Python com operações CRUD completas, consultas com filtros e exportação em JSON, utilizando as tabelas implementadas na disciplina de Building Relational Database.

**Tecnologias utilizadas:**  
- Python  
- cx_Oracle  
- Banco de Dados Oracle (FIAP - oracle.fiap.com.br:1521/orcl)  
- JSON  

**Funcionalidades Implementadas:**

1. Menu interativo com 7 opções
2. Inserção de usuários com validação
3. Listagem de usuários
4. Atualização de registros
5. Exclusão de registros
6. Exportação de dados filtrados das tabelas `SF_OCORRENCIA`, `SF_AUTORIDADE`, `SF_MENSAGEM` para JSON

**Exemplo de execução:**

> O programa solicita ao usuário o que deseja fazer. Após inserir, listar ou atualizar, mostra mensagens de sucesso. No caso da exportação, o sistema salva os arquivos como:
- `ocorrencias_status_PENDENTE.json`
- `autoridades_especialidade_TRÂNSITO.json`
- `mensagens_remetente_JOÃO.json`

**Tratamento de Erros:** Todos os acessos ao banco estão protegidos por blocos `try/except`, com encerramento seguro de conexões.

**Organização:** O sistema é modular, com cada função realizando uma única responsabilidade. O código é reutilizável e escalável.
