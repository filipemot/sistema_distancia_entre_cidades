package br.com.luisfilipemotame.distanciaentrecidades.entity.distancia.mapper;

import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.mapper.DistanciaMapper;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.model.Distancia;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.dto.DistanciaDTO;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

public class DistanciaMapperTest {

    @Test
    public void testMapperDistanciaToDistanciaDto() {
        Distancia distancia = new Distancia();
        distancia.setId(UUID.randomUUID());
        distancia.setIdMunicipioOrigem(1);
        distancia.setIdMunicipioDestino(2);
        distancia.setMinutos(1D);
        distancia.setTempoViagem(2D);
        distancia.setMilhas(3D);
        distancia.setKilometros(4D);
        distancia.setTempoAt(5D);
        distancia.setTempoAndando(6D);
        distancia.setTempoCaminhao(7D);
        distancia.setTempoViagemCaminhao(8D);

        DistanciaDTO distanciaDTO = DistanciaMapper.INSTANCE.distanciaToDistanciaDto(distancia);
        asserts(distancia, distanciaDTO);
    }


    @Test
    public void testMapperDistanciaDTOToDistancia() {
        DistanciaDTO distanciaDTO = new DistanciaDTO();
        distanciaDTO.setId(UUID.randomUUID());
        distanciaDTO.setIdMunicipioOrigem(1);
        distanciaDTO.setIdMunicipioDestino(2);
        distanciaDTO.setMinutos(1D);
        distanciaDTO.setTempoViagem(2D);
        distanciaDTO.setMilhas(3D);
        distanciaDTO.setKilometros(4D);
        distanciaDTO.setTempoAt(5D);
        distanciaDTO.setTempoAndando(6D);
        distanciaDTO.setTempoCaminhao(7D);
        distanciaDTO.setTempoViagemCaminhao(8D);


        Distancia distancia = DistanciaMapper.INSTANCE.distanciaDtoToDistancia(distanciaDTO);
        asserts(distancia, distanciaDTO);
    }

    private void asserts(Distancia distancia, DistanciaDTO distanciaDTO) {
        assertThat(distanciaDTO).isNotNull();
        assertThat(distanciaDTO.getId()).isEqualTo(distancia.getId());
        assertThat(distanciaDTO.getIdMunicipioOrigem()).isEqualTo(distancia.getIdMunicipioOrigem());
        assertThat(distanciaDTO.getIdMunicipioDestino()).isEqualTo(distancia.getIdMunicipioDestino());
        assertThat(distanciaDTO.getMinutos()).isEqualTo(distancia.getMinutos());
        assertThat(distanciaDTO.getTempoViagem()).isEqualTo(distancia.getTempoViagem());
        assertThat(distanciaDTO.getMilhas()).isEqualTo(distancia.getMilhas());
        assertThat(distanciaDTO.getKilometros()).isEqualTo(distancia.getKilometros());
        assertThat(distanciaDTO.getTempoAt()).isEqualTo(distancia.getTempoAt());
        assertThat(distanciaDTO.getTempoAndando()).isEqualTo(distancia.getTempoAndando());
        assertThat(distanciaDTO.getTempoCaminhao()).isEqualTo(distancia.getTempoCaminhao());
        assertThat(distanciaDTO.getTempoViagemCaminhao()).isEqualTo(distancia.getTempoViagemCaminhao());
    }
}
