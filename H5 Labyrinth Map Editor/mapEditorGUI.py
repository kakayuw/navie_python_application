from tkinter import *
import hashlib
import time
import random
import re

# The path of the html5 Labyrinth Game
html_path = './MazeGame.html'


class LabyMap():
    def __init__(self, map = []):
        self.mapdata = map
        self.width = 0
        self.height = 0
        self.cell = 1

    def set_cell(self, size=1):
        self.cell = size

    def refresh(self):
        self.width = self.get_height()
        self.height = self.get_height()

    def get_width(self):
        maxW = 0
        for i in self.mapdata:
            if len(i) > maxW:
                maxW = len(i)
        return maxW

    def get_height(self):
        return len(self.mapdata)

    def set_map_data(self, map_data):
        self.mapdata = map_data
        self.refresh()

    def get_color(self, x, y):
        value = 0
        try:
            value = self.mapdata[x][y]
        except IndexError:
            value = 0

        if value == 0:
            return '#333'
        elif value == 1:
            return '#888'
        elif value == 2:
            return '#555'
        elif value == 3:
            return 'Green'
        elif value == 4:
            return '#777'
        elif value == 5:
            return '#E373FA'
        elif value == 6:
            return '#666'
        elif value == 7:
            return '#73C6FA'
        elif value == 8:
            return '#FADF73'
        elif value == 9:
            return '#C93232'
        elif value == 10:
            return '#555'
        elif value == 11:
            return '#0FF'
        return 'Maroon'

    def cell_up(self):
        self.cell += 1

    def cell_down(self):
        self.cell -= 1


