
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

cursor = None
conexion =psycopg2.connect(user='postgres',
                           password='1234',
                           host='127.0.0.1',
                           port='5432',
                           database='dataEngineer')


'''
este metodo sirve  para cargar los datos proporcionados en una tabla llamada <set>
se utilozo PostgreSQL 14 por su rendimiento, seguridad y estabilidad.
'''
def add_table_set():

    try:
        cursor = conexion.cursor()
        df = pd.read_csv('C:/Users/USUARIO/Downloads/data.csv')
        df_filtrado = df.dropna(subset=['id'])
        df_filtrado.to_csv('data.csv', index=False)
        with open('data.csv', 'r') as f:
            cursor.copy_from(f, 'set', sep=',', null='')
        conexion.commit()
    except Exception as e:
        print(f"error: {e}")
    finally:
        cursor.close()
        conexion.close()


'''
Python junto con la librería Pandas para manejar archivos CSV y filtrar datos,
pandas es muy rápido para manejar archivos CSV grandes.
Usa estructuras optimizadas (como DataFrames con NumPy internamente).
fueron varios retos que se tuvieron que superar, ordenamiento de columnas, 
'''
def ddbb_to_csv():

    try:
        engine = create_engine(f'postgresql+psycopg2://{'postgres'}:{'1234'}@{'127.0.0.1'}:{'5432'}/{'dataEngineer'}')
        sql_query = "SELECT * FROM set;"
        df = pd.read_sql(sql_query, engine)
        df.drop(df.index[0], inplace=True)
        nombres = ['id','company_name','company_id','amount','status','created_at','updated_at']
        df.columns = nombres
        nuevo_orden = ['id','amount','company_id','company_name','status','created_at','updated_at']
        df_reordenado = df[nuevo_orden]
        csv_file_path = 'output_data.csv'
        df_reordenado.to_csv(csv_file_path, index=False) 
    except Exception as e:
        print(f"error: {e}")
    finally:
        conexion.close()

'''
en la parte de la dispersion de la informacion tuvimos varios retos que cumplir.
campo de company_id tenia datos incorrectos, duplicados
para el vaciado de la informacion a la bbdd se tuvo que ordenas las columnas y omitir algunas
dependiendo la tabla

'''
def dispersion_informacion():
    try:
        cursor = conexion.cursor()
        df = pd.read_csv('output_data.csv')

        df_subset_col1 = df.drop_duplicates(subset=['company_id']).dropna(subset=['company_id'])
        filas_a_eliminar = df_subset_col1[df_subset_col1['company_id'].str.contains('\\*', na=False)].index
        mi_df_filtrado = df_subset_col1.drop(filas_a_eliminar)
        mi_df_filtrado = mi_df_filtrado.drop(columns=['id','created_at','updated_at','amount','status'])
        mi_df_filtrado = mi_df_filtrado.explode('company_name').reset_index(drop=True)
        #columnas_a_guardar = ['company_id','company_name']
        #df_seleccionado = mi_df_filtrado[columnas_a_guardar]
        engine = create_engine(f'postgresql+psycopg2://{'postgres'}:{'1234'}@{'127.0.0.1'}:{'5432'}/{'dataEngineer'}')
        #mi_df_filtrado.to_sql('companies', engine, if_exists='append', index=False)
        print('--charges---')
        df2 = df.dropna(subset=['company_id'])#vacios
        filas_a_eliminar2 = df2[df2['company_id'].str.contains('\\*', na=False)].index#***
        mi_df_filtrado2 = df2.drop(filas_a_eliminar2)
        #mi_df_filtrado2 = mi_df_filtrado2.drop('company_name', axis=1, inplace=True)
        
        dftemp = pd.DataFrame()
        dftemp[['id','amount','company_id','status','created_at','updated_at']] = mi_df_filtrado2[['id','amount','company_id','status','created_at','updated_at']].copy()

        #dftemp = dftemp['amount'].map('{:.2f}'.format)
        #print('-->',dftemp)
        dftemp.to_sql('charges', engine, if_exists='append', index=False)
        
    except Exception as e:
        print(f"error: {e}")
    finally:
        cursor.close()
        conexion.close()


add_table_set()
ddbb_to_csv()
dispersion_informacion()





