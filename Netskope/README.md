## Netskope Private Access REST APIs

As APIs REST do Netskope Private Access fornecem funcionalidades relacionadas aos Publishers. Abaixo estão os principais endpoints e operações disponíveis.

## Netskope Private Access REST APIs

### Instalação

Certifique-se de ter as bibliotecas necessárias instaladas em seu ambiente Python. Você pode fazer isso executando o seguinte comando:

```bash
pip3 install requests json python-dotenv
```

Certifique-se de incluir essas bibliotecas em seu script Python:

```python
import os
import requests
import json
from dotenv import load_dotenv
```

### Publishers

#### 1. [Create a Publisher](https://<tenant-URL>/apidocs/#/infrastructure/post_api_v2_infrastructure_publishers)
- Endpoint: `/api/v2/infrastructure/publishers`
- Método: `POST`
- Descrição: Crie um novo Publisher.

#### 2. [Get a Publisher](https://<tenant-URL>/apidocs/#/infrastructure/get_api_v2_infrastructure_publishers__publisher_id_)
- Endpoint: `/api/v2/infrastructure/publishers/{publisher_id}`
- Método: `GET`
- Descrição: Obtenha detalhes de um Publisher específico.

#### 3. [Get a list of Publishers](https://<tenant-URL>/apidocs/#/infrastructure/get_api_v2_infrastructure_publishers)
- Endpoint: `/api/v2/infrastructure/publishers`
- Método: `GET`
- Descrição: Obtenha uma lista de todos os Publishers.

#### 4. [Update a Publisher](https://<tenant-URL>/apidocs/#/infrastructure/put_api_v2_infrastructure_publishers__publisher_id_)
- Endpoint: `/api/v2/infrastructure/publishers/{publisher_id}`
- Método: `PUT`
- Descrição: Atualize as informações de um Publisher específico.

#### 5. [Patch a Publisher](https://<tenant-URL>/apidocs/#/infrastructure/patch_api_v2_infrastructure_publishers__publisher_id_)
- Endpoint: `/api/v2/infrastructure/publishers/{publisher_id}`
- Método: `PATCH`
- Descrição: Aplique modificações parciais a um Publisher específico.

#### 6. [Delete a Publisher](https://<tenant-URL>/apidocs/#/infrastructure/delete_api_v2_infrastructure_publishers__publisher_id_)
- Endpoint: `/api/v2/infrastructure/publishers/{publisher_id}`
- Método: `DELETE`
- Descrição: Exclua um Publisher específico.

### Autenticação

As APIs REST do Netskope usam um token de autenticação para autorizar chamadas à API. O token deve ser incluído no cabeçalho `Netskope-Api-Token` em todas as solicitações.

#### Status da API REST
O status da API REST mostra o status e permite ativar ou desativar todos os tokens da API REST para um locatário.

![Status da API REST](https://netskope-techdocs.github.io/doc-stage/en/image/uuid-704584d6-3800-f7f0-4900-fd30c5474649.png)

#### Limite de Taxa Global
Mostra a taxa de solicitações por segundo.

#### Referência
A [documentação da API Swagger](#) fornece detalhes sobre os endpoints e operações disponíveis.

### Criação de um Novo Token

Para criar um novo token:

1. Na página REST API v2, clique em "Novo Token".
   ![Criar Token](https://netskope-techdocs.github.io/doc-stage/en/image/uuid-35363d3c-66ea-7ea1-d44d-da52930a64e8.png)

2. Insira um nome para o token, defina o tempo de expiração e selecione os endpoints de API desejados.
   ![Selecionar Endpoints](https://netskope-techdocs.github.io/doc-stage/en/image/uuid-75751146-599e-a4c4-64dc-b0bc2aae1d6b.png)

3. Especifique os privilégios para cada endpoint adicionado.

4. Clique em "Salvar" quando terminar.

5. Uma caixa de confirmação será exibida; clique em "Copiar token" para armazená-lo e utilizá-lo nas solicitações de API.

![Copiar Token](https://netskope-techdocs.github.io/doc-stage/en/image/uuid-1abdf058-11cf-9343-2a41-d898e3e24901.png)

Agora você pode adicionar o token ao cabeçalho `Netskope-Api-Token` em suas solicitações de API.

<h6>Abreusz<h6>