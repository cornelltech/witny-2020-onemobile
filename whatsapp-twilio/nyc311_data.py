import garbage
import school
import parking
import time

data_dict={
    
}

def get_data(data_name):
    currentTime=time.time()
    if data_name not in data_dict:
        data_dict[data_name] = {'time':None, 'data':None}
    lastTime=data_dict[data_name]['time']
    if lastTime == None or lastTime + 3600000 < currentTime:
        data = None
        if (data_name =='school'):
            data = school.get_school_data()
        elif (data_name=='garbage'):
            data = garbage.get_garbage_data()
        elif (data_name=='parking'):
            data = parking.get_parking_data()

        data_dict[data_name]['time']=currentTime
        data_dict[data_name]['data']=data
 
    return data_dict[data_name]['data']
