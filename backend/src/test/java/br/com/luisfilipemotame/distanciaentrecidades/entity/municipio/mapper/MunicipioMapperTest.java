package br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.mapper;

import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.model.Municipio;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.dto.MunicipioDTO;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

public class MunicipioMapperTest {

    @Test
    public void testMapperMunicipioToMunicipioDto() {
        Municipio municipio = new Municipio();
        municipio.setId(UUID.randomUUID());
        municipio.setIdReferencia(1);
        municipio.setNome("Municipio 1");
        municipio.setCodigoIbge(1005);
        municipio.setLatitude(-45.0);
        municipio.setLongitude(-25.0);
        municipio.setCapital(true);
        municipio.setUf("SP");
        municipio.setDdd(11);

        MunicipioDTO tipoContaDTO = MunicipioMapper.INSTANCE.municipioToMunicipioDto(municipio);
        asserts(municipio, tipoContaDTO);
    }


    @Test
    public void testMapperTipoContaDTOToTipoConta() {
        MunicipioDTO municipioDTO = new MunicipioDTO();
        municipioDTO.setId(UUID.randomUUID());
        municipioDTO.setIdReferencia(1);
        municipioDTO.setNome("Municipio 1");
        municipioDTO.setCodigoIbge(1005);
        municipioDTO.setLatitude(-45.0);
        municipioDTO.setLongitude(-25.0);
        municipioDTO.setCapital(true);
        municipioDTO.setUf("SP");
        municipioDTO.setDdd(11);


        Municipio municipio = MunicipioMapper.INSTANCE.municipioDtoToMunicipio(municipioDTO);
        asserts(municipio, municipioDTO);
    }

    private void asserts(Municipio municipio, MunicipioDTO municipioDTO) {
        assertThat(municipioDTO).isNotNull();
        assertThat(municipioDTO.getId()).isEqualTo(municipio.getId());
        assertThat(municipioDTO.getIdReferencia()).isEqualTo(municipio.getIdReferencia());
        assertThat(municipioDTO.getNome()).isEqualTo(municipio.getNome());
        assertThat(municipioDTO.getCodigoIbge()).isEqualTo(municipio.getCodigoIbge());
        assertThat(municipioDTO.getLatitude()).isEqualTo(municipio.getLatitude());
        assertThat(municipioDTO.getLongitude()).isEqualTo(municipio.getLongitude());
        assertThat(municipioDTO.getCapital()).isEqualTo(municipio.getCapital());
        assertThat(municipioDTO.getUf()).isEqualTo(municipio.getUf());
        assertThat(municipioDTO.getDdd()).isEqualTo(municipio.getDdd());
    }
}
