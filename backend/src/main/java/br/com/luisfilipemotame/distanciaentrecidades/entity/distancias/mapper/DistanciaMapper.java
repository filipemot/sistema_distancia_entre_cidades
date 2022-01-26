package br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.mapper;

import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.model.Distancia;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.dto.DistanciaDTO;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.model.Municipio;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.dto.MunicipioDTO;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(componentModel = "spring")
public interface DistanciaMapper {
    DistanciaMapper INSTANCE = Mappers.getMapper( DistanciaMapper.class );

    DistanciaDTO distanciaToDistanciaDto(Distancia distancia);

    Distancia distanciaDtoToDistancia(DistanciaDTO distanciaDTO);
}
