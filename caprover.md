# Ambiente de teste

Este é um ambiente de teste para o deploy e configuração do capRover.

# Primeiro Passo:
Seguir o tutorial do Otávio Miranda <https://www.youtube.com/watch?v=UNiRHn2iusg>.

Se estiver usando o linux, provavelmente terá problemas com permissão de usuário. 
Para evitar isso faz-se necessário a adicionar a seguinte linha no arquivo docker-compose.yml
conforme indicado por este site: <https://blog.giovannidemizio.eu/2021/05/24/how-to-set-user-and-group-in-docker-compose/>

`user: "${UID}:${GID}"`

Exemplo:<br>
```
  djangoapp:
    container_name: djangoapp
#    Isso resolve o erro de falta de permissão ao criar o container
    user: "${UID}:${GID}"
    build:
      context: .
```

Ainda terá problemas quando começar a programar com o docker rodando. 
Para isso abra o terminal e de o comando `sudo chown -R $USER:$USER <caminho nome da pasta>` Assim você cogeguirá acessar a pasta e fazer modificações em tempo de execução.


# Depoly com linux e CapRover

Para subir a aplicação é necessário fazer algumas configurações conforme as documentações e <https://caprover.com/docs/cli-commands.html>, <https://gitlab.com/kamneros/caprover-django/-/tree/master?ref_type=heads>.

Vamos seguir os passos:
- instalando o npm com o `sudo apt install npm`. 
- instlando o caprover cli `sudo npm install -g caprover`
- Ir no servidor, e criar o banco de dados
- - Copie os dados do banco de dados para adicionar depois como variáveis de ambiente
- - Copie o endereço de host do banco de dados
- Crie o aplicativo para subir a sua aplicação
- - Adicione as variáveis de ambiente
- abra o terminal dentro da pasta e digite `caprover login`. 
- - Digite o nome do servidor
- - Digite a senha do Servidor 
- - Digite um nome para a conexão do servidor

Agora tem que configurar o ambiente para o deploy. Vai na pasta do aplicativo e crie o arquivo `captain-definition` e dentro dele 
coloque o sequinte código:
```
 {
  "schemaVersion": 2,
  "dockerfilePath": "./Dockerfile"
 }
```
Este será responsável para indicar o caminho do `Dockerfile` para o servidor. O arquivo `docker-compose.yml` não sará mais utilizado, pois o CapRover não consegue implementa-lo por completo.
Na documentação é mencionado que pode ser feito uma adaptação, porem ele irá reconhecer somente alguns comandos. Sendo assim, para esta aplicação, é melhor fazer cada docker separado.

Para finalizar, temos que alterar o arquivo `commands.sh`, pois o servidor já está pronto no CapRover, então não há a necessidade de saber se o banco de dados está ativo.

No caso, vamos remover as linhas do while, deixando somente as migrações e o servidor rodando
``` 
#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
```

Ultima alteração, para finalizar, é alterar a porta 8080 para a porta 80


Agora commite as alterações para poder enviar ao servidor.


Para o deploy defenitivo, abra o terminal na pasta do projeto e digite: `caprover deploy -b <nome da branch> -a <nome do aplicativo>`
- Ele irá pedir para selecionar o servidor (representado pelo token)
- será perguntado se deseja ignorar os arquivos do `.gitignore`

Se precisar refazer o deploy, pode colocar o -d no comando `caprover deploy -d` e ele fará o deploy automáticamente.


# Deploy em rede interna usando o Github Actions
<https://medium.com/@debasishkumardas5/running-github-actions-locally-a-complete-guide-for-windows-mac-and-linux-users-34c45999c7cd>