class FoliumMapGen:
    def __init__(self):
        self.map = folium.Map(location=[59.929951597507284, 30.321970787637802], control_scale=True)
        self.basic = MarkerCluster(name="Базовый", control=False)
        self.all = FeatureGroupSubGroup(self.basic, name="Все")
        self.organic = FeatureGroupSubGroup(self.basic, name="Органика")
        self.metal = FeatureGroupSubGroup(self.basic, name="Железо")
        self.plastic = FeatureGroupSubGroup(self.basic, name="Пластик")
        self.betary = FeatureGroupSubGroup(self.basic, name="Батарейки")
        self.paper = FeatureGroupSubGroup(self.basic, name="Бумага")
        self.glass = FeatureGroupSubGroup(self.basic, name="Стекло")

        self.map.add_child(self.basic)
        self.map.add_child(self.all)
        self.map.add_child(self.organic)
        self.map.add_child(self.metal)
        self.map.add_child(self.plastic)
        self.map.add_child(self.betary)
        self.map.add_child(self.paper)
        self.map.add_child(self.glass)
        LayerControl().add_to(self.map)

    def add_marker(self, name: str, type_trash: str, lan: float, len: float):  # self-name
        Market = folium.Marker([lan, len], popup=f"<i>{name}</i>", tooltip=type_trash)
        # Market.add_to(self.all)
        if type_trash == "Органика":
            Market.add_to(self.organic)
        elif type_trash == "Железо":
            Market.add_to(self.metal)
        elif type_trash == "Пластик":
            Market.add_to(self.plastic)
        elif type_trash == "Батарейки":
            Market.add_to(self.betary)
        elif type_trash == "Бумага":
            Market.add_to(self.paper)
        elif type_trash == "Стекло":
            Market.add_to(self.glass)
        elif type_trash == "Все":
            Market.add_to(self.all)

    def html(self, name: str):
        self.map.save(f"{name}.html")
