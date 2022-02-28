import requests
from bs4 import BeautifulSoup
from DataBase import DataBase
import pandas as pd
class Spider:
    def __init__(self):
        self.db=DataBase()
        pass
    
    def getHref(self):

        Province=[]
        City=[]

        url='http://www.tianqihoubao.com/aqi/'
        province_data=requests.get(url)
        province_data.encoding='gbk'
        province_data.status_code
        soup=BeautifulSoup(province_data.text,'html.parser')
        html=soup.find_all('div',{'class':'citychk'})
        for i in html:
            detail_data=i.find_all('dl')

            for  Municipalities in detail_data[0].find_all('a'):
                cityName=Municipalities.text.strip()

                if cityName=='广州':
                    break
                city_href=Municipalities.get('href')
                Province.append((cityName,cityName))
                href='http://www.tianqihoubao.com/'+city_href
                City.append((cityName,href))
            for j in detail_data[1:]:
                Province_name=j.dt.text
                city=[]
                for data in j.find_all('a'):
                    city.append(data.text.strip())
                    href='http://www.tianqihoubao.com/'+data.get('href')
                    City.append((data.text.strip(),href))
                Province.append((Province_name,str(city)))
        #The data is saved in the csv file.
        a=pd.DataFrame(Province,columns=['Province','affiliated_cities'])
        b=pd.DataFrame(City,columns=['city_name','href'])
        a.to_csv('Provinces and affiliated cities.csv')
        b.to_csv('City name and href.csv')
        #The data is saved in the database
        self.db.insertProvinces(Province)
        self.db.insert_City_href(City)
    
    #feature Air quality indicators include the following options: AQI,PM2.5,CO,SO2,PM10,O3,NO2
    def getAQI(self,cityName,feature):
        data={}
        url=self.db.get_city_href(cityName)
        url=url[0]
        data['cityName']=cityName
        r=requests.get(url)
        r.encoding='gbk'
        soup=BeautifulSoup(r.text,'html.parser')
        b=soup.find_all('div',{'class':'mod-tab-quality'})
        for i in b:
            aqi=i.find('div',{'class':'num'}).text.strip()
            data['AQI']=aqi
            status=i.find('div',{'class':'status'}).text.strip()
            data['status']=status
            J=i.find_all('li')
            PM2=J[0].text.strip().split('：')[-1]
            CO=J[1].text.strip().split('：')[-1]
            SO2=J[2].text.strip().split('：')[-1]
            PM10=J[3].text.strip().split('：')[-1]
            O3=J[4].text.strip().split('：')[-1]
            NO2=J[5].text.strip().split('：')[-1]
            data['PM2.5']=PM2
            data['CO']=CO
            data['SO2']=SO2
            data['PM10']=PM10
            data['O3']=O3
            data['NO2']=NO2
            
        return data[feature]

#If there is no data in the database, run the crawler first. If there is data in the database, draw directly
if __name__=='__main__':
    spider=Spider()
    spider.getHref()