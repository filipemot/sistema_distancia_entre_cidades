package br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.repository;

import br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.model.Distancia;
import org.springframework.data.repository.CrudRepository;

import java.util.List;
import java.util.UUID;

public interface DistanciaRepository extends CrudRepository<Distancia, UUID> {
    @Override
    List<Distancia> findAll();

    List<Distancia> findAllByIdMunicipioOrigemAndIdMunicipioDestino(int idMunicipioOrigem, int idMunicipioDestino);
}
