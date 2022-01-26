package br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service;

import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.mapper.DistanciaMapper;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.model.Distancia;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.repository.DistanciaRepository;
import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.dto.DistanciaDTO;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.model.Municipio;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.dto.MunicipioDTO;
import javassist.NotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class DistanciaService {

    private final DistanciaRepository distanciaRepository;

    private final DistanciaMapper distanciaMapper;

    public DistanciaService(DistanciaMapper distanciaMapper, DistanciaRepository distanciaRepository) {
        this.distanciaMapper = distanciaMapper;
        this.distanciaRepository = distanciaRepository;
    }

    public DistanciaDTO save(DistanciaDTO distanciaDTO) {
        Distancia municipio = distanciaMapper.distanciaDtoToDistancia(distanciaDTO);

        municipio = distanciaRepository.save(municipio);

        return distanciaMapper.distanciaToDistanciaDto(municipio);
    }

    public DistanciaDTO update(UUID id, DistanciaDTO distanciaDTO) throws NotFoundException {

        Distancia distanciaSaved = getDistancia(id);
        Distancia municipio = distanciaMapper.distanciaDtoToDistancia(distanciaDTO);
        municipio.setId(distanciaSaved.getId());

        Distancia distanciaUpdated = distanciaRepository.save(municipio);
        distanciaDTO = distanciaMapper.distanciaToDistanciaDto(distanciaUpdated);

        return distanciaDTO;
    }

    public List<DistanciaDTO> findAll() {
        List<Distancia> listDistancia = distanciaRepository.findAll();
        List<DistanciaDTO> listDistanciaDTO = new ArrayList<>();

        for (Distancia distancia : listDistancia) {
            listDistanciaDTO.add(distanciaMapper.distanciaToDistanciaDto(distancia));
        }

        return listDistanciaDTO;
    }

    public void delete(UUID id) throws NotFoundException {
        Distancia distancia = getDistancia(id);
        distanciaRepository.delete(distancia);
    }

    public DistanciaDTO findById(UUID id) throws NotFoundException {
        Distancia distancia = getDistancia(id);

        return distanciaMapper.distanciaToDistanciaDto(distancia);
    }

    private Distancia getDistancia(UUID id) throws NotFoundException {
        Optional<Distancia> optionalDistancia = distanciaRepository.findById(id);

        if (!optionalDistancia.isPresent()) {
            throw new NotFoundException("Distancia não encontrado");
        }

        return optionalDistancia.get();
    }

}
