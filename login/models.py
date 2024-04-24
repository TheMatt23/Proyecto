from django.db import models

# Modelo para Admin
class Admin(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    celular = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo para Paciente
class Paciente(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    celular = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo para Fisioterapeuta
class Fisioterapeuta(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    celular = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo para TipoLesion
class TipoLesion(models.Model):
    lesionID = models.AutoField(primary_key=True)  # Auto-incremento
    nombreLesion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombreLesion

# Modelo para HistorialPaciente
class HistorialPaciente(models.Model):
    historialID = models.AutoField(primary_key=True)  # Auto-incremento
    cedulaPaciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    lesionID = models.ForeignKey(TipoLesion, on_delete=models.CASCADE)

# Modelo para CitaMedica
class CitaMedica(models.Model):
    citaID = models.AutoField(primary_key=True)  # Auto-incremento
    cedulaFisioterapeuta = models.ForeignKey(Fisioterapeuta, on_delete=models.CASCADE)
    cedulaPaciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)  # Se establece la fecha automáticamente

# Modelo para Terapia
class Terapia(models.Model):
    terapiaID = models.AutoField(primary_key=True)
    citaID = models.ForeignKey(CitaMedica, on_delete=models.CASCADE)
    fecha = models.DateField()
    nombre = models.CharField(max_length=255)  # Corregido el error de tipo
    cantidadTerapias = models.IntegerField()

# Modelo para Movimiento
class Movimiento(models.Model):
    movimientoID = models.AutoField(primary_key=True)
    terapiaID = models.ForeignKey(Terapia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

# Modelo para TipoEjercicio
class TipoEjercicio(models.Model):
    tipoEjercicioID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

# Modelo para Ejercicio
class Ejercicio(models.Model):
    ejercicioID = models.AutoField(primary_key=True)
    tipoEjercicioID = models.ForeignKey(TipoEjercicio, on_delete=models.CASCADE)

# Modelo para MovimientosEjercicios
class MovimientosEjercicios(models.Model):
    movimientoID = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    ejercicioID = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    porcentaje = models.FloatField()
    class Meta:
        unique_together = ('movimientoID', 'ejercicioID')  # Para la clave primaria compuesta

# Modelo para Resultados
class Resultados(models.Model):
    resultadoID = models.AutoField(primary_key=True)  # Clave primaria única
    movimientoID = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    cantidadPos = models.IntegerField()
    cantidadNeg = models.IntegerField()
    porcentaje = models.FloatField()
