package br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service;

import br.com.luisfilipemotame.distanciaentrecidades.DistanciaentrecidadesApplication;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.mapper.MunicipioMapper;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.model.Municipio;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.repository.MunicipioRepository;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.dto.MunicipioDTO;
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
public class MunicipioServiceTest {

    @Autowired
    MunicipioService municipioService;

    @MockBean
    MunicipioRepository municipioRepository;

    @MockBean
    MunicipioMapper municipioMapper;

    private final UUID UUID_TEST  = UUID.randomUUID();


    @Test
    public void testSalvarMunicipioDTO() {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Municipio municipio = getMunicipio();

        Mockito.when(municipioMapper.municipioDtoToMunicipio(municipioDTO))
                .thenReturn(municipio);

        Mockito.when(municipioRepository.save(municipio))
                .thenReturn(municipio);

        Mockito.when(municipioMapper.municipioToMunicipioDto(municipio))
                .thenReturn(municipioDTO);

        MunicipioDTO municipioSalva = municipioService.save(municipioDTO);
        asserts(municipioDTO, municipioSalva);
    }

    @Test
    public void testAtualizarMunicipioDTOComMunicipioEncontrado() throws NotFoundException {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Municipio municipio = getMunicipio();

        Optional<Municipio> municipioOptional = Optional.of(municipio);

        Mockito.when(municipioRepository.findById(UUID_TEST))
                .thenReturn(municipioOptional);

        Mockito.when(municipioRepository.save(municipio))
                .thenReturn(municipio);

        Mockito.when(municipioMapper.municipioToMunicipioDto(municipio))
                .thenReturn(municipioDTO);

        Mockito.when(municipioMapper.municipioDtoToMunicipio(municipioDTO))
                .thenReturn(municipio);

        MunicipioDTO municipioSalva = municipioService.update(UUID_TEST, municipioDTO);
        asserts(municipioDTO, municipioSalva);
    }


    @Test
    public void testAtualizarMunicipioDTOComMunicipioDTONaoEncontrado() {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Municipio municipio = getMunicipio();

        Mockito.when(municipioRepository.findById(UUID_TEST))
                .thenReturn(Optional.empty());

        Mockito.when(municipioRepository.save(municipio))
                .thenReturn(municipio);

        Mockito.when(municipioMapper.municipioToMunicipioDto(municipio))
                .thenReturn(municipioDTO);

        try {
            municipioService.update(UUID_TEST, municipioDTO);
            fail("Falha");
        } catch (NotFoundException e) {
            assertThat(e.getMessage()).isEqualTo("municipio não encontrado");
        } catch (Exception e) {
            fail("Falha");
        }
    }

    @Test
    public void testDeletarMunicipioDTOComMunicipioEncontrado() {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Municipio municipio = getMunicipio();

        Mockito.when(municipioRepository.findById(UUID_TEST))
                .thenReturn(Optional.of(municipio));

        Mockito.when(municipioMapper.municipioToMunicipioDto(municipio))
                .thenReturn(municipioDTO);

        try {
            municipioService.delete(UUID_TEST);
        } catch (NotFoundException e) {
            fail(e.getMessage());
        }
    }

    @Test
    public void testDeletarMunicipioDTOComMunicipioNaoEncontrado() {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Municipio municipio = getMunicipio();

        Mockito.when(municipioRepository.findById(UUID_TEST))
                .thenReturn(Optional.empty());

        Mockito.when(municipioMapper.municipioToMunicipioDto(municipio))
                .thenReturn(municipioDTO);

        try {
            municipioService.delete(UUID_TEST);
            fail("Falha");
        } catch (NotFoundException e) {
            assertThat(e.getMessage()).isEqualTo("Municipio não encontrado");
        } catch (Exception e) {
            fail("Falha");
        }
    }

    @Test
    public void testPesquisaPorIdComMunicipioEncontrado() throws NotFoundException {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Municipio municipio = getMunicipio();

        Mockito.when(municipioRepository.findById(UUID_TEST))
                .thenReturn(Optional.of(municipio));

        Mockito.when(municipioMapper.municipioToMunicipioDto(municipio))
                .thenReturn(municipioDTO);

        MunicipioDTO municipioSalva = municipioService.findById(UUID_TEST);

        asserts(municipioDTO, municipioSalva);
    }

    @Test
    public void testPesquisaPorIdComMunicipioNaoEncontrado() {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Municipio municipio = getMunicipio();

        Mockito.when(municipioRepository.findById(UUID_TEST))
                .thenReturn(Optional.empty());

        Mockito.when(municipioMapper.municipioToMunicipioDto(municipio))
                .thenReturn(municipioDTO);

        try {
            municipioService.findById(UUID_TEST);
            fail("Falha");
        } catch (NotFoundException e) {
            assertThat(e.getMessage()).isEqualTo("municipio não encontrado");
        } catch (Exception e) {
            fail("Falha");
        }
    }

    @Test
    public void testPesquisaTodosMunicipios() {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Municipio municipio = getMunicipio();

        Mockito.when(municipioRepository.findAll())
                .thenReturn(Collections.singletonList(municipio));

        Mockito.when(municipioMapper.municipioToMunicipioDto(municipio))
                .thenReturn(municipioDTO);


        List<MunicipioDTO> municipioSalva = municipioService.findAll();

        assertThat(municipioSalva).isNotNull();
        assertThat(municipioSalva.size()).isEqualTo(1);
        asserts(municipioDTO, municipioSalva.get(0));
    }

    private MunicipioDTO getMunicipioDTO() {
        MunicipioDTO municipioDTO = new MunicipioDTO();
        municipioDTO.setId(UUID_TEST);
        municipioDTO.setIdReferencia(1);
        municipioDTO.setNome("Municipio 1");
        municipioDTO.setCodigoIbge(1005);
        municipioDTO.setLatitude(-45.0);
        municipioDTO.setLongitude(-25.0);
        municipioDTO.setCapital(true);
        municipioDTO.setUf("SP");
        municipioDTO.setDdd(11);
        return municipioDTO;
    }

    private Municipio getMunicipio() {
        Municipio municipio = new Municipio();
        municipio.setId(UUID_TEST);
        municipio.setIdReferencia(1);
        municipio.setNome("Municipio 1");
        municipio.setCodigoIbge(1005);
        municipio.setLatitude(-45.0);
        municipio.setLongitude(-25.0);
        municipio.setCapital(true);
        municipio.setUf("SP");
        municipio.setDdd(11);
        return municipio;
    }

    private void asserts(MunicipioDTO municipioDTO, MunicipioDTO municipio) {
        assertThat(municipio).isNotNull();
        assertThat(municipio.getId()).isNotNull();
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
