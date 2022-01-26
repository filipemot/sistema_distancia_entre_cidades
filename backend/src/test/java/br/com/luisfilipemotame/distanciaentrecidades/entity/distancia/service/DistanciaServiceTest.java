package br.com.luisfilipemotame.distanciaentrecidades.entity.distancia.service;

import br.com.luisfilipemotame.distanciaentrecidades.DistanciaentrecidadesApplication;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.mapper.DistanciaMapper;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.model.Distancia;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.repository.DistanciaRepository;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.DistanciaService;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.dto.DistanciaDTO;
import javassist.NotFoundException;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;

import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.fail;

@SpringBootTest(classes = DistanciaentrecidadesApplication.class,
        webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
public class DistanciaServiceTest {

    @Autowired
    DistanciaService distanciaService;

    @MockBean
    DistanciaRepository distanciaRepository;

    @MockBean
    DistanciaMapper distanciaMapper;

    private final UUID UUID_TEST  = UUID.randomUUID();


    @Test
    public void testSalvarDistanciaDTO() {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Mockito.when(distanciaMapper.distanciaDtoToDistancia(distanciaDTO))
                .thenReturn(distancia);

        Mockito.when(distanciaRepository.save(distancia))
                .thenReturn(distancia);

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);

        DistanciaDTO distacniaSalva = distanciaService.save(distanciaDTO);
        asserts(distanciaDTO, distacniaSalva);
    }

    @Test
    public void testAtualizarDistanciaDTOComDistanciaEncontrada() throws NotFoundException {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Optional<Distancia> distanciaOptional = Optional.of(distancia);

        Mockito.when(distanciaRepository.findById(UUID_TEST))
                .thenReturn(distanciaOptional);

        Mockito.when(distanciaRepository.save(distancia))
                .thenReturn(distancia);

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);

        Mockito.when(distanciaMapper.distanciaDtoToDistancia(distanciaDTO))
                .thenReturn(distancia);

        DistanciaDTO distanciaSalvo = distanciaService.update(UUID_TEST, distanciaDTO);
        asserts(distanciaDTO, distanciaSalvo);
    }


    @Test
    public void testAtualizarDistanciaDTOComDistanciaDTONaoEncontrada() {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Mockito.when(distanciaRepository.findById(UUID_TEST))
                .thenReturn(Optional.empty());

        Mockito.when(distanciaRepository.save(distancia))
                .thenReturn(distancia);

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);

        try {
            distanciaService.update(UUID_TEST, distanciaDTO);
            fail("Falha");
        } catch (NotFoundException e) {
            assertThat(e.getMessage()).isEqualTo("Distancia não encontrado");
        } catch (Exception e) {
            fail("Falha");
        }
    }

    @Test
    public void testDeletarDistanciaDTOComDistanciaEncontrada() {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Mockito.when(distanciaRepository.findById(UUID_TEST))
                .thenReturn(Optional.of(distancia));

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);

        try {
            distanciaService.delete(UUID_TEST);
        } catch (NotFoundException e) {
            fail(e.getMessage());
        }
    }

    @Test
    public void testDeletarDistanciaDTOComDistanciaNaoEncontrada() {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Mockito.when(distanciaRepository.findById(UUID_TEST))
                .thenReturn(Optional.empty());

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);

        try {
            distanciaService.delete(UUID_TEST);
            fail("Falha");
        } catch (NotFoundException e) {
            assertThat(e.getMessage()).isEqualTo("Distancia não encontrado");
        } catch (Exception e) {
            fail("Falha");
        }
    }

    @Test
    public void testPesquisaPorIdComDistanciaEncontrado() throws NotFoundException {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Mockito.when(distanciaRepository.findById(UUID_TEST))
                .thenReturn(Optional.of(distancia));

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);

        DistanciaDTO distanciaSalva = distanciaService.findById(UUID_TEST);

        asserts(distanciaDTO, distanciaSalva);
    }

    @Test
    public void testPesquisaPorIdComDistanciaoNaoEncontrado() {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Mockito.when(distanciaRepository.findById(UUID_TEST))
                .thenReturn(Optional.empty());

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);

        try {
            distanciaService.findById(UUID_TEST);
            fail("Falha");
        } catch (NotFoundException e) {
            assertThat(e.getMessage()).isEqualTo("Distancia não encontrado");
        } catch (Exception e) {
            fail("Falha");
        }
    }

    @Test
    public void testPesquisaTodosDistancias() {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Mockito.when(distanciaRepository.findAll())
                .thenReturn(Collections.singletonList(distancia));

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);


        List<DistanciaDTO> distanciaDTOS = distanciaService.findAll();

        assertThat(distanciaDTOS).isNotNull();
        assertThat(distanciaDTOS.size()).isEqualTo(1);
        asserts(distanciaDTO, distanciaDTOS.get(0));
    }

    @Test
    public void testPesquisaTodosDistanciasPorIdMunicipioOrigemEIdMunicipioDestino() {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Distancia distancia = getDistancia();

        Mockito.when(distanciaRepository.findAllByIdMunicipioOrigemAndIdMunicipioDestino(1, 1))
                .thenReturn(Collections.singletonList(distancia));

        Mockito.when(distanciaMapper.distanciaToDistanciaDto(distancia))
                .thenReturn(distanciaDTO);


        List<DistanciaDTO> distanciaDTOS = distanciaService.findAllByIdMunicipioOrigemAndIdMunicipioDestino(1, 1);

        assertThat(distanciaDTOS).isNotNull();
        assertThat(distanciaDTOS.size()).isEqualTo(1);
        asserts(distanciaDTO, distanciaDTOS.get(0));
    }

    private DistanciaDTO getDistanciaDTO() {
        DistanciaDTO distanciaDTO = new DistanciaDTO();
        distanciaDTO.setId(UUID_TEST);
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

        return distanciaDTO;
    }

    private Distancia getDistancia() {
        Distancia distancia = new Distancia();
        distancia.setId(UUID_TEST);
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
        return distancia;
    }

    private void asserts(DistanciaDTO distanciaDTO, DistanciaDTO distancia) {
        assertThat(distancia).isNotNull();
        assertThat(distancia.getId()).isNotNull();
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
