"""
Configuración centralizada para FollowTracker
"""

# Configuración de la aplicación
APP_TITLE = "FollowTracker"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Gestor de interacciones en redes sociales"

# Configuración de la ventana
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Configuración de archivos
DATA_FILE = "follows.yaml"
BACKUP_FILE = "follows_backup.yaml"

# Configuración de la interfaz
FONT_FAMILY = "Arial"
FONT_SIZE_TITLE = 16
FONT_SIZE_NORMAL = 10
FONT_SIZE_BOLD = 12

# Colores
COLORS = {
    'background': '#f0f0f0',
    'primary': '#007acc',
    'secondary': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Estados de usuario
USER_STATES = {
    'seguido': 'Lo sigues pero él/ella no te sigue',
    'mutuo': 'Se siguen mutuamente',
    'no_seguido': 'No lo sigues',
    'te_sigue': 'Él/ella te sigue pero tú no lo sigues',
    'seguido_previamente': 'Lo seguiste en el pasado pero ya no lo sigues'
}

# Tipos de eventos
EVENT_TYPES = {
    'seguido': 'Cuando sigues a alguien',
    'follow_back': 'Cuando alguien te sigue de vuelta',
    'dejado_de_seguir': 'Cuando dejas de seguir a alguien'
}

# Configuración de redes sociales
SOCIAL_NETWORKS = {
    'instagram': {
        'name': 'Instagram',
        'url_template': 'https://instagram.com/{username}',
        'icon': '📷'
    }
}

# Configuración de la tabla
TABLE_COLUMNS = {
    'username': {
        'text': 'Usuario',
        'width': 200,
        'anchor': 'w'
    },
    'estado': {
        'text': 'Estado',
        'width': 150,
        'anchor': 'center'
    },
    'fecha_primer_seguimiento': {
        'text': 'Primer Seguimiento',
        'width': 150,
        'anchor': 'center'
    },
    'fecha_ultima_interaccion': {
        'text': 'Última Interacción',
        'width': 150,
        'anchor': 'center'
    }
}

# Configuración de filtros
FILTER_OPTIONS = [
    ("todos", "Todos los usuarios"),
    ("seguido", "Solo seguidos"),
    ("mutuo", "Solo mutuos"),
    ("no_seguido", "No seguidos"),
    ("te_sigue", "Te siguen"),
    ("seguido_previamente", "Seguidos previamente")
]

# Mensajes de la aplicación
MESSAGES = {
    'welcome': 'Bienvenido a FollowTracker',
    'user_not_found': 'Usuario no encontrado',
    'user_added': 'Usuario agregado exitosamente',
    'event_added': 'Evento registrado exitosamente',
    'data_saved': 'Datos guardados correctamente',
    'data_load_error': 'Error al cargar datos',
    'data_save_error': 'Error al guardar datos',
    'invalid_username': 'Nombre de usuario inválido',
    'confirm_delete': '¿Estás seguro de que quieres eliminar este usuario?',
    'no_events': 'No hay eventos registrados para este usuario'
}

# Configuración de validación
VALIDATION = {
    'min_username_length': 1,
    'max_username_length': 30,
    'allowed_chars': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._'
} 