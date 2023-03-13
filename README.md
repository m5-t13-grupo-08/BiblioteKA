# BiblioteKA - README

Esta é uma aplicação de gestão de biblioteca, em Python/Django e com banco de dados postgreSQL, cujo objetivo é gerenciar o empréstimo e devolução de livros, além de possibilitar o cadastro e login de usuários e colaboradores.

## Funcionalidades
As seguintes funcionalidades foram desenvolvidas para o MVP do projeto:

1. Empréstimo de Livros: cada livro pode ser emprestado por um período fixo de tempo.

2. Devolução de Livros: todos os livros emprestados possuem uma data de retorno e, caso a devolução seja agendada para um fim de semana, a data de retorno será modificada para o próximo dia útil. Se o estudante não devolver o livro no prazo estipulado, ele será bloqueado de solicitar novos empréstimos.

3. Bloqueio de Novos Empréstimos: estudantes com livros em atraso não podem solicitar novos empréstimos até a devolução dos anteriores. Após completar as devoluções pendentes, o bloqueio permanece por alguns dias.

4. Usuários: o sistema permite o cadastro de dois tipos de usuários - estudante e colaborador da biblioteca - e também possibilita que usuários não autenticados visualizem informações sobre os livros, como disponibilidade e título.

5. Funcionalidades para estudantes: um estudante pode ver seu próprio histórico de livros emprestados, obter informações sobre livros e seguir um livro para receber notificações por e-mail.

6. Funcionalidades para colaboradores: um colaborador pode cadastrar novos livros, emprestar livros, verificar o histórico de empréstimo de cada estudante e verificar o status do estudante.

## Diagrama de Entidade e Relacionamento Conceitual

Há uma relação de 1 → N entre livro e cópia, pois na biblioteca pode haver mais de uma cópia disponível para um determinado livro.

Também há uma relação de N:N entre usuário e cópia, onde a tabela com as informações do empréstimo é a pivô. Isso permite saber quais cópias foram emprestadas para cada usuário e também quais usuários pegaram emprestado uma determinada cópia.

E também uma relação N:N entre usuário e livro, que possibilita guardar informações de qual livro o usuário está seguindo. Essa relação é importante para que o usuário receba notificações sobre o livro que está interessado em ler.

Essas relações foram implementadas no desenvolvimento da aplicação para garantir a integridade dos dados e permitir o correto funcionamento das funcionalidades.

## Models

User (Usuário):

* id: identificador único gerado automaticamente em UUID4
* email: endereço de email do usuário
* user_category: categoria do usuário, que define a duração do empréstimo (graduação, pós-graduação ou colaborador)
* first_name: primeiro nome do usuário
* last_name: sobrenome do usuário
* username: nome de usuário para login (geralmente a matrícula)
* password: senha do usuário
* situation: situação do usuário na biblioteca (normal, em débito, desconectado ou suspenso)
* address: endereço do usuário, relacionamento com o modelo Address

Address:

* zip_code: CEP do endereço
* uf: unidade federativa do endereço
* complement: complemento do endereço
* telephone: telefone do endereço
* street: rua do endereço
* district: bairro do endereço

Book (Livro):

* id: identificador único gerado automaticamente em UUID4
* title: título do livro
* author: autor do livro
* page_number: número de páginas do livro
* publisher: editora do livro
* cdu: código de classificação decimal universal do livro
* followed_by: usuários que seguem o livro, relacionamento many-to-many com o modelo User

Copy (Cópia):

* buyed_at: data de compra da cópia
* price: preço da cópia
* sector: setor da biblioteca em que a cópia se encontra (coleção geral, restauração, perdido ou tratamento técnico)
* is_free: indica se a cópia está disponível para empréstimo
* book: livro ao qual a cópia pertence, relacionamento com o modelo Book

Loan (Empréstimo):

* id: identificador único gerado automaticamente em UUID4
* user: usuário que realizou o empréstimo, relacionamento com o modelo User
* copy: cópia emprestada, relacionamento com o modelo Copy
* loan_date: data do empréstimo
* deadline: data de devolução prevista
* devolutions_date: data de devolução efetiva
* renovations: número de renovações do empréstimo

## Extras
As seguintes funcionalidades extras também foram desenvolvidas:

* Sistema de avaliações de livros
* Feed com livros recentes adicionados à biblioteca
* Front end responsivo
* Mensagens de cobrança para livros não devolvidos no prazo
* Multa por devolução tardia do livro
* Envio de lembrete um dia antes da data máxima do prazo de devolução

## Comandos para inicialização e uso da Api

1. Crie seu ambiente virtual:
```bash
python -m venv venv
```
2. Ative seu venv:
```bash
# linux:
source venv/bin/activate
# windows:
.\venv\Scripts\activate
```
3. Instalar requirements.txt:
```bash
pip install -r requirements.txt
```
4. Preencher as variáveis de ambiente no .env; 
* Setar a variável DEBUG como True
