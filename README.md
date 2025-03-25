# Projeto1-Nginx

## Sobre o Projeto

Este projeto tem como objetivo configurar um servidor web na AWS com monitoramento automático, utilizando uma instância EC2 com Ubuntu Server 24.04 LTS para instalar o Nginx. Será criada uma VPC com sub-redes públicas e privadas, além de uma página HTML para testes. Para garantir a continuidade e a disponibilidade do serviço, será implementado um script de monitoramento personalizado que verifica o status do Nginx a cada 1 minuto, enviando uma mensagem para o Discord mostrando se está ONLINE ou OFFLINE.

## Sumário


## 2. Configuração do Ambiente Virtual

Para começar, precisamos criar e configurar uma VPC (Virtual Private Cloud) dedicada ao projeto.

### 2.1 Configuração dos Recursos
 
1. No console AWS, acesse o serviço VPC e clique em **Criar VPC**.

2. Em "**Geração automática de etiqueta de nome**", deixe marcado para gerar os nomes automaticamente.

3. No campo de entrada, digite a etiqueta que deseja utilizar como prefixo para o nome dos recursos que serão criados.

4. Configure os recursos: 

    - CIDR da VPC: 10.0.0.0/24 (fornece 256 endereços IP, suficiente para o projeto)
    - Número de zonas de disponibilidade (AZs): 1 
    - Número de sub-redes públicas: 1 
    - Número de sub-redes privadas: 0 
    - Gateway NAT: Nenhuma
    - VPC endpoints: Nenhuma 

5. Opcionalmente, adicione tags descritivas à VPC. Isso ajuda a identificar facilmente os recursos associados ao projeto.

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
