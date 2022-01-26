package br.com.luisfilipemotame.distanciaentrecidades.entity.distancia.resource;

import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.resource.DistanciaResource;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.DistanciaService;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.dto.DistanciaDTO;
import com.google.gson.Gson;
import javassist.NotFoundException;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.util.Collections;
import java.util.UUID;

import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.mockito.Mockito.doThrow;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(controllers = DistanciaResource.class, excludeAutoConfiguration = SecurityAutoConfiguration.class)
public class DistanciaResourceTest {
    @Autowired
    MockMvc mvc;

    @MockBean
    DistanciaService distanciaService;

    private final UUID UUID_TEST  = UUID.randomUUID();

    @Test
    public void testPesquisaPorDistanciaComIdIgualUUIDTest() throws Exception {
        DistanciaDTO municipioDTO = getDistanciaDTO();

        Mockito.when(distanciaService.findById(UUID_TEST))
                .thenReturn(municipioDTO);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.get("/api/distancias/" + UUID_TEST)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isOk(), true);
    }

    @Test
    public void testPesquisaPorDistanciaDistanciaNaoEncontrada() throws Exception {
        UUID uuid = UUID.randomUUID();

        Mockito.when(distanciaService.findById(uuid))
                .thenThrow(NotFoundException.class);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.get("/api/distancias/"+uuid)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound());
        assertsRequest(result, status().isNotFound(), false);
    }

    @Test
    public void testSalvarDistancia() throws Exception {
        DistanciaDTO distancia = getDistanciaDTO();
        String requestJson = getJson(distancia);

        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Mockito.when(distanciaService.save(Mockito.any(DistanciaDTO.class)))
                .thenReturn(distanciaDTO);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.post("/api/distancias")
                        .content(requestJson)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isCreated(), true);
    }

    @Test
    public void testAtualizarDistanciaComDistanciaEncontrada() throws Exception {
        DistanciaDTO distancia = getDistanciaDTO();
        String requestJson = getJson(distancia);

        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Mockito.when(distanciaService.update(Mockito.any(UUID.class), Mockito.any(DistanciaDTO.class)))
                .thenReturn(distanciaDTO);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.put("/api/distancias/" + UUID_TEST)
                        .content(requestJson)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isOk(), true);
    }

    @Test
    public void testAtualizarDistanciaNaoEncontrada() throws Exception {
        DistanciaDTO distanciaDTO = getDistanciaDTO();
        String requestJson = getJson(distanciaDTO);
        Mockito.when(distanciaService.update(Mockito.any(UUID.class), Mockito.any(DistanciaDTO.class)))
                .thenThrow(NotFoundException.class);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.put("/api/distancias/" + UUID_TEST)
                        .content(requestJson)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isNotFound(), false);
    }

    @Test
    public void testDeletarPorDistanciaComIdIgualUUIDTest() throws Exception {
        Mockito.doNothing().when(distanciaService).delete(Mockito.any(UUID.class));

        ResultActions result = mvc.perform(MockMvcRequestBuilders.delete("/api/distancias/" + UUID_TEST)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isOk(), false);
    }

    @Test
    public void testDeletarPorDistanciaComDistanciaNaoEncontrada() throws Exception {
        doThrow(NotFoundException.class).when(distanciaService).delete(Mockito.any(UUID.class));

        ResultActions result = mvc.perform(MockMvcRequestBuilders.delete("/api/distancias/" + UUID_TEST)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isNotFound(), false);
    }

    @Test
    public void testPesquisaTodosDistancias() throws Exception {
        DistanciaDTO distanciaDTO = getDistanciaDTO();

        Mockito.when(distanciaService.findAll())
                .thenReturn(Collections.singletonList(distanciaDTO));

        mvc.perform(MockMvcRequestBuilders.get("/api/distancias")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(content()
                        .contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].idMunicipioOrigem", is(1)))
                .andExpect(jsonPath("$[0].idMunicipioDestino", is(2)))
                .andExpect(jsonPath("$[0].minutos", is(1.0)))
                .andExpect(jsonPath("$[0].tempoViagem", is(2.0)))
                .andExpect(jsonPath("$[0].milhas", is(3.0)))
                .andExpect(jsonPath("$[0].kilometros", is(4.0)))
                .andExpect(jsonPath("$[0].tempoAt", is(5.0)))
                .andExpect(jsonPath("$[0].tempoAndando", is(6.0)))
                .andExpect(jsonPath("$[0].tempoCaminhao", is(7.0)))
                .andExpect(jsonPath("$[0].tempoViagemCaminhao", is(8.0)));
    }

    private void assertsRequest(ResultActions result, ResultMatcher status, Boolean isContent) throws Exception {

        if (isContent) {
            result.andExpect(status)
                    .andExpect(content()
                            .contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.id", is(UUID_TEST.toString())))
                    .andExpect(jsonPath("$.idMunicipioOrigem", is(1)))
                    .andExpect(jsonPath("$.idMunicipioDestino", is(2)))
                    .andExpect(jsonPath("$.minutos", is(1.0)))
                    .andExpect(jsonPath("$.tempoViagem", is(2.0)))
                    .andExpect(jsonPath("$.milhas", is(3.0)))
                    .andExpect(jsonPath("$.kilometros", is(4.0)))
                    .andExpect(jsonPath("$.tempoAt", is(5.0)))
                    .andExpect(jsonPath("$.tempoAndando", is(6.0)))
                    .andExpect(jsonPath("$.tempoCaminhao", is(7.0)))
                    .andExpect(jsonPath("$.tempoViagemCaminhao", is(8.0)));
        } else {
            result.andExpect(status);
        }
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

    private String getJson(DistanciaDTO distanciaDTO) {
        Gson gson = new Gson();
        return gson.toJson(distanciaDTO);
    }

}
