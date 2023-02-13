from django.core.exceptions import ValidationError
from django.db import models


def validar_uf(valor):
    if len(valor) != 2:
        raise ValidationError("A UF deve ter 2 dígitos!")


def validar_regiao_geografica_intermediaria(valor):
    if len(valor) != 4:
        raise ValidationError("A região geográfica intermediária deve ter 4 dígitos!")


def validar_regiao_geografica_imediata(valor):
    if len(valor) != 6:
        raise ValidationError("A região geográfica imediata deve ter 6 dígitos!")


def validar_mesorregiao_geografica(valor):
    if (len(valor) < 1) or (len(valor) > 2):
        raise ValidationError("A mesorregião geográfica deve ter 1 ou 2 dígitos!")


def validar_microrregiao_geografica(valor):
    if (len(valor) < 1) or (len(valor) > 2):
        raise ValidationError("A microrregião geográfica deve ter 1 ou 2 dígitos!")


def validar_municipio(valor):
    if (len(valor) < 2) or (len(valor) > 5):
        raise ValidationError("O município deve ter de 2 a 5 dígitos!")


def validar_codigo_municipio_completo(valor):
    if len(valor) != 7:
        raise ValidationError("O código do município completo deve ter 7 dígitos!")


def validar_codigo_municipio_6_digitos(valor):
    if len(valor) != 6:
        raise ValidationError("O código do município de 6 dígitos deve ter 6 dígitos!")


def validar_ibge(valor):
    if len(valor) != 7:
        raise ValidationError("O número IBGE deve ter 7 dígitos!")


def validar_numero_ob(valor):
    if len(valor) != 6:
        raise ValidationError("O número OB deve ter 6 dígitos!")


def validar_banco_ob(valor):
    if len(valor) != 3:
        raise ValidationError("O banco OB deve ter 3 dígitos!")


def validar_agencia_ob(valor):
    if len(valor) != 6:
        raise ValidationError("A agência OB deve ter 6 dígitos!")


def validar_conta_ob(valor):
    if len(valor) != 10:
        raise ValidationError("A conta OB deve ter 10 dígitos!")


class Reg_Ter(models.Model):
    uf = models.PositiveIntegerField(validators=[validar_uf])
    nome_uf = models.CharField(max_length=30)
    regiao_geografica_intermediaria = models.PositiveIntegerField(validators=[validar_regiao_geografica_intermediaria])
    nome_regiao_geografica_intermediaria = models.CharField(max_length=100)
    regiao_geografica_imediata = models.PositiveIntegerField(validators=[validar_regiao_geografica_imediata])
    nome_regiao_geografica_imediata = models.CharField(max_length=100)
    mesorregiao_geografica = models.PositiveIntegerField(validators=[validar_mesorregiao_geografica])
    nome_mesorregiao = models.CharField(max_length=100)
    microrregiao_geografica = models.PositiveIntegerField(validators=[validar_microrregiao_geografica])
    nome_microrregiao = models.CharField(max_length=100)
    municipio = models.PositiveIntegerField(validators=[validar_municipio])
    codigo_municipio_completo = models.PositiveIntegerField(primary_key=True, unique=True, validators=[validar_codigo_municipio_completo])
    nome_municipio = models.CharField(max_length=100)
    codigo_municipio_6_digitos = models.PositiveIntegerField(validators=[validar_codigo_municipio_6_digitos])


class Repasse(models.Model):
    ibge = models.ForeignKey(Reg_Ter, to_field='codigo_municipio_completo', on_delete=models.CASCADE, validators=[validar_ibge])
    bloco = models.CharField(max_length=250)
    grupo = models.CharField(max_length=250)
    acao_detalhada = models.TextField()
    competencia_parcela = models.CharField(max_length=250)
    numero_ob = models.PositiveIntegerField(validators=[validar_numero_ob])
    data_ob = models.DateField()
    banco_ob = models.PositiveIntegerField(validators=[validar_banco_ob])
    agencia_ob = models.PositiveIntegerField(validators=[validar_agencia_ob])
    conta_ob = models.PositiveIntegerField(validators=[validar_conta_ob])
    valor_total = models.FloatField()
    desconto = models.FloatField()
    valor_liquido = models.FloatField()
    observacao = models.TextField()
    processo = models.PositiveBigIntegerField()
    tipo_repasse = models.CharField(max_length=250)
    numero_proposta = models.PositiveIntegerField()
