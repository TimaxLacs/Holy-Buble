from tool import FoliumMapGen
from mitya.main import worksheet1
selfx = FoliumMapGen()
for i in worksheet1:
    cd = i["кординаты"].split(",")
    FoliumMapGen.add_marker(selfx, i["адрес"], i["название"], cd[0], cd[1])
FoliumMapGen.html(selfx, "gafas")
