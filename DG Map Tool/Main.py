import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class SharedData:
    def __init__(self, image):
        self.backgroundImage = image

class DrawShapeApp:
    def __init__(self, parent, SBM):
        if SBM == None:
            return
        self.root = tk.Toplevel(parent)
        self.canvas = tk.Canvas(self.root, bg='white', width=500, height=500)
        self.canvas.grid(row = 0, column = 0, padx=10, pady=10)

        # Load and display an image
        self.image = Image.open(SBM)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(250, 250, image=self.tk_image)  # Center image

        # Shape options and current shape variable
        self.shapes = {"Select": None, 'Move': None, 'Rectangle': self.create_rectangle, 'Oval': self.create_oval, 'Line': self.create_line}
        self.current_shape = None

        # Add buttons for shape selection
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=1, column=0, padx=5, pady=5)
        CUR_COL = 0
        for shape in self.shapes:
            btn = tk.Button(self.buttons_frame, text=shape, command=lambda s=shape: self.select_shape(s))
            btn.grid(row=0, column= CUR_COL)
            CUR_COL += 1

        self.token_frame = tk.Frame(self.root)
        self.token_frame.grid(row=2, column=0)
        CUR_COL = 0
        self.token_path = CURRENT_DIRECTORY + "\\Tokens"
        
        #load buttons for all the tokens
        for token in os.listdir(self.token_path):
            image = Image.open(self.token_path + "\\" + token)
            image = image.resize((50,50))
            photo = ImageTk.PhotoImage(image)
            tokenButton = tk.Button(self.token_frame, image = photo, command = print())
            tokenButton.photo = photo
            tokenButton.grid(row=0, column=CUR_COL)
            CUR_COL += 1

        # Bind mouse events to methods
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<ButtonPress-3>", self.delete_shape)

        self.start_x = None
        self.start_y = None
        self.current_item = None
        self.current_action = None  # This is for moving shapes

    #chenge which shape is being created
    def select_shape(self, shape):
        self.current_shape = self.shapes[shape]
        if shape == "Select":
            self.current_action = 'select'
        elif shape == "Move":
            self.current_action = "move"
        else:
            self.current_action = "create"

    def on_press(self, event):
        if self.current_action == 'create':
            self.start_x = event.x
            self.start_y = event.y
            self.current_item = self.current_shape(self.start_x, self.start_y, event.x, event.y)
        elif self.current_action == 'move':
            self.current_item = self.canvas.find_closest(event.x, event.y)[0]
            print(self.current_item)
            if self.current_item == 1:
                self.current_item = None
                return
            self.start_x = event.x
            self.start_y = event.y

    def on_drag(self, event):
        if self.current_action == 'create':
            self.canvas.coords(self.current_item, self.start_x, self.start_y, event.x, event.y)
        elif self.current_action == 'move' and self.current_item:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.current_item, dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def on_release(self, event):
        if self.current_action == 'create':
            self.canvas.coords(self.current_item, self.start_x, self.start_y, event.x, event.y)
            self.current_item = None  # Reset the current item
        if self.current_action == 'select':
            self.current_item = self.canvas.find_closest(event.x, event.y)[0]
            print(self.current_item)
            if self.current_item == 1:
                self.current_item = None
                return
            current_color = self.canvas.itemcget(self.current_item, "fill")
            new_color = "red" if current_color != "red" else "green"
            self.canvas.itemconfig(self.current_item, fill=new_color)
            self.current_item = None

    def create_rectangle(self, x1, y1, x2, y2):
        return self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='green', tags='rectangle')

    def create_oval(self, x1, y1, x2, y2):
        return self.canvas.create_oval(x1, y1, x2, y2, outline='black', fill='green')

    def create_line(self, x1, y1, x2, y2):
        return self.canvas.create_line(x1, y1, x2, y2, fill='black')

    def delete_shape(self, event):
        if self.current_action == "select":
            self.current_item = self.canvas.find_closest(event.x, event.y)
            print(self.current_item)
            if self.current_item == ():
                self.current_item = None
                return
            
            self.current_item = self.current_item[0]
            if self.current_item == 1:
                self.current_item = None
                return
            
            self.canvas.delete(self.current_item)
            self.current_item = None

def browse_files(SBM):
    global SBM_full_text

    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                    title="Select Battle Map")
    SBM.config(text = filename.split("/")[-1])
    SBM_full_text = filename
    
if __name__ == "__main__":
    global SBM_full_text
    SBM_full_text = None
    root = tk.Tk()
    selectedBattleMap = tk.Label(root, text=None)
    selectedBattleMap.grid(row=0, column=1)

    tk.Label(root, text=("Selected Battle Map: ")).grid(row=0, column=0)
    tk.Button(root, text="Browse Files", command= lambda: browse_files(selectedBattleMap)).grid(row=0, column=2)
    tk.Button(root, text="Open Battle Map Tool", command=lambda: DrawShapeApp(root, SBM_full_text)).grid(row=0, column=3)
    #app = DrawShapeApp(root)
    root.title("Draw Shapes")
    root.mainloop()