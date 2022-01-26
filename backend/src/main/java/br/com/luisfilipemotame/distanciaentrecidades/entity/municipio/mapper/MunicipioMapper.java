package br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.mapper;

import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.model.Municipio;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.dto.MunicipioDTO;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(componentModel = "spring")
public interface MunicipioMapper {
    MunicipioMapper INSTANCE = Mappers.getMapper( MunicipioMapper.class );

    MunicipioDTO municipioToMunicipioDto(Municipio municipio);

    Municipio municipioDtoToMunicipio(MunicipioDTO municipioDTO);
}
