package br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service;

import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.mapper.MunicipioMapper;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.model.Municipio;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.repository.MunicipioRepository;
import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.service.dto.MunicipioDTO;

import javassist.NotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class MunicipioService {

    private final MunicipioRepository municipioRepository;

    private final MunicipioMapper municipioMapper;

    public MunicipioService(MunicipioMapper municipioMapper, MunicipioRepository municipioRepository) {
        this.municipioMapper = municipioMapper;
        this.municipioRepository = municipioRepository;
    }

    public MunicipioDTO save(MunicipioDTO municipioDTO) {
        Municipio municipio = municipioMapper.municipioDtoToMunicipio(municipioDTO);

        municipio = municipioRepository.save(municipio);

        return municipioMapper.municipioToMunicipioDto(municipio);
    }

    public MunicipioDTO update(UUID id, MunicipioDTO municipioDTO) throws NotFoundException {

        Municipio municipioSaved = getMunicipio(id);
        Municipio municipio = municipioMapper.municipioDtoToMunicipio(municipioDTO);
        municipio.setId(municipioSaved.getId());

        Municipio municipioUpdated = municipioRepository.save(municipio);
        municipioDTO = municipioMapper.municipioToMunicipioDto(municipioUpdated);

        return municipioDTO;
    }

    public List<MunicipioDTO> findAll() {
        List<Municipio> listMunicipio = municipioRepository.findAll();
        List<MunicipioDTO> listMunicipioDto = new ArrayList<>();

        for (Municipio municipio : listMunicipio) {
            listMunicipioDto.add(municipioMapper.municipioToMunicipioDto(municipio));
        }

        return listMunicipioDto;
    }

    public void delete(UUID id) throws NotFoundException {
        Municipio municipio = getMunicipio(id);
        municipioRepository.delete(municipio);
    }

    public MunicipioDTO findById(UUID id) throws NotFoundException {
        Municipio municipio = getMunicipio(id);

        return municipioMapper.municipioToMunicipioDto(municipio);
    }

    private Municipio getMunicipio(UUID id) throws NotFoundException {
        Optional<Municipio> optionalMunicipio = municipioRepository.findById(id);

        if (!optionalMunicipio.isPresent()) {
            throw new NotFoundException("Municipio não encontrado");
        }

        return optionalMunicipio.get();
    }

}
