from django.urls import path

from .views import CPUMonitorView, cpu_usage_view, CpuStressView, MemoryMonitorView, memory_usage_view, MemoryStressView

urlpatterns = [
    path('cpu-monitor/', CPUMonitorView.as_view(), name='cpu_monitor'),
    path('cpu-usage/', cpu_usage_view, name='cpu_usage'),
    path('cpu-stress/', CpuStressView.as_view(), name='cpu_stress'),

    path('memory-monitor/', MemoryMonitorView.as_view(), name='memory_monitor'),
    path('memory-usage/', memory_usage_view, name='memory_usage'),
    path('memory-stress/', MemoryStressView.as_view(), name='memory_stress'),
]