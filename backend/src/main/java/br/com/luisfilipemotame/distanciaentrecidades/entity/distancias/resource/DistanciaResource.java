package br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.resource;

import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.DistanciaService;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.dto.DistanciaDTO;
import javassist.NotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/distancias")
public class DistanciaResource {

    private final DistanciaService distanciaService;

    @GetMapping
    public List<DistanciaDTO> list() {
        return this.distanciaService.findAll();
    }

    public DistanciaResource(DistanciaService distanciaService){
        this.distanciaService = distanciaService;
    }

    @GetMapping("/{id}")
    public DistanciaDTO findById(@PathVariable UUID id) {
        DistanciaDTO distanciaDTO;
        try {
            distanciaDTO = this.distanciaService.findById(id);
        } catch (NotFoundException e) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, e.getMessage()
            );
        }

        return distanciaDTO;
    }

    @PostMapping
    public ResponseEntity<DistanciaDTO> save(@RequestBody DistanciaDTO distanciaDTO) {

        DistanciaDTO distanciaDTOSaved = this.distanciaService.save(distanciaDTO);

        return new ResponseEntity<>(distanciaDTOSaved, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public DistanciaDTO update(@PathVariable UUID id, @RequestBody DistanciaDTO distanciaDTO) {
        DistanciaDTO distanciaDTOSaved;
        try {
            distanciaDTOSaved = this.distanciaService.update(id, distanciaDTO);
        } catch (NotFoundException e) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, e.getMessage()
            );
        }
        return distanciaDTOSaved;
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable UUID id) {
        try {
            this.distanciaService.delete(id);
        } catch (NotFoundException e) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, e.getMessage()
            );
        }
    }
}
