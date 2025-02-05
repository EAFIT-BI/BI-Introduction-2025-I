# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 18:57:03 2025

@author: lmsepulvedac
"""

import pandas as pd
import sqlite3
import os


def archivo_a_sql(ruta_archivo, nombre_db):
    """
    Convierte un archivo de Excel (todas las hojas) o un archivo CSV en tablas de una base de datos SQLite.

    Parámetros:
        ruta_archivo (str): Ruta del archivo de Excel o CSV.
        nombre_db (str): Nombre del archivo de la base de datos SQLite.
    """
    try:
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()

        # Obtener la extensión del archivo
        extension = os.path.splitext(ruta_archivo)[1].lower()

        if extension in ['.xlsx', '.xls']:
            # Procesar archivo de Excel
            xls = pd.ExcelFile(ruta_archivo)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(ruta_archivo, sheet_name=sheet_name)
                table_name = sheet_name.strip().replace(' ', '_').replace('-', '_')
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"✅ Hoja '{sheet_name}' importada como tabla '{table_name}'.")
        
        elif extension == '.csv':
            # Procesar archivo CSV
            df = pd.read_csv(ruta_archivo)
            table_name = os.path.splitext(os.path.basename(ruta_archivo))[0].replace(' ', '_').replace('-', '_')
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"✅ Archivo CSV '{ruta_archivo}' importado como tabla '{table_name}'.")
        
        else:
            print("❌ Formato de archivo no soportado. Solo se permiten archivos Excel (.xlsx, .xls) o CSV (.csv).")
    
    except (sqlite3.Error, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"❌ Error durante la importación: {e}")
    
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
        print("🔒 Conexión cerrada.")
    
def ejecutar_consulta(consulta_sql, nombre_bd):
    """
    Ejecuta una consulta SQL en una base de datos SQLite.

    Parámetros:
        consulta_sql (str): La consulta SQL a ejecutar.
        nombre_bd (str): El nombre del archivo de la base de datos SQLite.

    Retorna:
        list: Una lista de tuplas con los resultados si es una consulta SELECT.
        None: Si es una consulta de modificación (INSERT, UPDATE, DELETE).
    """
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(nombre_bd)
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute(consulta_sql)
        
        # Verificar si es una consulta SELECT
        if consulta_sql.strip().lower().startswith('select'):
            resultados = cursor.fetchall()
            return resultados
        else:
            # Confirmar los cambios para INSERT, UPDATE, DELETE
            conn.commit()
            return None

    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        # Cerrar la conexión
        conn.close()
    
def mostrar_tablas(nombre_db):
    """
    Muestra todas las tablas de una base de datos SQLite.

    Parámetros:
        nombre_db (str): Nombre del archivo de la base de datos SQLite.
    
    Retorna:
        list: Lista con los nombres de las tablas en la base de datos.
    """
    try:
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()

        # Consultar las tablas existentes en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()

        if tablas:
            print("📊 Tablas en la base de datos:")
            for tabla in tablas:
                print(f" - {tabla[0]}")
        else:
            print("⚠️ No hay tablas en la base de datos.")
        
        return [tabla[0] for tabla in tablas]

    except sqlite3.Error as e:
        print(f"❌ Error al consultar las tablas: {e}")
        return []
    
    finally:
        # Cerrar la conexión
        conn.close()
        print("🔒 Conexión cerrada.")    
    
def mostrar_columnas(nombre_db, nombre_tabla):
    """
    Muestra los nombres de las columnas de una tabla en una base de datos SQLite.

    Parámetros:
        nombre_db (str): Nombre del archivo de la base de datos SQLite.
        nombre_tabla (str): Nombre de la tabla para la cual se desean ver las columnas.
    
    Retorna:
        list: Lista con los nombres de las columnas de la tabla.
    """
    try:
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()

        # Obtener la información de las columnas usando PRAGMA
        cursor.execute(f"PRAGMA table_info({nombre_tabla});")
        columnas_info = cursor.fetchall()

        if columnas_info:
            print(f"📋 Columnas de la tabla '{nombre_tabla}':")
            for columna in columnas_info:
                print(f" - {columna[1]}")  # columna[1] contiene el nombre de la columna
        else:
            print(f"⚠️ La tabla '{nombre_tabla}' no existe o no tiene columnas.")
        
        return [columna[1] for columna in columnas_info]

    except sqlite3.Error as e:
        print(f"❌ Error al consultar las columnas: {e}")
        return []
    
    finally:
        # Cerrar la conexión
        conn.close()
        print("🔒 Conexión cerrada.")
        
        