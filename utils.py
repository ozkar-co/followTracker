"""
Utilidades para FollowTracker
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
import config

def normalize_username(username: str) -> str:
    """
    Normalizar un nombre de usuario
    - Asegura que comience con @
    - Convierte a minúsculas
    - Elimina espacios extra
    """
    username = username.strip().lower()
    if not username.startswith('@'):
        username = '@' + username
    return username

def validate_username(username: str) -> tuple[bool, str]:
    """
    Validar un nombre de usuario
    Retorna (es_válido, mensaje_error)
    """
    if not username:
        return False, "El nombre de usuario no puede estar vacío"
    
    # Remover @ para validación
    clean_username = username[1:] if username.startswith('@') else username
    
    if len(clean_username) < config.VALIDATION['min_username_length']:
        return False, f"El nombre de usuario debe tener al menos {config.VALIDATION['min_username_length']} caracteres"
    
    if len(clean_username) > config.VALIDATION['max_username_length']:
        return False, f"El nombre de usuario no puede tener más de {config.VALIDATION['max_username_length']} caracteres"
    
    # Verificar caracteres permitidos
    for char in clean_username:
        if char not in config.VALIDATION['allowed_chars']:
            return False, f"El carácter '{char}' no está permitido en nombres de usuario"
    
    return True, ""

def format_date(date_str: str) -> str:
    """
    Formatear una fecha para mostrar
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        return date_str

def get_current_date() -> str:
    """
    Obtener la fecha actual en formato YYYY-MM-DD
    """
    return datetime.now().strftime("%Y-%m-%d")

def calculate_user_statistics(follows_data: List[Dict]) -> Dict[str, int]:
    """
    Calcular estadísticas de usuarios
    """
    stats = {
        'total_usuarios': len(follows_data),
        'seguidos_actualmente': 0,
        'te_siguen': 0,
        'relaciones_mutuas': 0,
        'dejados_seguir': 0,
        'no_seguidos': 0
    }
    
    for user in follows_data:
        estado = user.get('estado_actual', 'no_seguido')
        if estado == 'seguido':
            stats['seguidos_actualmente'] += 1
        elif estado == 'te_sigue':
            stats['te_siguen'] += 1
        elif estado == 'mutuo':
            stats['relaciones_mutuas'] += 1
        elif estado == 'seguido_previamente':
            stats['dejados_seguir'] += 1
        elif estado == 'no_seguido':
            stats['no_seguidos'] += 1
    
    return stats

def calculate_follow_back_rate(stats: Dict[str, int]) -> str:
    """
    Calcular tasa de follow back
    """
    total_seguidos = stats['seguidos_actualmente'] + stats['relaciones_mutuas']
    if total_seguidos > 0:
        rate = (stats['relaciones_mutuas'] / total_seguidos) * 100
        return f"{rate:.1f}%"
    return "0%"

def get_user_events_summary(user_data: Dict) -> str:
    """
    Obtener un resumen de eventos de un usuario
    """
    eventos = user_data.get('eventos', [])
    if not eventos:
        return "Sin eventos registrados"
    
    summary = []
    for evento in eventos:
        tipo = evento.get('tipo', 'desconocido')
        fecha = format_date(evento.get('fecha', ''))
        summary.append(f"{fecha}: {tipo}")
    
    return " | ".join(summary)

def get_social_network_url(username: str, network: str = 'instagram') -> str:
    """
    Generar URL para una red social específica
    """
    clean_username = username[1:] if username.startswith('@') else username
    
    if network in config.SOCIAL_NETWORKS:
        url_template = config.SOCIAL_NETWORKS[network]['url_template']
        return url_template.format(username=clean_username)
    
    # Default a Instagram
    return f"https://instagram.com/{clean_username}"

def backup_data(data: List[Dict], backup_file: str = None) -> bool:
    """
    Crear backup de los datos
    """
    if backup_file is None:
        backup_file = config.BACKUP_FILE
    
    try:
        import yaml
        with open(backup_file, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
        return True
    except Exception:
        return False

def restore_backup(backup_file: str = None) -> Optional[List[Dict]]:
    """
    Restaurar datos desde backup
    """
    if backup_file is None:
        backup_file = config.BACKUP_FILE
    
    try:
        import yaml
        with open(backup_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or []
    except Exception:
        return None

def export_to_csv(follows_data: List[Dict], filename: str) -> bool:
    """
    Exportar datos a formato CSV
    """
    try:
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['username', 'estado_actual', 'fecha_primer_seguimiento', 
                         'fecha_ultima_interaccion', 'total_eventos']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for user in follows_data:
                row = {
                    'username': user.get('username', ''),
                    'estado_actual': user.get('estado_actual', ''),
                    'fecha_primer_seguimiento': user.get('fecha_primer_seguimiento', ''),
                    'fecha_ultima_interaccion': user.get('fecha_ultima_interaccion', ''),
                    'total_eventos': len(user.get('eventos', []))
                }
                writer.writerow(row)
        return True
    except Exception:
        return False

def import_from_csv(filename: str) -> Optional[List[Dict]]:
    """
    Importar datos desde formato CSV
    """
    try:
        import csv
        data = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_data = {
                    'username': row.get('username', ''),
                    'estado_actual': row.get('estado_actual', 'no_seguido'),
                    'fecha_primer_seguimiento': row.get('fecha_primer_seguimiento', ''),
                    'fecha_ultima_interaccion': row.get('fecha_ultima_interaccion', ''),
                    'eventos': []
                }
                data.append(user_data)
        return data
    except Exception:
        return None

def get_user_by_username(follows_data: List[Dict], username: str) -> Optional[Dict]:
    """
    Buscar usuario por nombre de usuario
    """
    normalized_username = normalize_username(username)
    for user in follows_data:
        if user.get('username') == normalized_username:
            return user
    return None

def sort_users_by_criteria(follows_data: List[Dict], criteria: str = 'username', reverse: bool = False) -> List[Dict]:
    """
    Ordenar usuarios por criterio específico
    """
    if criteria == 'username':
        return sorted(follows_data, key=lambda x: x.get('username', ''), reverse=reverse)
    elif criteria == 'fecha_ultima_interaccion':
        return sorted(follows_data, key=lambda x: x.get('fecha_ultima_interaccion', ''), reverse=reverse)
    elif criteria == 'estado':
        return sorted(follows_data, key=lambda x: x.get('estado_actual', ''), reverse=reverse)
    else:
        return follows_data 