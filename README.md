# Projeto1-Nginx

## Sobre o Projeto

Este projeto tem como objetivo configurar um servidor web na AWS com monitoramento automático, utilizando uma instância EC2 com Ubuntu Server 24.04 LTS para instalar o Nginx. Será criada uma VPC com sub-redes públicas e privadas, além de uma página HTML para testes. Para garantir a continuidade e a disponibilidade do serviço, será implementado um script de monitoramento personalizado que verifica o status do Nginx a cada 1 minuto, enviando uma mensagem para o Discord mostrando se está ONLINE ou OFFLINE.

## Sumário


## 2. Configuração do Ambiente Virtual

Para começar, precisamos criar e configurar uma VPC (Virtual Private Cloud) dedicada ao projeto.

### 2.1 Configuração dos Recursos
 
1. No console AWS, acesse o serviço VPC e clique em **Criar VPC**.

2. Em "**Geração automática de etiqueta de nome**", deixe marcado para gerar os nomes automaticamente.

3. Aqui vai ter 2 fotos mostrando configuração

4. No campo de entrada, digite a etiqueta que deseja utilizar como prefixo para o nome dos recursos que serão criados.

5. Configure os recursos: 

    - CIDR da VPC: 10.0.0.0/24 (fornece 256 endereços IP, suficiente para o projeto)
    - Número de zonas de disponibilidade (AZs): 1 
    - Número de sub-redes públicas: 1 
    - Número de sub-redes privadas: 0 
    - Gateway NAT: Nenhuma
    - VPC endpoints: Nenhuma 

6. Opcionalmente, adicione tags descritivas à VPC. Isso ajuda a identificar facilmente os recursos associados ao projeto.

## 2.2 Criação da VPC 

1. Clique em "**Criar VPC**" e aguarde a criação dos recursos.

2. O assistente criará automaticamente:

    - Uma VPC com DNS hostnames habilitado
    - Uma sub-rede pública na AZ selecionada
    - Um gateway de internet anexado à VPC
    - Uma tabela de rota configurada com rota para o gateway de internet
    - Um grupo de segurança padrão

#### Preview do VPC Workflow

![VPC Workflow](../imgs/nginx-vpc-workflow.png)

## 3. Configuração e Criação da Instância EC2

Criaremos uma instância EC2 utilizando uma AMI do Ubuntu Server 24.04 LTS e iremos configurar um IP elástico para garantir um endereço consistente ao servidor nginx na instância. Além disso, iremos configurar regras específicas de entrada e saída no grupo de segurança da instância. A porta SSH (22) será limitada apenas ao seu IP para garantir acesso à instância de maneira segura e a porta HTTP (80) será aberta para qualquer IP (0.0.0.0/0) para que o servidor nginx seja acessível publicamente. Por fim, manteremos o tráfego de saída liberado para permitir que o servidor faça download de atualizações e pacotes necessários durante a instalação e operação do nginx.

### 3.1 Configuração do Grupo de Segurança 

1. Na aba de serviços, clique em "**EC2**".

2. No painel EC2, na seção "**Rede e Segurança**", clique em "**Grupos de segurança**".

3. Localize o grupo de segurança criado pela sua VPC (procure pelo grupo de segurança associado ao ID da sua VPC no painel de informações), e clique nele para editar.

4. Clique em editar as regras de entrada (Inbound rules).

5. Adicione uma regra para o **SSH**:

    - Tipo: SSH
    - Porta: 22
    - Tipo de origem: seu endereço de IP (use "**Meu IP**" para adicionar automaticamente)

6. Adicione uma regra para o **HTTP**:

    - Tipo: HTTP
    - Porta: 80
    - Tipo de origem: qualquer local-ipv4 (0.0.0.0/0)

7. Verifique as regras de saída (Outbound rules):

    - Mantenha a regra padrão que permite todo tráfego (0.0.0.0/0)

### 3.2 Criação da Instância

1. Na página principal do EC2, clique em "**Executar instância**".

2. Configurações gerais da instância:

    - Crie tags descritivas associadas ao projeto para facilitar o gerenciamento da instância no futuro.

    - Selecione a AMI do **Ubuntu Server 24.04 LTS**.

    - No **tipo de instância**, selecione a **t2.micro**. Para o caso de utilização do projeto, os recursos da t2.micro serão suficientes. Além disto, ela está inclusa no nível gratuito da AWS.

    - Crie um par de chaves ou selecione um par de chaves já existente. Elas serão necessárias para acessar a instância via SSH.

3. Configurações de rede da instância:

    - Em "**VPC**", selecione a VPC criada anteriormente para o projeto.

    - Em "**sub-rede**", selecione a sub-rede criada com a VPC.

    - Habilite a **atribuição de IP público automaticamente**.

    - Em "**Grupos de segurança comuns**", selecione o grupo de segurança criado com a VPC.

4. Mantenha as configurações de armazenamento padrões.

2. Revise as configurações. Caso esteja tudo correto, clique em "**Executar instância**".

### 3.3 Alocação do IP Elástico

1. No painel EC2, na seção "**Rede e Segurança**", navegue até "**IPs elásticos**".

2. Clique em "**Alocar endreço de IP elástico**".

3. Utilize o conjunto de endereços IPv4 da Amazon.

4. Se desejar, adicione tags descritivas associadas ao projeto.

5. Após criado, selecione o IP, clique em "**Ações**" e "**Associar endereço de IP elástico**".

6. Selecione a instância do servidor.

7. Clique em "**Associar**".

## 4. Conectando à Instância

Primeiro, iremos ajustar as permissões da chave privada. Em seguida, iremos usar essa chave para estabelecer uma conexão segura via SSH com a instância.

### 4.1 Configuração da Chave SSH 

1. Use o seguinte comando para definir as permissões do seu arquivo de chave privada para que somente você possa lê-lo:

   ```bash
   chmod 400 ~/caminho/da/chave.pem
   ```

> [!IMPORTANT]
> Se você não definir essas permissões, não será possível se conectar à sua instância usando esse par de chaves, pois, por questões de segurança, o cliente SSH rejeitará a chave.

### 4.2 Conexão via SSH

1. Abra o terminal no seu computador e use o comando `ssh` para se conectar à sua instancia. Você precisará da localização da chave privada (arquivo .pem), do nome de usuário e seu DNS público, como no exemplo abaixo:

```bash
ssh -i ~/caminho/da/chave.pem ubuntu@seu-dns-publico
```

2. Na primeira vez que se conectar, você verá um aviso de fingerprint. Aceite digitando "yes" para confirmar que está se conectando ao servidor correto e salvá-lo para futuras conexões seguras. Após a conexão, algumas informações sobre a distribuição Ubuntu serão exibidas, e o prompt do shell deve ser algo como:

```bash 
ubuntu@ip-10-0-0-xx:~$
```

## 5. Instalação e Configuração do nginx

1. Abra o terminal do Ubuntu e execute o seguinte comando para garantir a instalação do pacote correto e sua versão mais recente:

```bash
sudo apt update && sudo apt upgrade -y
```

2. Instale o nginx:

```bash
sudo apt install nginx -y
```

3. Verifique o status do nginx:

```bash
sudo systemctl status nginx
