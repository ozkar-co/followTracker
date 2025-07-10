#!/usr/bin/env python3
"""
FollowTracker - Aplicación para gestionar interacciones en redes sociales
"""

import tkinter as tk
from tkinter import ttk, messagebox
import yaml
import os
from datetime import datetime
import webbrowser
from typing import Dict, List, Optional

class FollowTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FollowTracker")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar el archivo de datos
        self.data_file = "follows.yaml"
        self.follows_data = self.load_data()
        
        # Variables de control
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="todos")
        
        self.setup_ui()
        self.update_statistics()
        
    def load_data(self) -> List[Dict]:
        """Cargar datos desde el archivo YAML"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    return yaml.safe_load(file) or []
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar datos: {e}")
                return []
        return []
    
    def save_data(self):
        """Guardar datos al archivo YAML"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                yaml.dump(self.follows_data, file, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar datos: {e}")
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="FollowTracker", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Consulta de Cuenta", padding="10")
        search_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Usuario:").grid(row=0, column=0, padx=(0, 10))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        search_entry.bind('<Return>', self.search_user)
        
        ttk.Button(search_frame, text="Buscar", command=self.search_user).grid(row=0, column=2)
        
        # Frame de información de usuario
        self.user_info_frame = ttk.LabelFrame(main_frame, text="Información de Usuario", padding="10")
        self.user_info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.user_info_frame.columnconfigure(1, weight=1)
        
        # Frame de acciones
        self.actions_frame = ttk.LabelFrame(main_frame, text="Acciones", padding="10")
        self.actions_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Frame de estadísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        stats_frame.columnconfigure(1, weight=1)
        
        # Estadísticas
        self.stats_labels = {}
        stats = [
            ("Total usuarios:", "total_usuarios"),
            ("Seguidos actualmente:", "seguidos_actualmente"),
            ("Te siguen:", "te_siguen"),
            ("Relaciones mutuas:", "relaciones_mutuas"),
            ("Dejados de seguir:", "dejados_seguir"),
            ("Tasa follow back:", "tasa_follow_back")
        ]
        
        for i, (label, key) in enumerate(stats):
            ttk.Label(stats_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=(0, 10))
            self.stats_labels[key] = ttk.Label(stats_frame, text="0", font=('Arial', 10, 'bold'))
            self.stats_labels[key].grid(row=i, column=1, sticky=tk.W)
        
        # Frame de búsqueda avanzada
        advanced_frame = ttk.LabelFrame(main_frame, text="Buscador Avanzado", padding="10")
        advanced_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        advanced_frame.columnconfigure(0, weight=1)
        advanced_frame.rowconfigure(1, weight=1)
        
        # Controles de filtro
        filter_frame = ttk.Frame(advanced_frame)
        filter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filtrar por:").pack(side=tk.LEFT, padx=(0, 10))
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["todos", "seguido", "mutuo", "no_seguido", "te_sigue", "seguido_previamente"],
                                   state="readonly", width=15)
        filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        filter_combo.bind('<<ComboboxSelected>>', self.apply_filter)
        
        ttk.Button(filter_frame, text="Actualizar", command=self.refresh_table).pack(side=tk.LEFT)
        
        # Tabla de usuarios
        self.create_table(advanced_frame)
        
    def create_table(self, parent):
        """Crear la tabla de usuarios"""
        # Frame para la tabla
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Crear Treeview
        columns = ('username', 'estado', 'fecha_primer_seguimiento', 'fecha_ultima_interaccion')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        self.tree.heading('username', text='Usuario')
        self.tree.heading('estado', text='Estado')
        self.tree.heading('fecha_primer_seguimiento', text='Primer Seguimiento')
        self.tree.heading('fecha_ultima_interaccion', text='Última Interacción')
        
        self.tree.column('username', width=200)
        self.tree.column('estado', width=150)
        self.tree.column('fecha_primer_seguimiento', width=150)
        self.tree.column('fecha_ultima_interaccion', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Eventos
        self.tree.bind('<Double-1>', self.on_user_select)
        
        # Cargar datos iniciales
        self.refresh_table()
    
    def search_user(self, event=None):
        """Buscar un usuario específico"""
        username = self.search_var.get().strip()
        if not username:
            messagebox.showwarning("Advertencia", "Por favor ingresa un nombre de usuario")
            return
        
        # Normalizar username
        if not username.startswith('@'):
            username = '@' + username
        
        # Buscar en datos
        user_data = None
        for user in self.follows_data:
            if user['username'] == username:
                user_data = user
                break
        
        self.display_user_info(username, user_data)
    
    def display_user_info(self, username: str, user_data: Optional[Dict]):
        """Mostrar información de usuario"""
        # Limpiar frame de información
        for widget in self.user_info_frame.winfo_children():
            widget.destroy()
        
        # Limpiar frame de acciones
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        if user_data:
            # Información del usuario
            ttk.Label(self.user_info_frame, text=f"Usuario: {username}", 
                     font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
            
            # Mostrar detalles del estado
            estado_actual = user_data.get('estado_actual', 'N/A')
            estado_descripcion = self.get_estado_description(estado_actual)
            ttk.Label(self.user_info_frame, text=f"Estado: {estado_actual}", 
                     font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W)
            ttk.Label(self.user_info_frame, text=f"Descripción: {estado_descripcion}").grid(row=2, column=0, sticky=tk.W)
            
            # Mostrar fecha de última interacción
            ultima_interaccion = user_data.get('fecha_ultima_interaccion', 'N/A')
            if ultima_interaccion != 'N/A':
                ultima_interaccion = self.format_date(ultima_interaccion)
            ttk.Label(self.user_info_frame, text=f"Última interacción: {ultima_interaccion}").grid(row=3, column=0, sticky=tk.W)
            
            # Enlace al perfil
            link_label = ttk.Label(self.user_info_frame, text="Abrir perfil", 
                                 foreground="blue", cursor="hand2")
            link_label.grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
            link_label.bind('<Button-1>', lambda e: self.open_profile(username))
            
            # Botones de acción con lógica de habilitación/deshabilitación
            self.create_action_buttons(username, user_data)
        else:
            # Usuario no encontrado
            ttk.Label(self.user_info_frame, text=f"Usuario {username} no encontrado", 
                     font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
            ttk.Label(self.user_info_frame, text="Este usuario no está en tu base de datos.").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
            
            # Botón para agregar nuevo usuario (seguir)
            ttk.Button(self.actions_frame, text="Seguir", 
                      command=lambda: self.add_new_user(username)).pack(side=tk.LEFT)
    
    def get_estado_description(self, estado: str) -> str:
        """Obtener descripción del estado"""
        descriptions = {
            'seguido': 'Lo sigues pero él/ella no te sigue',
            'mutuo': 'Se siguen mutuamente',
            'no_seguido': 'No lo sigues',
            'te_sigue': 'Él/ella te sigue pero tú no lo sigues',
            'seguido_previamente': 'Lo seguiste en el pasado pero ya no lo sigues'
        }
        return descriptions.get(estado, 'Estado desconocido')
    
    def format_date(self, date_str: str) -> str:
        """Formatear fecha para mostrar"""
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            return date_str
    
    def create_action_buttons(self, username: str, user_data: Dict):
        """Crear botones de acción con lógica de habilitación"""
        estado_actual = user_data.get('estado_actual', 'no_seguido')
        
        # Botón Seguir - habilitado solo si no lo sigues actualmente
        seguir_enabled = estado_actual not in ['seguido', 'mutuo']
        btn_seguir = ttk.Button(self.actions_frame, text="Seguir", 
                               command=lambda: self.add_event(username, "seguido"),
                               state='normal' if seguir_enabled else 'disabled')
        btn_seguir.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Follow Back - habilitado solo si no te ha dado follow back
        follow_back_enabled = estado_actual not in ['mutuo', 'te_sigue']
        btn_follow_back = ttk.Button(self.actions_frame, text="Follow Back", 
                                    command=lambda: self.add_event(username, "follow_back"),
                                    state='normal' if follow_back_enabled else 'disabled')
        btn_follow_back.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Dejar de Seguir - habilitado si lo sigues actualmente O si está en estado te_sigue (follow_back)
        # En estado te_sigue, técnicamente no lo sigues pero puedes "dejar de seguir" para marcar que ya no quieres seguirlo
        dejar_seguir_enabled = estado_actual in ['seguido', 'mutuo', 'te_sigue']
        btn_dejar_seguir = ttk.Button(self.actions_frame, text="Dejar de Seguir", 
                                     command=lambda: self.add_event(username, "dejado_de_seguir"),
                                     state='normal' if dejar_seguir_enabled else 'disabled')
        btn_dejar_seguir.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Ver Historial - siempre habilitado
        ttk.Button(self.actions_frame, text="Ver Historial", 
                  command=lambda: self.show_history(username)).pack(side=tk.LEFT, padx=(0, 10))
    
    def add_event(self, username: str, event_type: str):
        """Agregar un evento para un usuario"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Buscar usuario existente
        user_index = None
        for i, user in enumerate(self.follows_data):
            if user['username'] == username:
                user_index = i
                break
        
        if user_index is not None:
            # Usuario existe, agregar evento
            if 'eventos' not in self.follows_data[user_index]:
                self.follows_data[user_index]['eventos'] = []
            
            self.follows_data[user_index]['eventos'].append({
                'tipo': event_type,
                'fecha': today
            })
            
            # Actualizar fechas
            if event_type == "seguido" and not self.follows_data[user_index].get('fecha_primer_seguimiento'):
                self.follows_data[user_index]['fecha_primer_seguimiento'] = today
            
            self.follows_data[user_index]['fecha_ultima_interaccion'] = today
            
            # Actualizar estado
            self.update_user_state(user_index)
        else:
            # Crear nuevo usuario
            new_user = {
                'username': username,
                'eventos': [{'tipo': event_type, 'fecha': today}],
                'fecha_primer_seguimiento': today if event_type == "seguido" else None,
                'fecha_ultima_interaccion': today
            }
            self.follows_data.append(new_user)
            self.update_user_state(len(self.follows_data) - 1)
        
        self.save_data()
        self.refresh_table()
        self.update_statistics()
        self.search_user()  # Actualizar vista
    
    def update_user_state(self, user_index: int):
        """Actualizar el estado de un usuario basado en sus eventos"""
        user = self.follows_data[user_index]
        eventos = user.get('eventos', [])
        
        if not eventos:
            user['estado_actual'] = 'no_seguido'
            return
        
        # Obtener último evento
        ultimo_evento = eventos[-1]['tipo']
        
        if ultimo_evento == "seguido":
            # Verificar si hay follow_back después del seguimiento
            seguido_index = None
            for i, evento in enumerate(eventos):
                if evento['tipo'] == "seguido":
                    seguido_index = i
            
            if seguido_index is not None:
                # Buscar follow_back después del seguimiento
                for evento in eventos[seguido_index:]:
                    if evento['tipo'] == "follow_back":
                        user['estado_actual'] = 'mutuo'
                        return
            
            user['estado_actual'] = 'seguido'
        elif ultimo_evento == "follow_back":
            user['estado_actual'] = 'te_sigue'
        elif ultimo_evento == "dejado_de_seguir":
            user['estado_actual'] = 'seguido_previamente'
    
    def add_new_user(self, username: str):
        """Agregar un nuevo usuario"""
        self.add_event(username, "seguido")
    
    def show_history(self, username: str):
        """Mostrar historial de un usuario"""
        for user in self.follows_data:
            if user['username'] == username:
                eventos = user.get('eventos', [])
                if eventos:
                    history_text = f"Historial de {username}:\n\n"
                    for evento in eventos:
                        history_text += f"• {evento['fecha']}: {evento['tipo']}\n"
                    
                    # Crear ventana de historial
                    history_window = tk.Toplevel(self.root)
                    history_window.title(f"Historial - {username}")
                    history_window.geometry("400x300")
                    
                    text_widget = tk.Text(history_window, wrap=tk.WORD, padx=10, pady=10)
                    text_widget.pack(fill=tk.BOTH, expand=True)
                    text_widget.insert(tk.END, history_text)
                    text_widget.config(state=tk.DISABLED)
                else:
                    messagebox.showinfo("Historial", f"No hay eventos registrados para {username}")
                break
    
    def open_profile(self, username: str):
        """Abrir perfil en el navegador"""
        # Remover @ si existe
        clean_username = username[1:] if username.startswith('@') else username
        url = f"https://instagram.com/{clean_username}"
        webbrowser.open(url)
    
    def refresh_table(self):
        """Actualizar la tabla de usuarios"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Aplicar filtro
        filtered_data = self.filter_data()
        
        # Insertar datos
        for user in filtered_data:
            self.tree.insert('', tk.END, values=(
                user['username'],
                user.get('estado_actual', 'N/A'),
                user.get('fecha_primer_seguimiento', 'N/A'),
                user.get('fecha_ultima_interaccion', 'N/A')
            ))
    
    def filter_data(self):
        """Filtrar datos según el filtro seleccionado"""
        filter_value = self.filter_var.get()
        
        if filter_value == "todos":
            return self.follows_data
        
        return [user for user in self.follows_data 
                if user.get('estado_actual') == filter_value]
    
    def apply_filter(self, event=None):
        """Aplicar filtro a la tabla"""
        self.refresh_table()
    
    def on_user_select(self, event):
        """Manejar selección de usuario en la tabla"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            username = item['values'][0]
            self.search_var.set(username)
            self.search_user()
    
    def update_statistics(self):
        """Actualizar estadísticas"""
        total_usuarios = len(self.follows_data)
        seguidos_actualmente = len([u for u in self.follows_data if u.get('estado_actual') == 'seguido'])
        te_siguen = len([u for u in self.follows_data if u.get('estado_actual') == 'te_sigue'])
        relaciones_mutuas = len([u for u in self.follows_data if u.get('estado_actual') == 'mutuo'])
        dejados_seguir = len([u for u in self.follows_data if u.get('estado_actual') == 'seguido_previamente'])
        
        # Calcular tasa de follow back
        total_seguidos = seguidos_actualmente + relaciones_mutuas
        tasa_follow_back = f"{(relaciones_mutuas / total_seguidos * 100):.1f}%" if total_seguidos > 0 else "0%"
        
        # Actualizar labels
        self.stats_labels['total_usuarios'].config(text=str(total_usuarios))
        self.stats_labels['seguidos_actualmente'].config(text=str(seguidos_actualmente))
        self.stats_labels['te_siguen'].config(text=str(te_siguen))
        self.stats_labels['relaciones_mutuas'].config(text=str(relaciones_mutuas))
        self.stats_labels['dejados_seguir'].config(text=str(dejados_seguir))
        self.stats_labels['tasa_follow_back'].config(text=tasa_follow_back)
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    app = FollowTracker()
    app.run()

if __name__ == "__main__":
    main() 