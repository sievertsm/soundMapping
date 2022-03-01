import numpy as np

def sound_attenuation(db1, R1, R2):
    '''
    Function to predict decibles at a distance away from a source
    
    INPUT:
        db1 -- decibles measured at R1
        R1  -- distance from source of close measured point
        R2  -- distance from source of further point to be predicted
    
    OUTPUT:
        db2  -- decibles predicted at R2
        
    SOURCE:
        https://www.wkcgroup.com/tools-room/inverse-square-law-sound-calculator/
        https://www.engineeringtoolbox.com/inverse-square-law-d_890.html
    '''
    return db1 - 20 * np.log10(R2/R1)


def add_dB(dbs):
    '''
    Function to add arrays containing decible measurements
    
    INPUT:
        dbs -- list of arrays that have the same shape
        
    OUTPUT:
        lt  -- summation of the decible arrays (dbs)
        
    SOURCE:
        https://www.eetimes.com/using-the-decibel-part-3-combining-decibels-and-using-log-charts/#
    '''
    # expand dimension
    dbs = [np.expand_dims(d, 0) for d in dbs]
    # concatentate
    dbs = np.concatenate(dbs, axis=0)
    # add sound
    lt = dbs/10
    lt = 10**lt
    lt = 10*np.log10(lt.sum(axis=0))
    
    return lt


def get_boiler_machine(boil1=False, boil2=False, boil3=True, pump1=False, pump2=False, pump3=False, pump4=False, pump5=True, floor_dim=(75, 85)):
    
    b1 = {'on': boil1, 'dB': 79.8, 'coord': (15+16, floor_dim[0]-26)}
    b2 = {'on': boil2, 'dB': 81.1, 'coord': (floor_dim[1]-10-29, floor_dim[0]-26)}
    b3 = {'on': boil3, 'dB': 82.5, 'coord': (floor_dim[1]-10, floor_dim[0]-26)}
    p1 = {'on': pump1, 'dB': 79.3, 'coord': (floor_dim[1]-55, 10)}
    p2 = {'on': pump2, 'dB': 79.3, 'coord': (floor_dim[1]-42, 10)}
    p3 = {'on': pump3, 'dB': 79.3, 'coord': (floor_dim[1]-35, 10)}
    p4 = {'on': pump4, 'dB': 79.3, 'coord': (floor_dim[1]-28, 10)}
    p5 = {'on': pump5, 'dB': 79.3, 'coord': (floor_dim[1]-13, 10)}
    
    machines=[]
    machines_all = [b1, b2, b3, p1, p2, p3, p4, p5]
    for m in machines_all:
        if m['on']:
            machines.append(m)
            
    return machines


def get_chill1_machine(chill1=False, chill2=False, chill3=True, chill4=False, pump1=False, pump2=False, pump3=False, pump4=False, floor_dim=(75, 116)):
    
    c1 = {'on': chill1, 'dB': 87.2, 'coord': (floor_dim[1]-15-75, floor_dim[0]-40)}
    c2 = {'on': chill2, 'dB': 87.2, 'coord': (floor_dim[1]-15-55, floor_dim[0]-40)}
    c3 = {'on': chill3, 'dB': 87.2, 'coord': (floor_dim[1]-15-35, floor_dim[0]-40)}
    c4 = {'on': chill4, 'dB': 87.2, 'coord': (floor_dim[1]-15-14, floor_dim[0]-40)}
    p1 = {'on': pump1, 'dB': 84.3, 'coord': (10, floor_dim[0]-42)}
    p2 = {'on': pump2, 'dB': 84.3, 'coord': (10, floor_dim[0]-32)}
    p3 = {'on': pump3, 'dB': 84.3, 'coord': (10, floor_dim[0]-23)}
    p4 = {'on': pump4, 'dB': 84.3, 'coord': (10, floor_dim[0]-15)}
    
    machines=[]
    machines_all = [c1, c2, c3, c4, p1, p2, p3, p4]
    for m in machines_all:
        if m['on']:
            machines.append(m)
            
    return machines

def get_chill2_machine(chill1=False, chill2=False, floor_dim=(75, 45)):
    
    c1 = {'on': chill1, 'dB': 90.1, 'coord': (floor_dim[1]-31, floor_dim[0]-40)}
    c2 = {'on': chill2, 'dB': 87.8, 'coord': (floor_dim[1]-15, floor_dim[0]-40)}
    
    machines=[]
    machines_all = [c1, c2]
    for m in machines_all:
        if m['on']:
            machines.append(m)
            
    return machines


def get_noise_map(machines, floor_dim):
      
    xrange = np.arange(floor_dim[1])
    yrange = np.arange(floor_dim[0])
    
    distances=[]
    noise=[]
    for m in machines:

        dbs = m['dB']
        x, y = m['coord']

        xr = np.abs(xrange - x) + 1
        yr = np.abs(yrange - y) + 1

        X, Y = np.meshgrid(xr, yr)
        W, H = np.meshgrid(xrange, yrange)

        dist = np.sqrt(X**2 + Y**2)
        distances.append(np.expand_dims(dist, 0))

        n = sound_attenuation(dbs, 1, dist)
        noise.append(n)
        
    noise_sum = add_dB(noise)
    dist_min = np.concatenate(distances, axis=0).min(axis=0)
    
    return noise_sum, dist_min, (W, H)