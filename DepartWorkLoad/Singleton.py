class Singleton(object):
    _instance = None
    '''
    def __new__(cls,*args,**kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls,*args,**kwargs)
        return cls._instance
    '''
    def __new__(cls,a):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    def __init__(self,workload):        
        self.exeworkload=workload.exeWorkLoad()
