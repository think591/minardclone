
# 繪製地圖
#* projection="lcc": Lambert Conformal.
#* resolution="i": 解析度為中階（intermediate）
#* width=1000000: 地圖寬度為 100 萬公尺（1000 公里）
#* height=400000: 地圖高度為 40 萬公尺（400 公里）
#* lon_0=31, lat_0=55: 地圖的中心經緯度為 (31, 55)

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
            lon_0=31, lat_0=55)
lons = [24.0, 37.6]# 24.0, 55.0, Kowno; 37.6, 55.8, Moscou
lats = [55.0, 55.8]# 24.0, 55.0, Kowno; 37.6, 55.8, Moscou
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54, 58),labels=[True, False, False, False])
m.drawmeridians(range(23, 56, 2),labels=[False, False, False, True])
# plt.show()
xi, yi = m(lons, lats)  # 映射的轉換
m.scatter(xi, yi)
plt.show()



# 繪製城市圖

import sqlite3
import pandas as pd

connection = sqlite3.connect("data/minard.db")
city_df = pd.read_sql("""SELECT * FROM cities;""", con=connection)
connection.close()
print(city_df)

lons = city_df["lonc"].values
lats = city_df["latc"].values
city_names = city_df["city"].values
fig, ax = plt.subplots()
m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
            lon_0=31, lat_0=55, ax=ax)
m.drawcountries()
m.drawrivers()
x, y = m(lons, lats)
for xi, yi, city_name in zip(x, y, city_names):
    ax.annotate(text=city_name, xy=(xi, yi), fontsize=6)
plt.show()


# 繪製氣溫圖

connection = sqlite3.connect("data/minard.db")
temperature_df = pd.read_sql("""SELECT * FROM temperatures;""", con=connection)
connection.close()
print(temperature_df)

temp_celsius = (temperature_df["temp"] * 5/4).values  # 原始資料採用「列氏」溫度，轉換為攝氏溫度
lons = temperature_df["lont"].values
fig, ax = plt.subplots()
ax.plot(lons, temp_celsius)
plt.show()

# 繪製軍隊圖
connection = sqlite3.connect("data/minard.db")
troop_df = pd.read_sql("""SELECT * FROM troops;""", con=connection)
connection.close()
print(troop_df)

fig, ax = plt.subplots()
rows = troop_df.shape[0]
lons = troop_df["lonp"].values
lats = troop_df["latp"].values
survivals = troop_df["surviv"].values
directions = troop_df["direc"].values
for i in range(rows - 1):
    if directions[i] == "A":
        line_color = "tan"
    else:
        line_color = "black"
    start_stop_lons = (lons[i], lons[i + 1])
    start_stop_lats = (lats[i], lats[i + 1])
    line_width = survivals[i]
    ax.plot(start_stop_lons, start_stop_lats, linewidth=line_width/10000, color=line_color)
plt.show()


# 成品：將三個資料框準備好

import sqlite3
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

connection = sqlite3.connect("data/minard.db")
city_df = pd.read_sql("""SELECT * FROM cities;""", con=connection)
temperature_df = pd.read_sql("""SELECT * FROM temperatures;""", con=connection)
troop_df = pd.read_sql("""SELECT * FROM troops;""", con=connection)
connection.close()

# 透過 matplotlib 的子圖功能將四張圖合併在一個畫布上
#* nrows=2: 要有兩個垂直排列的軸物件。
#* figsize=(25, 12): 指定畫布的長與寬。
#* gridspec_kw={"height_ratios": [4, 1]}: 兩個垂直排列的軸物件高度比為 4:1

fig, axes = plt.subplots(nrows=2, figsize=(25,12))
fig, axes = plt.subplots(nrows=2, figsize=(25,12), gridspec_kw={"height_ratios": [4, 1]})
plt.show()

