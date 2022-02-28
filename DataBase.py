from pymysql import *
class DataBase:

    def __init__(self):

        self.db_name='air_qualitydb'
        #user of mysql
        user='root'
        #password of mysql
        password='123456'
        #self.db=connect('localhost',user,password,self.db_name)
        self.db = connect(host="localhost", user="root", password="123456", database="air_qualitydb")

    #The properties of the database table I provinces include province and cityList
    def insertProvinces(self,province):
        c=self.db.cursor()
        c.executemany('''INSERT into provinces values (%s,%s)''' ,province)
        self.db.commit()
    
    #Database table II city_href attribute has cityname href
    def insert_City_href(self,city_href):
        c=self.db.cursor()
        c.executemany('''INSERT into city_href values (%s,%s)''' ,city_href)
        self.db.commit()
    
    #Obtain the capital cities of 31 provinces or municipalities directly under the central government (no data from Hong Kong, Macao and Taiwan)
    def get_capital_city(self):
        c = self.db.cursor()
        c.execute('''select cityList from provinces ''')
        result = c.fetchall()
        l = []
        for i in range(len(result)):
            if i < 4:
                l.append(result[i][0])
            elif i<30:
                a=eval(result[i][0])[0]
                l.append(a)
            else:
                continue
        self.db.commit()
        return l
    
    def get_province(self):
        c=self.db.cursor()
        c.execute('''select Province from provinces''')
        result=c.fetchall()
        l=[]
        for i in result:
            l.append(i[0])
        self.db.commit()
        return l
    
    #Return to all affiliated cities in a province
    def get_citylist(self,provinceName):
        c=self.db.cursor()
        c.execute(''' select cityList from provinces where Province = %s ''',provinceName)
        result=c.fetchone()
        self.db.commit()
        return eval(result[0])
        
    #Get a hyperlink to a city
    def get_city_href(self,cityName):
        c=self.db.cursor()
        c.execute('''select href from city_href where cityName=%s ''',cityName)
        result=c.fetchone()
        self.db.commit()
        return result

    def delete(self):
        c=self.db.cursor()
        c.execute(''' truncate table city_href ''')
        self.db.commit()



    def close(self):
        self.db.close()
''''''
if __name__=='__main__':
    db=DataBase()
    a=db.get_capital_city()
    print(a)
