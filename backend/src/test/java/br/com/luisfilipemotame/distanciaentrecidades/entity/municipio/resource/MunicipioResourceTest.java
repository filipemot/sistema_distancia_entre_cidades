package br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.resource;

import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.MunicipioService;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.dto.MunicipioDTO;
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

@WebMvcTest(controllers = MunicipioResource.class, excludeAutoConfiguration = SecurityAutoConfiguration.class)
public class MunicipioResourceTest {
    @Autowired
    MockMvc mvc;

    @MockBean
    MunicipioService municipioService;

    private final UUID UUID_TEST  = UUID.randomUUID();

    @Test
    public void testPesquisaPorMunicipioComIdIgualUUIDTest() throws Exception {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Mockito.when(municipioService.findById(UUID_TEST))
                .thenReturn(municipioDTO);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.get("/api/municipios/" + UUID_TEST)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isOk(), true);
    }

    @Test
    public void testPesquisaPorMunicipioMunicipioNaoEncontrado() throws Exception {
        UUID uuid = UUID.randomUUID();

        Mockito.when(municipioService.findById(uuid))
                .thenThrow(NotFoundException.class);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.get("/api/municipios/"+uuid)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound());
        assertsRequest(result, status().isNotFound(), false);
    }

    @Test
    public void testSalvarMunicipio() throws Exception {
        MunicipioDTO municipio = getMunicipioDTO();
        String requestJson = getJson(municipio);

        MunicipioDTO municipioDTO = getMunicipioDTO();

        Mockito.when(municipioService.save(Mockito.any(MunicipioDTO.class)))
                .thenReturn(municipioDTO);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.post("/api/municipios")
                        .content(requestJson)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isCreated(), true);
    }

    @Test
    public void testAtualizarMunicipioComMunicipioEncontrado() throws Exception {
        MunicipioDTO municipio = getMunicipioDTO();
        String requestJson = getJson(municipio);

        MunicipioDTO municipioDTO = getMunicipioDTO();

        Mockito.when(municipioService.update(Mockito.any(UUID.class), Mockito.any(MunicipioDTO.class)))
                .thenReturn(municipioDTO);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.put("/api/municipios/" + UUID_TEST)
                        .content(requestJson)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isOk(), true);
    }

    @Test
    public void testAtualizarMunicipioNaoEncontrado() throws Exception {
        MunicipioDTO municipioDTO = getMunicipioDTO();
        String requestJson = getJson(municipioDTO);
        Mockito.when(municipioService.update(Mockito.any(UUID.class), Mockito.any(MunicipioDTO.class)))
                .thenThrow(NotFoundException.class);

        ResultActions result = mvc.perform(MockMvcRequestBuilders.put("/api/municipios/" + UUID_TEST)
                        .content(requestJson)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isNotFound(), false);
    }

    @Test
    public void testDeletarPorMunicipioComIdIgualUUIDTest() throws Exception {
        Mockito.doNothing().when(municipioService).delete(Mockito.any(UUID.class));

        ResultActions result = mvc.perform(MockMvcRequestBuilders.delete("/api/municipios/" + UUID_TEST)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isOk(), false);
    }

    @Test
    public void testDeletarPorMunicipioComMunicipioNaoEncontrado() throws Exception {
        doThrow(NotFoundException.class).when(municipioService).delete(Mockito.any(UUID.class));

        ResultActions result = mvc.perform(MockMvcRequestBuilders.delete("/api/municipios/" + UUID_TEST)
                        .contentType(MediaType.APPLICATION_JSON));
        assertsRequest(result, status().isNotFound(), false);
    }

    @Test
    public void testPesquisaTodosMunicipios() throws Exception {
        MunicipioDTO municipioDTO = getMunicipioDTO();

        Mockito.when(municipioService.findAll())
                .thenReturn(Collections.singletonList(municipioDTO));

        mvc.perform(MockMvcRequestBuilders.get("/api/municipios")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(content()
                        .contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].idReferencia", is(1)))
                .andExpect(jsonPath("$[0].nome", is("Municipio 1")))
                .andExpect(jsonPath("$[0].codigoIbge", is(1005)))
                .andExpect(jsonPath("$[0].latitude", is(-45.0)))
                .andExpect(jsonPath("$[0].longitude", is(-25.0)))
                .andExpect(jsonPath("$[0].capital", is(true)))
                .andExpect(jsonPath("$[0].uf", is("SP")))
                .andExpect(jsonPath("$[0].ddd", is(11)));
    }

    private void assertsRequest(ResultActions result, ResultMatcher status, Boolean isContent) throws Exception {

        if (isContent) {
            result.andExpect(status)
                    .andExpect(content()
                            .contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                    .andExpect(jsonPath("$.id", is(UUID_TEST.toString())))
                    .andExpect(jsonPath("$.idReferencia", is(1)))
                    .andExpect(jsonPath("$.nome", is("Municipio 1")))
                    .andExpect(jsonPath("$.codigoIbge", is(1005)))
                    .andExpect(jsonPath("$.latitude", is(-45.0)))
                    .andExpect(jsonPath("$.longitude", is(-25.0)))
                    .andExpect(jsonPath("$.capital", is(true)))
                    .andExpect(jsonPath("$.uf", is("SP")))
                    .andExpect(jsonPath("$.ddd", is(11)));

        } else {
            result.andExpect(status);
        }
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

    private String getJson(MunicipioDTO municipioDTO) {
        Gson gson = new Gson();
        return gson.toJson(municipioDTO);
    }

}
