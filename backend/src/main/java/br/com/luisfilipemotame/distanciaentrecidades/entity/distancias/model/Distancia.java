package br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.model;


import org.hibernate.annotations.GenericGenerator;

import javax.persistence.*;
import java.util.UUID;

@Entity
@Table(name="distancias" )
public class Distancia {
    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(
            name = "UUID",
            strategy = "org.hibernate.id.UUIDGenerator"
    )
    private UUID id;

    @Column(name = "id_municipio_origem")
    private int idMunicipioOrigem;

    @Column(name = "id_municipio_destino")
    private int idMunicipioDestino;

    @Column(name = "minutos")
    private Double minutos;

    @Column(name = "tempo_viagem")
    private Double tempoViagem;

    @Column(name = "milhas")
    private Double milhas;

    @Column(name = "kilometros")
    private Double kilometros;

    @Column(name = "tempo_at")
    private Double tempoAt;

    @Column(name = "tempo_andando")
    private Double tempoAndando;

    @Column(name = "tempo_caminhao")
    private Double tempoCaminhao;

    @Column(name = "tempo_viagem_caminhao")
    private Double tempoViagemCaminhao;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public int getIdMunicipioOrigem() {
        return idMunicipioOrigem;
    }

    public void setIdMunicipioOrigem(int idMunicipioOrigem) {
        this.idMunicipioOrigem = idMunicipioOrigem;
    }

    public int getIdMunicipioDestino() {
        return idMunicipioDestino;
    }

    public void setIdMunicipioDestino(int idMunicipioDestino) {
        this.idMunicipioDestino = idMunicipioDestino;
    }

    public Double getMinutos() {
        return minutos;
    }

    public void setMinutos(Double minutos) {
        this.minutos = minutos;
    }

    public Double getTempoViagem() {
        return tempoViagem;
    }

    public void setTempoViagem(Double tempoViagem) {
        this.tempoViagem = tempoViagem;
    }

    public Double getMilhas() {
        return milhas;
    }

    public void setMilhas(Double milhas) {
        this.milhas = milhas;
    }

    public Double getKilometros() {
        return kilometros;
    }

    public void setKilometros(Double kilometros) {
        this.kilometros = kilometros;
    }

    public Double getTempoAt() {
        return tempoAt;
    }

    public void setTempoAt(Double tempoAt) {
        this.tempoAt = tempoAt;
    }

    public Double getTempoAndando() {
        return tempoAndando;
    }

    public void setTempoAndando(Double tempoAndando) {
        this.tempoAndando = tempoAndando;
    }

    public Double getTempoCaminhao() {
        return tempoCaminhao;
    }

    public void setTempoCaminhao(Double tempoCaminhao) {
        this.tempoCaminhao = tempoCaminhao;
    }

    public Double getTempoViagemCaminhao() {
        return tempoViagemCaminhao;
    }

    public void setTempoViagemCaminhao(Double tempoViagemCaminhao) {
        this.tempoViagemCaminhao = tempoViagemCaminhao;
    }
}
