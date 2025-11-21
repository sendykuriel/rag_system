"""
Utilidades para manejo de archivos.

Contiene funciones para leer, escribir y procesar archivos de texto.
"""

import json
import os
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional


def read_text_files(directory: str, file_extension: str = "*.txt") -> List[Dict[str, str]]:
    """
    Lee todos los archivos de texto de un directorio.
    
    Args:
        directory: Directorio que contiene los archivos
        file_extension: Extensión de archivos a leer (por defecto "*.txt")
        
    Returns:
        Lista de diccionarios con contenido y metadatos de cada archivo
    """
    txt_files = list(Path(directory).glob(file_extension))
    if not txt_files:
        print(f"⚠️  No se encontraron archivos {file_extension} en {directory}")
        return []
    
    files_data = []
    for file_path in txt_files:
        try:
            with open(file_path, 'rt', encoding='utf-8') as f:
                content = f.read()
                files_data.append({
                    "content": content,
                    "file_name": str(file_path.name),
                    "file_path": str(file_path)
                })
        except Exception as e:
            print(f"Error leyendo archivo {file_path}: {e}")
            continue
    
    return files_data


def save_pickle(data: Any, filepath: str) -> bool:
    """
    Guarda datos en formato pickle.
    
    Args:
        data: Datos a guardar
        filepath: Ruta del archivo
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"✅ Datos guardados en {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error guardando pickle {filepath}: {e}")
        return False


def load_pickle(filepath: str) -> Optional[Any]:
    """
    Carga datos desde un archivo pickle.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Datos cargados o None si hay error
    """
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        print(f"✅ Datos cargados desde {filepath}")
        return data
    except Exception as e:
        print(f"❌ Error cargando pickle {filepath}: {e}")
        return None


def save_json(data: Any, filepath: str, indent: int = 2) -> bool:
    """
    Guarda datos en formato JSON.
    
    Args:
        data: Datos a guardar
        filepath: Ruta del archivo
        indent: Indentación del JSON
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        print(f"✅ Datos guardados en {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error guardando JSON {filepath}: {e}")
        return False


def load_json(filepath: str) -> Optional[Any]:
    """
    Carga datos desde un archivo JSON.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Datos cargados o None si hay error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Datos cargados desde {filepath}")
        return data
    except Exception as e:
        print(f"❌ Error cargando JSON {filepath}: {e}")
        return None


def ensure_directory_exists(directory: str) -> bool:
    """
    Asegura que un directorio existe, lo crea si no existe.
    
    Args:
        directory: Ruta del directorio
        
    Returns:
        True si el directorio existe o se creó correctamente
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"❌ Error creando directorio {directory}: {e}")
        return False


def get_file_info(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene información de un archivo.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Diccionario con información del archivo o None si hay error
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return None
            
        stat = path.stat()
        return {
            "name": path.name,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "extension": path.suffix,
            "exists": True
        }
    except Exception as e:
        print(f"❌ Error obteniendo info de {filepath}: {e}")
        return None
