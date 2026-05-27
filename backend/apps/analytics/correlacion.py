"""
Módulo de correlación clínica para el heatmap del dashboard.
Calcula la matriz de correlación de Pearson entre variables numéricas clave.
"""
from typing import Dict, List
import pandas as pd


VARIABLES_CLINICAS: List[str] = [
    'imc', 'glucosa', 'colesterol', 'presion_sistolica',
    'presion_diastolica', 'frecuencia_cardiaca', 'saturacion_oxigeno', 'temperatura',
]

LABELS: Dict[str, str] = {
    'imc':                'IMC',
    'glucosa':            'Glucosa',
    'colesterol':         'Colesterol',
    'presion_sistolica':  'Presión Sist.',
    'presion_diastolica': 'Presión Diast.',
    'frecuencia_cardiaca':'Frec. Cardíaca',
    'saturacion_oxigeno': 'Saturación O₂',
    'temperatura':        'Temperatura',
}


class CorrelacionCalculator:
    """
    Calcula la matriz de correlación de Pearson entre las variables clínicas
    numéricas de los registros almacenados en base de datos.

    Returns:
        Diccionario con labels y matriz lista para Chart.js matrix plugin.
    """

    def calcular(self) -> dict:
        from apps.etl.models import RegistroClinico

        qs: QuerySet = RegistroClinico.objects.values(*VARIABLES_CLINICAS)
        if not qs.exists():
            return {'error': 'Sin datos suficientes para calcular correlación'}

        df: pd.DataFrame = pd.DataFrame(list(qs)).dropna()
        if len(df) < 10:
            return {'error': 'Se necesitan al menos 10 registros'}

        corr: pd.DataFrame = df[VARIABLES_CLINICAS].corr(method='pearson')

        # Formato plano para Chart.js matrix plugin
        data_points = []
        for i, var_x in enumerate(VARIABLES_CLINICAS):
            for j, var_y in enumerate(VARIABLES_CLINICAS):
                val = round(float(corr.loc[var_x, var_y]), 3)
                data_points.append({'x': i, 'y': j, 'v': val})

        return {
            'labels':      [LABELS[v] for v in VARIABLES_CLINICAS],
            'variables':   VARIABLES_CLINICAS,
            'data_points': data_points,
            'n_registros': len(df),
        }