class myGUI():
    def __init__(self, init_window):
        self.init_window = init_window
        self.map = LabyMap()
        self.map_data_str = ""  # store as str format | decouple view & model

    def set_init_window(self):
        self.init_window.title("Map Data Editor")
        self.init_window["bg"] = "GhostWhite"  # other canvas color ：blog.csdn.net/chl0000/article/details/7657887
        self.init_window.attributes("-alpha", 0.95)  
        # Label
        self.init_data_label = Label(self.init_window, text="DIGIT FORMAT", bg="lightblue")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window, text="PIXEL FORMAT", bg="lightblue")
        self.result_data_label.grid(row=0, column=12)

        # Text input form
        self.init_data_Text = Text(self.init_window, width=67, height=39)
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)

        # Canvas
        self.canvas = Canvas(self.init_window, width=500, height=500)
        self.canvas.grid(row=1, column=10, rowspan=10, columnspan=10)

        # Canvas Scalable Button
        self.cell_up_button = Button(self.init_window, text="+", command=self.map.cell_up, width=2, bg="LightSlateGray")
        self.cell_down_button = Button(self.init_window, text="-", command=self.map.cell_down, width=2, bg="LightSlateGray")
        self.cell_up_button.grid(row=1, column=20)
        self.cell_down_button.grid(row=2, column=20)
        self.map.set_cell(6)

        # Export Button
        self.export_button = Button(self.init_window, text="EXPORT", command=self.save_map_str, width=10, bg="LightGreen")
        self.export_button.grid(row=15, column=14)
        self.exportHTML_button = Button(self.init_window, text="EXPORT HTML", command=self.export_html, width=12, bg="LightGreen")
        self.exportHTML_button.grid(row=15, column=16)

        # Refresh Button
        self.refresh_button = Button(self.init_window, text="REFRESH", command=self.refresh_data, width=10, bg="LightGreen")
        self.refresh_button.grid(row=15, column=12)
        self.refresh_tip = Label(self.init_window, text="Refresh every 10s or click the 'REFRESH' button")
        self.refresh_tip.grid(row=15, column=0)


    # Draw laby map on canvas with <mapdata>
    def drawMap(self):
        print(self.map.get_width())
        for i in range(self.map.get_height()):
            for j in range(self.map.get_width()):
                x1 = i * self.map.cell
                y1 = j * self.map.cell
                x2 = x1 + self.map.cell
                y2 = y1 + self.map.cell
                color = self.map.get_color(i, j)
                self.canvas.create_rectangle(y1, x1, y2, x2, fill=color)        # x and y are reversed in Tk canvas
        return

    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    # Refresh canvas every 1000 ms
    def refresh_data(self):
        self.canvas.delete("all")
        self.synchro_map(self.init_data_Text.get(1.0, END))
        self.map.set_map_data( self.get_map_data(self.map_data_str) )
        self.drawMap()
        self.init_window.after(100000, self.refresh_data)

    # Get 2 dm map from file in string format
    def get_string_from_file(self):
        f = open(html_path, 'r', encoding="utf-8")
        f_read = f.read()
        # print(f_read)
        p1 = re.compile(r'data: [[](.*?)\/\*', re.S)  # minimum map
        mapStr = re.findall(p1, f_read)[0]
        mapStr = mapStr.replace(' ', '').replace('\n', '')
        mapStr = mapStr[:-2]        # remove outer []
        mapStr = mapStr.replace('],', '],\n')
        return mapStr

    def load_text(self):
        # self.init_data_Text.delete(0, END)    # clean all text
        self.map_data_str = self.get_string_from_file()
        self.init_data_Text.insert(END, self.mapstr_to_text())


    # Get map data in list format
    def get_map_data(self, mapstr):
        mapstr = str(mapstr)
        mapData = []
        for rawStr in mapstr.split('\n'):
            rawStr = rawStr.replace('[', '').replace(']', '')
            # rowData = [int(i) for i in rawStr.split(',') if i.isdigit()]  # get bit data if in list string format
            rowData = [int(i) for i in rawStr.split(',') if i != '']
            mapData.append(rowData)
        return mapData

    # Convert stored str to EDITABLE TEXT, return text
    def mapstr_to_text(self):
        text = self.map_data_str
        text = text.replace('[', '').replace(']', '')
        text = text.replace('10', 'a').replace('11', 'b').replace('12', 'c').replace('13', 'd').replace('14', 'e')\
            .replace('15', 'f').replace('16', 'g').replace('17', 'h').replace('18', 'i').replace('19', 'j').replace('20', 'k')
        text = text.replace(',', '')
        return text

    # Decode editable text and update stored map data
    def synchro_map(self, text):
        text = str(text)
        rowList = []
        for row in text.split('\n'):
            new = row.replace('\n', '')
            new = ','.join([i for i in new])
            new = '[' + new + '],'
            rowList.append(new)
        map_str = '\n'.join(rowList)
        map_str = map_str.replace('a', '10').replace('b', '11').replace('c', '12').replace('d', '13').replace('e', '14') \
            .replace('f', '15').replace('g', '16').replace('h', '17').replace('i', '18').replace('j', '19').replace(
            'k', '20')
        map_str = map_str[:-1]      # erase the last comma
        self.map_data_str = map_str

    # Save map data string to local file
    def save_map_str(self, localpath = './', filename="mapstr.txt"):
        fo = open(localpath + filename, "w")
        fo.write(self.map_data_str)
        fo.close()

    # Save HTML file
    def export_html(self, localpath = './', filename="newfile.html"):
        html_str = open(html_path, 'r', encoding="utf-8").read()
        mapdata_str = self.get_string_from_file()
        purify = lambda x: x.replace(' ', '').replace("\n", '/**/\n').replace('//', '/*')\
                            .replace('\n', '')    # erase all \n and \\
        # newfilestr = purify(html_str).replace(purify(mapdata_str), purify(self.map_data_str))
        # newfilestr = html_str.replace(mapdata_str, self.map_data_str)

        patch_data = 'data:[' + self.map_data_str + '],/*'
        print(patch_data)
        re_match = re.compile(r'data: [[](.*?)\/\*', re.S)
        newfilestr = re_match.sub(patch_data, html_str)

        fo = open(localpath + filename, "w", encoding='utf-8')
        fo.write(newfilestr)
        fo.close()


def gui_start():
    init_window = Tk()
    portal = myGUI(init_window)
    portal.set_init_window()
    portal.load_text()
    portal.refresh_data()
    init_window.mainloop()


gui_start()