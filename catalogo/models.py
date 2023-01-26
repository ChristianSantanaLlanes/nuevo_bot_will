from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField('Nombre', max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Anime(models.Model):
    name = models.CharField('Nombre', max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genero = models.CharField("Genero", max_length=200, default="desconocido")
    imagen = models.CharField("Foto", max_length=100, help_text="Inserte el file_id de la foto, lo puede obtener solo enviando la foto al chat del bot")
    capitulos = models.CharField("Capitulos", max_length=50, help_text="Inserte la cantidad de capitulos si no tiene capitulos inserte 'En Transmision'")
    compania = models.CharField("Compania que lo hizo", max_length=100)
    descripcion = models.TextField('Descripcion')
    date = models.DateField("Fecha de lanzamiento")

    def __str__(self) -> str:
        return self.name
