from folium.plugins import MarkerCluster
import folium


class FoliumMapGen:
    def __init__(self):
        self.map = folium.Map(location=[59.929951597507284, 30.321970787637802], control_scale=True)
        self.all = MarkerCluster(name="Базовый", control=False)
        self.map.add_child(self.all)

    def add_marker(self, name: str, type_trash: str, lan: float, len: float):  # self-name
        Market = folium.Marker([lan, len], popup=f"<i>{name}</i>", tooltip=type_trash)
        Market.add_to(self.all)

    def html(self, name: str):
        self.map.save(f"{name}.html")
