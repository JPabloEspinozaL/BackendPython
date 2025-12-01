# ... (imports y configuraciones anteriores igual) ...

# 1. Consultar inventario CON FILTROS (Buscador)
@app.get("/vehiculos")
def listar_vehiculos(buscar: str = None):
    try:
        with engine.connect() as conn:
            # Consulta base
            sql = """
            SELECT 
                v.vin, v.modelo, v.ano, v.precio, v.stock, v.imagen_url, 
                v.marca_id, v.categoria_id,
                m.nombre as marca, 
                c.nombre as categoria
            FROM vehiculos v 
            JOIN marcas m ON v.marca_id = m.marca_id
            JOIN categorias c ON v.categoria_id = c.categoria_id
            """
            
            # Si hay búsqueda, agregamos el filtro WHERE
            params = {}
            if buscar:
                # Buscamos en modelo, marca o categoría (insensible a mayúsculas con ILIKE)
                sql += """ 
                WHERE 
                    v.modelo ILIKE :buscar OR 
                    m.nombre ILIKE :buscar OR 
                    c.nombre ILIKE :buscar
                """
                params["buscar"] = f"%{buscar}%"
            
            sql += " ORDER BY v.stock DESC"
            
            result = conn.execute(text(sql), params)
            return [dict(row._mapping) for row in result]
            
    except Exception as e:
        print(f"Error SQL: {e}")
        return []

# ... (resto del código igual) ...
