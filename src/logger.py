import datetime
class Logger:
        def __init__(self,filename):
            self.date=datetime.datetime.now().strftime("%d-%m-%y")
            self.filename='logs/{0}_{1}.log'.format(filename,self.date)
            with open(filename,'a') as file:
                file.write("logger initialized")
                file.write('\n')

        def info(self,msg):

            with open(self.filename,'a')  as file:
                statement='INFO:{0}:{1}'.format(datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),msg)
                file.write(statement)
                file.write('\n')
        def error(self,msg):

            with open(self.filename,'a')  as file:
                statement='ERROR:{0}:{1}'.format(datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),msg)
                file.write(statement)
                file.write('\n')
        
