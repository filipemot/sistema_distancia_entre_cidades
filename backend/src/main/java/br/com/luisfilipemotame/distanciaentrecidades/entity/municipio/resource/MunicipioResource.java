package br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.resource;

import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.MunicipioService;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.dto.MunicipioDTO;
import javassist.NotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/municipios")
public class MunicipioResource {

    private final MunicipioService municipioService;

    @GetMapping
    public List<MunicipioDTO> list() {
        return this.municipioService.findAll();
    }

    public MunicipioResource(MunicipioService tipoContaService){
        this.municipioService = tipoContaService;
    }

    @GetMapping("/{id}")
    public MunicipioDTO findById(@PathVariable UUID id) {
        MunicipioDTO municipioDTO;
        try {
            municipioDTO = this.municipioService.findById(id);
        } catch (NotFoundException e) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, e.getMessage()
            );
        }

        return municipioDTO;
    }

    @PostMapping
    public ResponseEntity<MunicipioDTO> save(@RequestBody MunicipioDTO tipoConta) {

        MunicipioDTO municipioDTO = this.municipioService.save(tipoConta);

        return new ResponseEntity<>(municipioDTO, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public MunicipioDTO update(@PathVariable UUID id, @RequestBody MunicipioDTO tipoConta) {
        MunicipioDTO municipioDTO;
        try {
            municipioDTO = this.municipioService.update(id, tipoConta);
        } catch (NotFoundException e) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, e.getMessage()
            );
        }
        return municipioDTO;
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable UUID id) {
        try {
            this.municipioService.delete(id);
        } catch (NotFoundException e) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, e.getMessage()
            );
        }
    }
}
