from rest_framework.views import APIView
from rest_framework.response import Response
from apps.authentication.permissions import EsMedico
from apps.analytics.calculators import KPICalculator
from apps.etl.models import EjecucionETL, Alerta

class DashboardKPIsView(APIView):
    permission_classes = [EsMedico]
    def get(self, request):
        kpis = KPICalculator().get_all_kpis()
        ultima_etl = EjecucionETL.objects.filter(estado='completado').first()
        return Response({
            'kpis': kpis,
            'ultima_etl': {
                'id': ultima_etl.id if ultima_etl else None,
                'fecha': ultima_etl.fecha_inicio if ultima_etl else None,
                'quality_score': (ultima_etl.reporte_calidad or {}).get('quality_score') if ultima_etl else None,
            } if ultima_etl else None,
        })

class DashboardTendenciaView(APIView):
    permission_classes = [EsMedico]
    def get(self, request):
        """Retorna datos de tendencia de los últimos 10 ETLs para gráfica de línea."""
        etls = EjecucionETL.objects.filter(estado='completado').order_by('-fecha_inicio')[:10]
        tendencia = []
        for e in reversed(list(etls)):
            qr = e.reporte_calidad or {}
            tendencia.append({
                'fecha': e.fecha_inicio.strftime('%d/%m'),
                'registros': e.registros_procesados,
                'quality_score': qr.get('quality_score', 0),
                'criticos': qr.get('criticos', 0),
            })
        return Response({'tendencia': tendencia})