# 在第零個軸物件繪製地圖、城市圖與軍隊圖
loncs = city_df["lonc"].values
latcs = city_df["latc"].values
city_names = city_df["city"].values
rows = troop_df.shape[0]
lonps = troop_df["lonp"].values
latps = troop_df["latp"].values
survivals = troop_df["surviv"].values
directions = troop_df["direc"].values
fig, axes = plt.subplots(nrows=2, figsize=(25,12), gridspec_kw={"height_ratios": [4, 1]})
m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
            lon_0=31, lat_0=55, ax=axes[0])  # 第0個軸物件
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54, 58),labels=[True, False, False, False])
m.drawmeridians(range(23, 56, 2),labels=[False, False, False, True])
x, y = m(loncs, latcs)
for xi, yi, city_name in zip(x, y, city_names):
    axes[0].annotate(text=city_name, xy=(xi, yi), fontsize=14, zorder=2)      # 第0個軸物件

plt.show()  

x, y = m(lonps, latps)
for i in range(rows - 1):
    if directions[i] == "A":
        line_color = "tan"
    else:
        line_color = "black"
    start_stop_lons = (x[i], x[i+1])
    start_stop_lats = (y[i], y[i+1])
    line_width = survivals[i]
    m.plot(start_stop_lons, start_stop_lats, linewidth=line_width/10000, color=line_color, zorder=1)

plt.show()    

# 在第一個軸物件繪製氣溫圖
temp_celsius = (temperature_df["temp"] * 5/4).astype(int)
annotations = temp_celsius.astype(str).str.cat(temperature_df["date"], sep="°C ") #concatenation
lonts = temperature_df["lont"].values
axes[1].plot(lonts, temp_celsius, linestyle="dashed", color="black")
for lont, temp_c, annotation in zip(lonts, temp_celsius, annotations):
    axes[1].annotate(annotation, xy=(lont - 0.3, temp_c - 7), fontsize=16)
axes[1].set_ylim(-50, 10)
axes[1].spines["top"].set_visible(False)       #隱藏邊框
axes[1].spines["right"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].grid(True, which="major", axis="both") #顯示隔線
axes[1].set_xticklabels([])                    #隱藏 x軸刻度
axes[1].set_yticklabels([])                    #隱藏 y軸刻度

# 完成兩個軸物件的繪製
loncs = city_df["lonc"].values
latcs = city_df["latc"].values
city_names = city_df["city"].values
rows = troop_df.shape[0]
lonps = troop_df["lonp"].values
latps = troop_df["latp"].values
survivals = troop_df["surviv"].values
directions = troop_df["direc"].values
temp_celsius = (temperature_df["temp"] * 5/4).astype(int)
annotations = temp_celsius.astype(str).str.cat(temperature_df["date"], sep="°C ")
lonts = temperature_df["lont"].values
fig, axes = plt.subplots(nrows=2, figsize=(25,12), gridspec_kw={"height_ratios": [4, 1]})
m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
            lon_0=31, lat_0=55, ax=axes[0])
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54, 58),labels=[True, False, False, False])
m.drawmeridians(range(23, 56, 2),labels=[False, False, False, True])
x, y = m(loncs, latcs)
for xi, yi, city_name in zip(x, y, city_names):
    axes[0].annotate(text=city_name, xy=(xi, yi), fontsize=16, zorder=2)
x, y = m(lonps, latps)
for i in range(rows - 1):
    if directions[i] == "A":
        line_color = "tan"
    else:
        line_color = "black"
    start_stop_lons = (x[i], x[i + 1])
    start_stop_lats = (y[i], y[i + 1])
    line_width = survivals[i]
    m.plot(start_stop_lons, start_stop_lats, linewidth=line_width/10000, color=line_color, zorder=1)
axes[1].plot(lonts, temp_celsius, linestyle="dashed", color="black")
for lont, temp_c, annotation in zip(lonts, temp_celsius, annotations):
    axes[1].annotate(annotation, xy=(lont - 0.3, temp_c - 7), fontsize=16)
axes[1].set_ylim(-50, 10)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].grid(True, which="major", axis="both")
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])
axes[0].set_title("Napoleon's disastrous Russian campaign of 1812", loc="left", fontsize=30)

plt.tight_layout()
fig.savefig("minard_clone.png")

# plt.close() # 關閉圖片

