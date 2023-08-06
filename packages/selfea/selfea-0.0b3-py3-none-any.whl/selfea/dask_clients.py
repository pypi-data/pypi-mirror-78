from dask.distributed import Client, LocalCluster
# from dask_yarn import YarnCluster
# from evaluation_framework.utils.decorator_utils import yarn_directory_normalizer

import threading
import queue
import socket
import os
import time


def get_host_ip_address():
    """Get the host ip address of the machine where the executor is running. 

    Returns
    -------
    host_ip : String
    """
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return host_ip
    except:
        host_ip = '127.0.0.1'  # playing with fire...
        return host_ip

class ClientFuture():
    
    def __init__(self, local_client_n_workers, local_client_threads_per_worker):
        
        host_ip = get_host_ip_address()
        self.local_cluster = LocalCluster(n_workers=local_client_n_workers,
                               threads_per_worker=local_client_threads_per_worker, 
                               processes=True, 
                               host=host_ip)
        self.local_client = Client(address=self.local_cluster, timeout='2s') 
        
    def submit(self, func, *args, **kwargs):
        
        future = self.local_client.submit(func, *args, **kwargs)
        return future
        
    def get_dashboard_link(self):
        
        print('local cluster: ', self.local_cluster.dashboard_link)

