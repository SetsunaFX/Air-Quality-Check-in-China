The database uses MySQL databas

Set the username and password in database.py to facilitate Python to connect to the database

Create two tables in the database
The properties of the database table I provinces include province and cityList
The properties of the database table II city_href include cityname and href
Properties are all set to varchar (200) type

If the database starts to be empty, run spider.py first, check whether the database has inserted data
If you have data, you don't have to run the crawler anymore

Drawing program has two functions
function I, China_map(self)：
Draw China's provincial capital PM2.5 concentration distribution
There are two pictures, one showing the name of the provincial capital and the other not

Function II,Province_map(self,ProvinceName):
ProvinceName is the name of the province you entered such as '江苏' and '浙江'

There are three pictures
One is a map, one is a histogram, and one is a line chart
