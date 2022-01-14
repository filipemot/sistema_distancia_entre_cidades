# Sistema de Distância entre Cidades - Script Python

Script para geração da Matriz de Distância entre todas as cidades

**Dependência**

- arcpy
- psycopg2

**Dados de Cidades**

Lat/Lng das Cidades em planilha disponibilizada no GitHub: [https://github.com/kelvins/Municipios-Brasileiros](https://github.com/kelvins/Municipios-Brasileiros)

No diretório data disponibilizo a planilha de Municípios e Estados, que serão utilizados para criação da Matriz de Distância

**Base de Arruamento**

Estamos utilizando para a Geração o Open Street Map Premium

**Licença**

- ArcGIS com extensão Network Analytics
- Open Street Map Premium

**Solução**

1. Importação da planilha excel de estados em Feature. Essa importação é utilizada para a informação de UF na tabela de Municipios
2. Importação da planilha de municipios em Feature
3. Criação do campo de UF na Feature de Municipios
4. Criação do campo de ID na Feature de Municipios para ser o ID de Referência, na Matriz de Distância
5. Criação do campo de Lat na Feature de Municipios, necessário para a conversão do dado importando que vem string, porém para esse dado precisa ser em número
6. Criação do campo de Lng na Feature de Municipios, necessário para a conversão do dado importando que vem string, porém para esse dado precisa ser em número
7. Salvar as informações de UF’s na tabela de municipios
8. Converter a Feature de Municipios em Feature de Ponto
9. Gravar na tabela do Postgree as Informações de Municipios
10. Deletar todas as informações de distancia no Postgree
11. Deletar do GeoDatabase, todo os datasets de Matriz de Distância
12. Criação do Layer de Matriz de Distância
13. Adicionar no Layer de Matriz de Distâncias as Informações de Origens
14. Adicionar no Layer de Matriz de Distâncias as Informações de Destinos
15. Executar a Matriz de Distância
16. Copiar os dados de Resultados para uma Feature
17. Remover todos os datasets
18. Gravar as informações de Distância no Postgree
19. Remoção das Features Temporárias

**Configuração**

No arquivo config.json, tem as informações configuráveis para execução

- **workspace:** FileGeoDatabase que será executado as interações com o arcgis
- **excel_city:** Excel com as informações de Municipios
- **excel_states:** Excel com as informações de Estados
- **route:** Localização do Network Dataset com as informações da base de Arruamento
- **execution/clear_state: 0/1 - Para Executar Leitura de Estado**
- **execution/clear_city: 0/1 - Para Executar Geração de Municipios**
- **execution/clear_distance: 0/1 - Para Executar Geração de Matriz de Distância**
- **execution/save_distance: 0/1 - Para Executar Gravação dos Dados de Distância no Postgree**

```json
{
  "workspace": "D:\\ProjetosPessoais\\sistema_distancia_entre_cidades\\arcgis_project\\SistemaDistanciaEntreCidades\\SistemaDistanciaEntreCidades.gdb",
  "excel_city": "D:\\ProjetosPessoais\\sistema_distancia_entre_cidades\\python\\data\\Municipios.xlsx",
  "excel_states": "D:\\ProjetosPessoais\\sistema_distancia_entre_cidades\\python\\data\\Estados.xlsx",
  "route": "C:\\Esri\\Open Street Map\\Dados\\FGDB\\StreetMap_Data\\LatinAmerica.gdb\\Routing\\Routing_ND",
  "execution": {
    "clear_state": 0,
    "clear_city": 0,
    "clear_distance": 0,
    "save_distance": 1
  }
}
```

**Configuração Banco de Dados**

No arquivo database.ini, tem as informações de configuração com o Banco de Dados:

[postgresql]

host = localhost

database = distanciaentrecidades

user = postgres

password = postgres

port = 5434

**Tabelas**

As tabelas do banco de dados são geradas pelo projeto do backend. Mas se precisar segue os scripts para criação das tabelas:

```sql
-- public.distancias definition

-- Drop table

-- DROP TABLE public.distancias;

CREATE TABLE public.distancias (
	id uuid NOT NULL,
	id_municipio_origem int4 NULL,
	id_municipio_destino int4 NULL,
	minutos float8 NULL,
	tempo_viagem float8 NULL,
	milhas float8 NULL,
	kilometros float8 NULL,
	tempo_at float8 NULL,
	tempo_andando float8 NULL,
	tempo_caminhao float8 NULL,
	tempo_viagem_caminhao float8 NULL,
	CONSTRAINT distancias_id_pk PRIMARY KEY (id)
);
CREATE INDEX distancias_id_municipio_destino ON public.distancias USING btree (id_municipio_destino);
CREATE INDEX distancias_id_municipio_origem ON public.distancias USING btree (id_municipio_origem);
CREATE INDEX distancias_id_municipio_origem_id_municipio_destino ON public.distancias USING btree (id_municipio_origem, id_municipio_destino);
```


```sql
-- public.municipios definition

-- Drop table

-- DROP TABLE public.municipios;

CREATE TABLE public.municipios (
	id uuid NOT NULL,
	id_referencia int4 NULL,
	nome varchar(255) NULL,
	codigo_ibge int4 NULL,
	latitude float8 NULL,
	longitude float8 NULL,
	capital bool NULL,
	uf varchar(2) NULL,
	ddd int4 NULL,
	CONSTRAINT municipios_id_pk PRIMARY KEY (id)
);
```

