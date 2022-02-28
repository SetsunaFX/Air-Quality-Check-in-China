from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Pie, Tab,Map,Geo
from Spider import Spider
from ProvinceName import province
import time
class Drawing:
    
    def __init__(self):
        self.spider=Spider()
    
    #Draw Chinese
    def China_map(self):
        capitalList=self.spider.db.get_capital_city()
        provinceList=self.spider.db.get_province()
        num=len(capitalList)
        data=[]
        data1=[]
        start=time.time()
        for i in range(num):
            value=self.spider.getAQI(capitalList[i], 'PM2.5')
            data.append([capitalList[i]+'市',value])
            data1.append([provinceList[i],value])
        print(data1)
        end=time.time()
        print(end-start)
        c=(
           Map()
           .add("PM2.5", data1, 'china')
           .set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
                            title_opts=opts.TitleOpts(title="China's provincial capital PM2.5 concentration map")
                            )
        )
        plt=(
            Geo()
            .add_schema(maptype='china')
            .add("PM2.5",data)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(visualmap_opts=opts.VisualMapOpts(),
                             title_opts=opts.TitleOpts(title="China's provincial capital PM2.5 concentration map"))
            
            )
        tab = Tab()
        tab.add(c,'PM2.5-marked drawing')
        tab.add(plt, "PM2.5-unmarked drawing")
        tab.render("China's provincial capital PM2.5 concentration distribution.html")
     
    
    def draw_bar(self,cityList,data)-> Bar:
        c = (
        Bar()
        .add_xaxis(cityList)
        .add_yaxis("PM2.5", data)
        .set_global_opts(
            datazoom_opts=[opts.DataZoomOpts()],
            title_opts=opts.TitleOpts(title="PM2.5 histogram"),
        )
        )
        return c
    
    def draw_Line(self,cityList,data)-> Line:
        c=(
            Line()
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
            .add_xaxis(cityList)
            .add_yaxis(
                series_name="PM2.5",
                y_axis=data,
                symbol="emptyCircle",
                is_symbol_show=True,
            )
        )
        return c
    
    def draw_Map(self,data,ProvinceName):
        c=(
           Map()
           .add("PM2.5", data, ProvinceName)
           .set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
                            title_opts=opts.TitleOpts(title=province[ProvinceName]+' PM2.5 concentration map')
                            )
        )
        return c
    
    def Province_map(self,ProvinceName):
        city_list=self.spider.db.get_citylist(ProvinceName)
        num=len(city_list)
        data=[]
        value=[]
        for i in range(num):
            values=int(self.spider.getAQI(city_list[i], 'PM2.5'))
            value.append(values)
            data.append([city_list[i]+'市',values])
        tab = Tab()
        tab.add(self.draw_Map(data, ProvinceName),'PM2.5-map')
        tab.add(self.draw_bar(city_list,value), "PM2.5-bar")
        tab.add(self.draw_Line(city_list, value), "PM2.5-line")
        tab.render(province[ProvinceName]+' Province PM2.5 combination diagram.html')

if __name__=='__main__':
    draw=Drawing()
    draw.China_map()
    draw.Province_map('黑龙江')
    draw.Province_map('河北')