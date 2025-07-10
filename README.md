# FollowTracker

Una aplicación **minimalista** con interfaz gráfica escrita en **Python** para llevar un registro personal de tus interacciones en redes sociales: a quién sigues, si te dieron follow back, o si dejaste de seguir a alguien. Ideal para creadores de contenido, community managers o simplemente usuarios interesados en gestionar de forma consciente sus conexiones.

## 🧠 ¿Por qué?

Actualmente las redes sociales como Instagram no ofrecen un historial claro de:
- A quién seguiste en el pasado.
- Quién dejó de seguirte.
- Quién te dio follow back (si lo hizo en algún punto).
- A quién dejaste de seguir y luego volviste a seguir.

Esta herramienta busca llenar ese vacío, permitiéndote llevar un control manual de tus relaciones en redes sociales con una interfaz gráfica intuitiva.

## 🛠️ Tecnologías

- **Python 3.10+**
- **Tkinter** - Interfaz gráfica nativa
- **YAML** - Formato de almacenamiento de datos
- **PyYAML** - Manejo de archivos YAML

## 🚀 Funcionalidades

### ✅ Funcionalidades Actuales
- ✅ **Interfaz gráfica minimalista** y fácil de usar
- ✅ **Consulta rápida** de cuentas con estado actual
- ✅ **Registro de interacciones** con botones intuitivos
- ✅ **Enlaces directos** a perfiles de redes sociales
- ✅ **Buscador avanzado** con filtros por estado
- ✅ **Historial cronológico** de eventos por cuenta
- ✅ **Ordenamiento** por columnas (seguido, follow back, etc.)

## 📦 Instalación

### Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Instalación Local

1. **Clona el repositorio:**
```bash
git clone https://github.com/ozkar-co/followTracker.git
cd followTracker
```

2. **Crea un entorno virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecuta la aplicación:**
```bash
python main.py
```

## 🎯 Uso Rápido

### Interfaz Principal

1. **Consulta de Cuenta**: Escribe el nombre de usuario en el campo de búsqueda
2. **Estado Actual**: Ve si sigues a esa cuenta, si te dio follow back, o si ya la habias seguido antes, etc.
3. **Acciones Rápidas**: Usa los botones para registrar interacciones
4. **Enlace Directo**: Haz clic en el enlace para abrir el perfil en tu navegador

### Buscador Avanzado

- **Filtros**: Busca por estado (seguido, mutuo, no seguido)
- **Ordenamiento**: Ordena por columnas (fecha, estado, nombre)
- **Vista Completa**: Ve todas tus cuentas registradas en una tabla

## 📚 Estructura del Registro

### Formato YAML
Los datos se almacenan en un archivo `follows.yaml` con la siguiente estructura:

```yaml
- username: @ejemplo_usuario
  eventos:
    - tipo: seguido
      fecha: 2025-01-15
    - tipo: follow_back
      fecha: 2025-01-16
    - tipo: dejado_de_seguir
      fecha: 2025-02-01
  estado_actual: seguido_previamente
  fecha_primer_seguimiento: 2025-01-15
  fecha_ultima_interaccion: 2025-02-01

- username: @usuario_mutuo
  eventos:
    - tipo: seguido
      fecha: 2025-01-10
    - tipo: follow_back
      fecha: 2025-01-11
  estado_actual: mutuo
  fecha_primer_seguimiento: 2025-01-10
  fecha_ultima_interaccion: 2025-01-11
```

### Tipos de Eventos
- `seguido`: Cuando sigues a alguien
- `follow_back`: Cuando alguien te sigue de vuelta
- `dejado_de_seguir`: Cuando dejas de seguir a alguien

### Estados Posibles
- `seguido`: Lo sigues pero él/ella no te sigue
- `mutuo`: Se siguen mutuamente
- `no_seguido`: No lo sigues
- `te_sigue`: Él/ella te sigue pero tú no lo sigues
- `seguido_previamente`: Lo seguiste en el pasado pero ya no lo sigues

## 🔧 Funcionalidades Avanzadas

### Búsqueda y Filtros
- **Búsqueda por nombre**: Encuentra cuentas rápidamente
- **Filtros por estado**: Solo ver cuentas seguidas, mutuas, etc.
- **Ordenamiento**: Ordena por fecha, estado, nombre de usuario
- **Búsqueda avanzada**: Combina múltiples criterios

### Acciones Rápidas
- **Registro de interacciones**: Botones para seguir, unfollow, follow back
- **Enlaces directos**: Abre perfiles en tu navegador predeterminado
- **Historial**: Ve todas las interacciones con una cuenta

## 📊 Estadísticas Disponibles

- **Total de usuarios registrados**
- **Usuarios seguidos actualmente**
- **Usuarios que te siguen**
- **Relaciones mutuas**
- **Total dejados de seguir**
- **Tasa de follow back**

## 🛡️ Privacidad y Seguridad

- **Datos locales**: Toda la información se almacena localmente en tu dispositivo
- **Sin conexión**: No requiere conexión a internet para funcionar (excepto para abrir enlaces)
- **Control total**: Tú decides qué información registrar
- **Sin tracking**: No recopilamos ni enviamos datos a servidores externos

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres contribuir:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas de Contribución
- 🐛 Reportar bugs
- 💡 Sugerir nuevas funcionalidades
- 📝 Mejorar la documentación
- 🔧 Optimizar el código
- 🎨 Mejorar la interfaz de usuario

## 📝 Licencia 

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- A Miguelito por ser el germen de la idea
- A la comunidad de Python por las excelentes librerías
- A todos los contribuidores que han ayudado a mejorar este proyecto
- A los usuarios que han proporcionado feedback valioso

## 📞 Soporte

Si tienes problemas o preguntas:

- 📧 Email: ozodx@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/ozkar-co/followTracker/issues)
