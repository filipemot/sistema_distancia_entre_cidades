package br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.repository;

import br.com.luisfilipemotame.distanciaentrecidades.entity.municipio.model.Municipio;
import org.springframework.data.repository.CrudRepository;

import java.util.List;
import java.util.UUID;

public interface MunicipioRepository extends CrudRepository<Municipio, UUID> {
    @Override
    List<Municipio> findAll();
}
