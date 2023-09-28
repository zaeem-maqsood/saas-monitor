from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from multiprocessing import Process, Value
from .models import CPUTest, MemoryTest
import os
import psutil
import time

# Create your views here.
class CPUMonitorView(TemplateView):
    template_name = "cpu_monitor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

def cpu_usage_view(request):
    exists = False
    if CPUTest.objects.exists():
        exists = True
    cpu_percent = psutil.cpu_percent(interval=0.5)
    data = {
        'cpu_percent': cpu_percent,
        'exists': exists
    }
    return JsonResponse(data)



class CpuStressView(View):

    start_time = None
    duration = 60  # seconds

    # The CPU stress function
    def fib(self, n):
        if n <= 1:
            return n
        return self.fib(n-1) + self.fib(n-2)

    def get(self, request, *args, **kwargs):
        action = request.GET.get('action')

        if action == 'start':
            # Check if there is a cpu test already
            if CPUTest.objects.exists():
                return JsonResponse({'error': 'A cpu test is already running'}, status=400)
            self.start_time = time.time()
            cpu_test = CPUTest.objects.create()
            self.start_load()
            cpu_test.delete()
            return JsonResponse({'status': 'load started'})
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    def start_load(self):
        while time.time() - self.start_time < self.duration:
            self.fib(30)


# Memory tests
class MemoryMonitorView(TemplateView):
    template_name = "memory_monitor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

def memory_usage_view(request):
    exists = False
    if MemoryTest.objects.exists():
        exists = True
    memory_info = psutil.virtual_memory()
    data = {
        'memory_percent_used': memory_info.percent,
        'exists': exists
    }
    return JsonResponse(data)

class MemoryStressView(View):

    start_time = None
    duration = 60  # seconds
    allocation_size = 500 * 10**6  # 500 MB, adjust as needed
    max_memory = 2 * 10**9  # 2GB
    # This will keep track of the total memory used across all processes
    memory_used = 0
    
    def total_memory_used(self):
        # Get the memory used by the current process
        current_process = psutil.Process(os.getpid())
        return current_process.memory_info().rss + self.memory_used
        
    def start_memory_load(self):
        print("Starting memory load")
        allocations = []
        try:
            while time.time() - self.start_time < self.duration:
                # Check the current memory usage before allocating
                if self.total_memory_used() + self.allocation_size > self.max_memory:
                    print(f"Approaching memory cap in process {os.getpid()}. Not allocating more.")
                    time.sleep(10)  # Sleep and check again later
                    continue
                
                memory_chunk = bytearray(self.allocation_size)
                allocations.append(memory_chunk)
                
                # Update the memory used value
                self.memory_used += self.allocation_size

                time.sleep(2)  # Adjust sleep time as needed
        except MemoryError:
            print(f"Memory error in process {os.getpid()}. Not allocating more.")
            while True:
                time.sleep(10)

    def get(self, request, *args, **kwargs):
        action = request.GET.get('action')

        if action == 'start':
            self.start_time = time.time()
            memory_test = MemoryTest.objects.create()
            self.start_memory_load()
            memory_test.delete()
            return JsonResponse({'status': 'load started'})
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)