# Aplicação Blocos CAD - Flask

Esta aplicação Flask permite aos usuários carregar arquivos de modelo DXF e pontos de coordenadas em formato TXT, processá-los e gerar um arquivo DXF com blocos adicionados nas coordenadas fornecidas.

## Requisitos

- Python 3.6 ou superior
- Flask
- ezdxf

## Instalação

1. Clone o repositório:

git clone https://github.com/seu-usuario/aplicacao-blocos-cad-flask.git

cd aplicacao-blocos-cad-flask

2. Crie um ambiente virtual e ative-o:

python3 -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate

3. Instale as dependências do projeto:

pip install -r requirements.txt

## Execução
Para executar a aplicação em ambiente de desenvolvimento, execute o seguinte comando:

flask run

A aplicação estará disponível no endereço: http://127.0.0.1:5000

## Implantação
Siga as instruções específicas do provedor de hospedagem escolhido para implantar a aplicação em um domínio público.

Licença
Esta aplicação é distribuída sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.

