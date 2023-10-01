import psutil
import threading
import time
import subprocess
import matplotlib.pyplot as plt


class ResourceMonitor:
    def __init__(self, interval=0.1, GPU=False, save_path=None):
        self.interval = interval
        self.GPU = GPU
        self.cpu_usage_data = []
        self.memory_usage_data = []
        if self.GPU:
            self.gpu_usage_data = []
            self.gpu_memory_data = []
        self.time_data = []
        self.monitor_thread = None
        self.is_monitoring = False
        self.save_path = save_path

    def start(self):
        self.monitor_thread = threading.Thread(target=self.monitor_usage)
        self.monitor_thread.start()

    def monitor_usage(self):
        time_begin = time.time()
        self.is_monitoring = True
        while self.is_monitoring:
            try:
                # Get CPU and memory usage for the current process.
                process = psutil.Process()
                cpu_percent = process.cpu_percent(interval=self.interval)
                memory_info = process.memory_info()

                # Record CPU and memory usage
                timestamp = time.time() - time_begin
                self.cpu_usage_data.append(cpu_percent)
                self.memory_usage_data.append(memory_info.rss / (1024 * 1024))  # Convert to MB
                self.time_data.append(timestamp)

                if self.GPU:
                    # Use subprocess to call 'nvidia-smi' to get GPU information
                    gpu_info = subprocess.check_output(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used', '--format=csv,noheader,nounits']).decode('utf-8').strip().split(',')
                    gpu_usage = float(gpu_info[0])
                    gpu_memory = float(gpu_info[1])

                    # Record GPU usage and GPU memory usage
                    self.gpu_usage_data.append(gpu_usage)
                    self.gpu_memory_data.append(gpu_memory)

                time.sleep(self.interval)
            except KeyboardInterrupt:
                print("Monitoring stopped.")
                break

    def stop(self):
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()

    def plot_usage(self):
        ncols = 2 if self.GPU else 1
        plt.figure(figsize=(12, 8))

        # Plot CPU usage
        plt.subplot(2, ncols, 1)
        plt.plot(self.time_data, self.cpu_usage_data, label='CPU Usage', color='blue')
        plt.xlabel('Time (s)')
        plt.ylabel('CPU Usage (%)')
        plt.title('CPU Usage Over Time')
        plt.grid(True)

        # Plot memory usage
        plt.subplot(2, ncols, 2)
        plt.plot(self.time_data, self.memory_usage_data, label='Memory Usage', color='green')
        plt.xlabel('Time (s)')
        plt.ylabel('Memory Usage (MB)')
        plt.title('Memory Usage Over Time')
        plt.grid(True)

        if self.GPU:
            # Plot GPU usage
            plt.subplot(2, ncols, 3)
            plt.plot(self.time_data, self.gpu_usage_data, label='GPU Usage', color='red')
            plt.xlabel('Time (s)')
            plt.ylabel('GPU Usage (%)')
            plt.title('GPU Usage Over Time')
            plt.grid(True)

            # Plot GPU memory usage
            plt.subplot(2, ncols, 4)
            plt.plot(self.time_data, self.gpu_memory_data, label='GPU Memory Usage', color='purple')
            plt.xlabel('Time (s)')
            plt.ylabel('GPU Memory Usage (MB)')
            plt.title('GPU Memory Usage Over Time')
            plt.grid(True)

        plt.tight_layout()

        if self.save_path is not None:
            plt.savefig(self.save_path)
        else:
            plt.show()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        self.plot_usage()
