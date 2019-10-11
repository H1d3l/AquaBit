
# TesteAquabit
Projeto com o objetivo de criar uma plataforma de login e cadastro de clientes do aquabit. 

## Como o projeto está estruturado?
- **Documentação :** Contém a modelagem das classes. Possui o arquivo de requisitos do projeto e a modelagem do diagrama de classe e caso de uso.
- **usuarios:** Contém os arquivos necessários para a execução da aplicação. A pasta “usuarios” refere-se a uma determinada parte da aplicação do software. A organização dos arquivos possui a estrutura do framework Django.

# Modelagem

- Diagrama de Classes
![Modelagem Design de Classes](/documentacao/Class%20Diagram0.png)

- Diagrama de Caso de Uso
![Modelagem Design de Caso de Uso](/documentação/UseCase%20Diagram0.png)



## Execução da aplicação:

O projeto não possui dependência. Então segue o passo-a-passo para executar a aplicação:
```
git clone https://github.com/H1d3l/TesteAquaBit.git
cd aquabit
```
Vá no arquivo (/aquabit/settings.py) e configure seu banco de dados no campo DATABASES.
Execute o prompt de comando e vá até o diretorio (TesteAquaBit\aquabit) e execute o comando **manage.py migrate**.
Apos as migrações estiverem completas execute o comando **manage.py runserver**. Vá até a seguinte linha **Starting development server at http://127.0.0.1:8000/** e copie a url e cole no seu navegador.
