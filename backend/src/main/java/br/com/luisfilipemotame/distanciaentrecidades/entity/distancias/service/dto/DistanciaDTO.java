package br.com.luisfilipemotame.distanciaentrecidades.entity.distancias.service.dto;


import java.util.UUID;

public class DistanciaDTO {

    private UUID id;

    private int idMunicipioOrigem;

    private int idMunicipioDestino;

    private Double minutos;

    private Double tempoViagem;

    private Double milhas;

    private Double kilometros;

    private Double tempoAt;

    private Double tempoAndando;

    private Double tempoCaminhao;

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
