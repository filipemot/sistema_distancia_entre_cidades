
# Sistema de Distância entre Cidades - Backend



**Última Atualização:** 26/01/2022

**Tecnologias Utilizadas:**

- **Backend:** Java com Spring Boot
- **Infraestrutura:** Docker
- **Banco de Dados:** Postgre

**Início do Projeto:** Janeiro de 2022

**Execução**

**Banco/Docker**

Entrar em backend/docker

```  
docker-compose -f banco_docker_compose.yml up -d  
```  

**Configuração Banco**

Entrar em backend/src/main/resources/application.properties

```yaml  
spring.datasource.url=jdbc:postgresql://localhost:5432/distanciaentrecidades  
spring.datasource.username=postgres  
spring.datasource.password=postgres  
```  

**Criação da Imagem da Aplicação em Container**

- Compilar Projeto: `mvn clean package`
- Criar Imagem do Container: `docker build -f Dockerfile . -t sistema_distancia_entre_cidades`

**Criação do Container**

- Entrar na pasta backend/docker
- Executar `docker-compose -f aplicacao.yml down`

# API's Disponibilizadas

## Municipios

**Listar Todos**

**GET** [http://localhost:8080/api/municipios](http://localhost:8080/api/municipios)

**Pesquisar por ID**

**GET** [http://localhost:8080/api/municipios/{id}](http://localhost:8080/api/municipios/%7Bid%7D)

**Salvar**

**POST** [http://localhost:8080/api/municipios](http://localhost:8080/api/municipios)

**Body**

```json  
{  
	 "idReferencia":1, 
	 "nome":"Municipio 1", 
	 "codigoIbge": 1005, 
	 "latitude": -45.5, 
	 "longitude": -25.50,
	 "capital": false, 
	 "uf": "SP", 
	 "ddd": 11 
}  
```  

**Atualizar**

**PUT** [http://localhost:8080/api/municipios/{id}](http://localhost:8080/api/municipios/%7Bid%7D)

**Body**

```json  
{  
	 "idReferencia":1, 
	 "nome":"Municipio 1", 
	 "codigoIbge": 1005, 
	 "latitude": -45.5, 
	 "longitude": -25.50,
	 "capital": false, 
	 "uf": "SP", 
	 "ddd": 11 
}  
```  

**Deletar**

**DEL** [http://localhost:8080/api/municipios/{id}](http://localhost:8080/api/municipios/%7Bid%7D)


## Distancias

**Listar Todos**

**GET** [http://localhost:8080/api/distancias](http://localhost:8080/api/distancias)

**Pesquisar por ID**

**GET** [http://localhost:8080/api/distancias/{id}](http://localhost:8080/api/distancias/%7Bid%7D)

**Salvar**

**POST** [http://localhost:8080/api/distancias](http://localhost:8080/api/distancias)

**Body**

```json  
{  
	 "idMunicipioOrigem":1, 
	 "idMunicipioDestino":2, 
	 "minutos": 1.0, 
	 "tempoViagem": 2.0, 
	 "milhas": 3.0,
	 "kilometros": 4,0, 
	 "tempoAt": 5,0, 
	 "tempoAndando": 6.0, 
	 "tempoCaminhao": 7.0, 
	 "tempoViagemCaminhao": 8.0
} 
```  

**Atualizar**

**PUT** [http://localhost:8080/api/distancias/{id}](http://localhost:8080/api/distancias/%7Bid%7D)

**Body**

```json  
{  
	 "idMunicipioOrigem":1, 
	 "idMunicipioDestino":2, 
	 "minutos": 1.0, 
	 "tempoViagem": 2.0, 
	 "milhas": 3.0,
	 "kilometros": 4,0, 
	 "tempoAt": 5,0, 
	 "tempoAndando": 6.0, 
	 "tempoCaminhao": 7.0, 
	 "tempoViagemCaminhao": 8.0
}  
```  

**Deletar**

**DEL** [http://localhost:8080/api/distancias/{id}](http://localhost:8080/api/distancias/%7Bid%7D)

**Listar Distancias Por Origem e Destino**

**GET** [http://localhost:8080/api/distancias/{idOrigem}/{idDestino}](http://localhost:8080/api/distancias/%7BidOrigem%7D/%7BidDestino%7D)
  