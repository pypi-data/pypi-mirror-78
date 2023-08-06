def esperar_fin_consulta_SQL_athena(query_execution_id):
    
    import boto3
    import time
    
    client = boto3.client('athena')
    execution = None
    status = None
    while True:
        execution = client.get_query_execution(QueryExecutionId=query_execution_id)
        status = execution['QueryExecution']['Status']['State']
        if not status in ['RUNNING', 'QUEUED']:
            break
        time.sleep(0.5) # 500ms
    
   #print(query_execution_id + " " + status)
    if status != 'SUCCEEDED':
        st = execution['QueryExecution']['Status']
        raise Exception('{} : {}'.format(st['State'], st['StateChangeReason']))


def ejecutar_consulta_SQL_athena(query, BUCKET_NAME, TRASH_FOLDER, trae_datos= True):
    
    import pandas as pd
    import boto3
    
    client = boto3.client('athena')
    
    queryStart = client.start_query_execution(
        QueryString = query,
        QueryExecutionContext = {
            'Database': 'sandbox'
        },
            ResultConfiguration={
                'OutputLocation': f's3://{BUCKET_NAME}/{TRASH_FOLDER}/'
            }
    )
    execution_id = queryStart['QueryExecutionId']
    esperar_fin_consulta_SQL_athena(execution_id)

    if trae_datos == True:
        archivo = execution_id + '.csv'
        ruta = f's3://{BUCKET_NAME}/{TRASH_FOLDER}/{archivo}'
        data = pd.read_csv(ruta)
    else:
        data = None
    return data    


def obtener_ultima_fecha_corte_tabla(pais, nombre_tabla, primera_ejecucion, ENV_DATABASE):
    
    import awswrangler as wr
    import pandas as pd
    
    if primera_ejecucion==False: #Si ya se corrió previamente, cual fue la última corrida?
        query = f"""
        SELECT 
            CAST(CAST(ult_fecha_corte AS DATE) AS VARCHAR) AS ult_fecha_corte 
        FROM
            (
            SELECT
                MAX(fecha_corte) AS ult_fecha_corte
            FROM {ENV_DATABASE}.{nombre_tabla} 
            WHERE partition_0='{pais}'
        )
        WHERE DATE(ult_fecha_corte) <= CURRENT_DATE
        """
        df = wr.athena.read_sql_query(sql=query, database=ENV_DATABASE)
        
        if df.shape[0]!=0:
            ult_fecha_corte = df.ult_fecha_corte[0]
        else:
            ult_fecha_corte = '2018-01-01' #si nunca se cargó la tabla cargarla entera
    else:
        ult_fecha_corte = '2018-01-01'

    return(ult_fecha_corte)



def obtener_fechas_corte_a_calcular(pais, ult_fecha_corte, dia_corte_pais):
    from datetime import date
    from itertools import compress
    import pandas as pd

    fecha_actual = pd.to_datetime(date.today())
    
    fechas_corte=[(d+pd.DateOffset(days=dia_corte_pais)) for d in  pd.date_range(start=ult_fecha_corte,end=fecha_actual, freq='1M')]
    filtro_antes_fecha_actual = [f < fecha_actual for f in fechas_corte]
    fechas_corte = list(compress(fechas_corte, filtro_antes_fecha_actual))

    fechas_corte_text=[d.strftime('%Y-%m-%d') for d in  fechas_corte]

    return(fechas_corte_text)


def generar_tabla_historica_cobros(dict_paises, nombre_tabla, ENV_DATABASE, BUCKET_NAME):    
    
    import cobrospsg
    import awswrangler as wr
    import boto3
    
    for key in dict_paises:

        pais = dict_paises[key]['pais']
        primera_ejecucion=dict_paises[key]['primera_ejecucion']
        dia_corte_pais = dict_paises[key]['dia_corte_pais']
        
        if pais==None or pais=='':
            print('Pais no definido:'+ str(pais))
            continue
        
        if primera_ejecucion == True:
            #Borro los datos
            print("Borrar datos de "+str(pais))

            a_borrar = f"""{ENV_DATABASE}/{nombre_tabla}/partition_0={pais}/"""
            print(a_borrar)
            
            s3 = boto3.resource('s3')
            bucket_o = s3.Bucket(BUCKET_NAME)
            bucket_o.objects.filter(Prefix=a_borrar).delete()
            #Drop ?      
            
        print(pais)

        ult_fecha_corte = cobrospsg.obtener_ultima_fecha_corte_tabla(pais=pais, nombre_tabla=nombre_tabla, primera_ejecucion=primera_ejecucion, ENV_DATABASE=ENV_DATABASE)
        fechas_corte_text = cobrospsg.obtener_fechas_corte_a_calcular(pais=pais, ult_fecha_corte=ult_fecha_corte, dia_corte_pais=dia_corte_pais)

        if len(fechas_corte_text)==0:
                print("No hay periodos nuevos.")
        else:

            for fecha_corte in fechas_corte_text:
                print("Fecha de corte: " + fecha_corte)
                query=generar_query(fecha_corte, pais)
                df = wr.athena.read_sql_query(sql=query, database=ENV_DATABASE)
                
                if(df.shape[0] != 0):
                    
                    print(df.shape)

                    wr.s3.to_parquet(
                        df,
                        path=f"""s3://{BUCKET_NAME}/{ENV_DATABASE}/{nombre_tabla}/""",
                        database=ENV_DATABASE,
                        dataset=True,
                        table=nombre_tabla,
                        partition_cols=['partition_0', 'fecha_corte'],
                        mode='append',
                        compression='snappy'
                    )
                else:
                    print("No hay datos para esta fecha de corte.")

        print("Fin pais.")
    print("Fin proceso.")