# Developed by: EL KHOUAJA KHALID
# elkhouajakhalid@gmail.com
# Date of publication: 13/01/2024
# Copyright @ 2024. All rights reserved.
########### Imports Necessary libraries ###########
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser, filedialog, messagebox, font
import PIL.ImageGrab as ImageGrab
from tktooltip import ToolTip  # Provides a tooltip (pop-up) widget for tkinter
import re  # Support for regular expressions (RE).

PAINTVERSION = "Paint 1.1.0"


class PaintApp:
    """Defining the PaintApp class."""

    def __init__(self, root):
        """Inilialize the properties of PaintApp class

        Args:
            root (_type_): _description_
        """
        self.root = root

        self.canvas_width = 900  # Canvas Width
        self.canvas_height = 600  # Canvas height
        # Construct canvas widget
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#FFFFFF",
            bd=0,
            relief=tk.SUNKEN,
        )
        self.canvas.pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=True, ipadx=4, ipady=4, padx=2, pady=2
        )

        self.setup_navbar()
        self.setup_tools()
        self.setup_events()
        self.prev_x = None
        self.prev_y = None

    def setup_navbar(self):
        """Setup the Navbar menu.\n
        File menu -> Save and Exit \n
        Edit menu -> Undo \n
        About menu -> About window
        """
        self.navbar = tk.Menu(
            self.root,
            background="#F7F9FC",
            foreground="#19191A",
            activebackground="#0060C0",
            activeforeground="#FFFFFF",
        )
        self.root.config(menu=self.navbar)

        # File menu
        self.file_menu = tk.Menu(
            self.navbar,
            tearoff=False,
            background="#F7F9FC",
            foreground="#19191A",
            activebackground="#0060C0",
            activeforeground="#FFFFFF",
        )
        self.navbar.add_cascade(label="File", menu=self.file_menu)
        self.save_icon = tk.PhotoImage(
            file="./assets/save_icon.png", height=16, width=16
        )
        self.file_menu.add_command(
            label="Save", image=self.save_icon, compound=tk.LEFT, command=self.save_as
        )
        self.file_menu.add_separator(background="#EBEBEB")
        self.exit_icon = tk.PhotoImage(
            file="./assets/exit_icon.png", height=16, width=16
        )
        self.file_menu.add_command(
            label="Exit", image=self.exit_icon, compound=tk.LEFT, command=self.root.quit
        )

        # Edit menu
        self.edit_menu = tk.Menu(
            self.navbar,
            tearoff=False,
            background="#F7F9FC",
            foreground="#19191A",
            activebackground="#0060C0",
            activeforeground="#FFFFFF",
        )
        self.navbar.add_cascade(label="Edit", menu=self.edit_menu)
        self.undo_icon = tk.PhotoImage(
            file="./assets/undo_icon.png", height=16, width=16
        )
        self.edit_menu.add_command(
            label="Undo", image=self.undo_icon, compound=tk.LEFT, command=self.undo
        )

        # About menu
        self.about_menu = tk.Menu(
            self.navbar,
            tearoff=False,
            background="#F7F9FC",
            foreground="#19191A",
            activebackground="#0060C0",
            activeforeground="#FFFFFF",
        )
        self.navbar.add_cascade(label="About", menu=self.about_menu)
        self.about_icon = tk.PhotoImage(
            file="./assets/about_icon.png", height=16, width=16
        )
        self.about_menu.add_command(
            label="About", image=self.about_icon, compound=tk.LEFT, command=self.about
        )

    def setup_tools(self):
        """Setup the Tools LabelFrame.\n
        Tools Frame -> Pen , Eraser and Clear canvas (New Page) \n
        Brush Size Frame -> Change the brush size from the dropdown list. \n
        Colours Frame -> Choose default colours or open color shooser palette.
        Pen style Frame -> Select pen style from the dropdown list ["line", "round", "square", "arrow", "diamond"] \n
        Shapes Frame -> Select shapes, rectangle, filled rectangle, circle(oval) , filled circle(oval), line \n
        Text Frame -> Enter a text, choose font style and size then click the "I" button to draw it.
        """
        self.selected_tool = "pen"  # Initialize selected tool to "pen"
        self.selected_color = "#000000"  # Initialize selected color to "black"
        self.choosecolor = ""
        self.brush_sizes = [
            1,
            2,
            3,
            4,
            5,
            6,
            8,
            10,
            15,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            100,
            150,
        ]
        self.selected_size = self.brush_sizes[1]  # Initialize selected size to "2"
        self.pen_types = ["line", "round", "square", "arrow", "diamond"]
        self.selected_pen_type = self.pen_types[
            0
        ]  # Initialize selected pen type to "line"

        # Getting all the font families installed in computer and display them in the text widget, so the user can change the font family from the dropdown list.
        self.fonts_families = []
        for i in sorted(font.families()):
            if re.match(r"^@", i) == None:
                self.fonts_families.append(i)
        self.selected_fonts_families = "Tahoma"

        self.text_sizes = [
            8,
            9,
            10,
            11,
            12,
            14,
            16,
            18,
            20,
            22,
            24,
            26,
            28,
            30,
            32,
            34,
            36,
            38,
            40,
            42,
            50,
            60,
            70,
        ]
        self.selected_text_size = self.text_sizes[
            4
        ]  # # Initialize selected text size to "12"
        # Tools frame
        self.tool_frame = ttk.LabelFrame(self.root, text="Tools", labelanchor="nw")
        self.tool_frame.pack(
            side=tk.LEFT, ipadx=4, ipady=4, padx=5, pady=5, fill=tk.BOTH
        )

        # Brush Size frame
        self.brush_frame = ttk.LabelFrame(
            self.root, text="Brush Size:", labelanchor="nw"
        )
        self.brush_frame.pack(
            side=tk.LEFT, ipadx=4, ipady=4, padx=5, pady=5, fill=tk.BOTH
        )

        # Colours frame
        self.colours_frame = ttk.LabelFrame(self.root, text="Colours", labelanchor="nw")
        self.colours_frame.pack(
            side=tk.LEFT, ipadx=4, ipady=4, padx=5, pady=5, fill=tk.BOTH
        )

        # Pen Style frame
        self.pen_type_frame = ttk.LabelFrame(
            self.root, text="Pen Style", labelanchor="nw"
        )
        self.pen_type_frame.pack(
            side=tk.LEFT, ipadx=4, ipady=4, padx=5, pady=5, fill=tk.BOTH
        )

        # Shapes frame
        self.shapes_frame = ttk.LabelFrame(self.root, text="Shapes", labelanchor="nw")
        self.shapes_frame.pack(
            side=tk.LEFT, ipadx=4, ipady=4, padx=5, pady=5, fill=tk.BOTH
        )

        # Text frame
        self.text_frame = ttk.LabelFrame(self.root, text="Text", labelanchor="nw")
        self.text_frame.pack(
            side=tk.LEFT,
            ipadx=4,
            ipady=4,
            padx=5,
            pady=5,
            fill=tk.BOTH,
        )

        ## TODO : customize the current colours, tools label
        # Show the current color and tool at the top right
        self.current_color_label = ttk.Label(
            self.root,
            text=self.selected_tool,
            border=2,
            borderwidth=1,
            font=("Fira Code", 12, "bold"),
            background=self.selected_color,
            foreground="#ffffff",
            justify=tk.CENTER,
            padding=4,
        )
        self.current_color_label.pack(
            side=tk.RIGHT, padx=(0, 4), pady=(10, 20), ipadx=0, ipady=0
        )

        # Undo button to delete last changes
        self.undo_icon = tk.PhotoImage(
            file="./assets/undo32_icon.png", height=32, width=32
        )
        self.undo_btn = tk.Button(
            self.root,
            image=self.undo_icon,
            compound=tk.LEFT,
            text="",
            bg="#FAFAFD",
            activebackground="#FAFAFD",
            width=32,
            height=32,
            border=0,
            borderwidth=0,
            command=self.undo,
        )
        self.undo_btn.pack(
            side=tk.RIGHT, padx=(10, 10), pady=(10, 20), ipadx=4, ipady=4
        )

        # Text Entry and font families combobox
        self.entry_text = ttk.Entry(self.text_frame)
        self.entry_text.pack(side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4)

        self.fonts_families_combobox = ttk.Combobox(
            self.text_frame,
            values=self.fonts_families,
            state="readonly",
            width=20,
            font=(self.selected_fonts_families, 8, ""),
        )
        self.fonts_families_combobox.current(0)
        self.fonts_families_combobox.pack(
            side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4
        )
        self.fonts_families_combobox.bind(
            "<<ComboboxSelected>>",
            lambda event: self.select_font_family(self.fonts_families_combobox.get()),
        )

        # Text size selector
        self.text_size_combobox = ttk.Combobox(
            self.text_frame,
            values=self.text_sizes,
            state="readonly",
            width=5,
            font=("Fira Code", 8, "bold"),
        )
        self.text_size_combobox.current(0)
        self.text_size_combobox.pack(
            side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4
        )
        self.text_size_combobox.bind(
            "<<ComboboxSelected>>",
            lambda event: self.select_text_size(int(self.text_size_combobox.get())),
        )

        # Text button to draw the text from the Text Entry
        self.text_icon = tk.PhotoImage(
            file="./assets/text_icon.png", height=16, width=16
        )
        self.text_button = ttk.Button(
            self.text_frame,
            image=self.text_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.draw_text,
        )
        self.text_button.pack(side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4)
        ToolTip(
            self.text_button,
            msg="Type a text in the input to draw it.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            delay=0.0,
            follow=True,
        )

        # Draw Rectangle tool
        self.rectangle_icon = tk.PhotoImage(
            file="./assets/rectangle_icon.png", height=16, width=16
        )
        self.rectangle_button = ttk.Button(
            self.shapes_frame,
            image=self.rectangle_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.draw_rectangle,
        )
        self.rectangle_button.pack(
            side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4
        )
        ToolTip(
            self.rectangle_button,
            msg="Select color to Draw a an empty rectangle.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )

        # Draw Filled Rectangle tool
        self.f_rectangle_icon = tk.PhotoImage(
            file="./assets/f_rectangle_icon.png", height=16, width=16
        )
        self.f_rectangle_button = ttk.Button(
            self.shapes_frame,
            image=self.f_rectangle_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.draw_filled_rectangle,
        )
        self.f_rectangle_button.pack(
            side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4
        )
        ToolTip(
            self.f_rectangle_button,
            msg="Select fill color to Draw a filled rectangle.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )

        # Draw Circle tool
        self.circle_icon = tk.PhotoImage(
            file="./assets/circle_icon.png", height=16, width=16
        )
        self.circle_button = ttk.Button(
            self.shapes_frame,
            image=self.circle_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.draw_circle,
        )
        self.circle_button.pack(
            side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4
        )
        ToolTip(
            self.circle_button,
            msg="Select color to Draw a circle.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )

        # Draw Filled Circle tool
        self.f_circle_icon = tk.PhotoImage(
            file="./assets/f_circle_icon.png", height=16, width=16
        )
        self.f_circle_button = ttk.Button(
            self.shapes_frame,
            image=self.f_circle_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.draw_filled_circle,
        )
        self.f_circle_button.pack(
            side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4
        )
        ToolTip(
            self.f_circle_button,
            msg="Select fill color to Draw a filled circle.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )

        # Draw Line tool
        self.line_icon = tk.PhotoImage(
            file="./assets/line_icon.png", height=16, width=16
        )
        self.line_button = ttk.Button(
            self.shapes_frame,
            image=self.line_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.draw_line,
        )
        self.line_button.pack(side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4)
        ToolTip(
            self.line_button,
            msg="Select color to Draw a line.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )

        self.rectangles = []

        # Pen tool
        self.pen_icon = tk.PhotoImage(file="./assets/pen_icon.png", height=16, width=16)
        self.pen_button = ttk.Button(
            self.tool_frame,
            image=self.pen_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.select_pen_tool,
        )  # Pen
        self.pen_button.pack(side=tk.LEFT, padx=(2, 2), pady=(0, 0), ipadx=4, ipady=4)
        ToolTip(
            self.pen_button,
            msg="Pen tool.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )
        # Eraser tool
        self.eraser_icon = tk.PhotoImage(
            file="./assets/eraser_icon.png", height=16, width=16
        )
        self.eraser_button = ttk.Button(
            self.tool_frame,
            image=self.eraser_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.select_eraser_tool,
        )  # Eraser
        self.eraser_button.pack(side=tk.LEFT, padx=2, pady=0, ipadx=4, ipady=4)
        ToolTip(
            self.eraser_button,
            msg="Eraser tool.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )
        # Clear tool
        self.clear_icon = tk.PhotoImage(
            file="./assets/clear_icon.png", height=16, width=16
        )
        self.clear_button = ttk.Button(
            self.tool_frame,
            image=self.clear_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.clear_canvas,
        )  # Clear
        self.clear_button.pack(side=tk.LEFT, padx=2, pady=0, ipadx=4, ipady=4)
        ToolTip(
            self.clear_button,
            msg="Clear Canvas (New page).",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )
        # Select Brush Size tool
        self.brush_size_combobox = ttk.Combobox(
            self.brush_frame,
            values=self.brush_sizes,
            state="readonly",
            width=8,
            font=("Fira Code", 10, "bold"),
        )
        self.brush_size_combobox.current(0)
        self.brush_size_combobox.pack(side=tk.TOP, padx=5, pady=5)
        self.brush_size_combobox.bind(
            "<<ComboboxSelected>>",
            lambda event: self.select_size(int(self.brush_size_combobox.get())),
        )

        ##TODO : Add more colours
        # Select colours tool
        self.black = tk.PhotoImage(
            file="./assets/colors/black.png", height=16, width=16
        )
        self.black_btn = tk.Button(
            self.colours_frame,
            image=self.black,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#000000"),
        )
        self.black_btn.pack(side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0)

        self.red = tk.PhotoImage(file="./assets/colors/red.png", height=16, width=16)
        self.red_btn = tk.Button(
            self.colours_frame,
            image=self.red,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#ec1c24"),
        )
        self.red_btn.pack(side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0)

        self.green = tk.PhotoImage(
            file="./assets/colors/green.png", height=16, width=16
        )
        self.green_btn = tk.Button(
            self.colours_frame,
            image=self.green,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#0ed145"),
        )
        self.green_btn.pack(side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0)

        self.yellow = tk.PhotoImage(
            file="./assets/colors/yellow.png", height=16, width=16
        )
        self.yellow_btn = tk.Button(
            self.colours_frame,
            image=self.yellow,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#fff200"),
        )
        self.yellow_btn.pack(side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0)

        self.indigo = tk.PhotoImage(
            file="./assets/colors/indigo.png", height=16, width=16
        )
        self.indigo_btn = tk.Button(
            self.colours_frame,
            image=self.indigo,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#3f48cc"),
        )
        self.indigo_btn.pack(side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0)

        self.gold = tk.PhotoImage(file="./assets/colors/gold.png", height=16, width=16)
        self.gold_btn = tk.Button(
            self.colours_frame,
            image=self.gold,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#ffca18"),
        )
        self.gold_btn.pack(side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0)

        self.lime = tk.PhotoImage(file="./assets/colors/lime.png", height=16, width=16)
        self.lime_btn = tk.Button(
            self.colours_frame,
            image=self.lime,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#c4ff0e"),
        )
        self.lime_btn.pack(side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0)

        self.pink = tk.PhotoImage(file="./assets/colors/pink.png", height=16, width=16)
        self.pink_btn = tk.Button(
            self.colours_frame,
            image=self.pink,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#b83dba"),
        )
        self.pink_btn.pack(side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0)

        self.turquoise = tk.PhotoImage(
            file="./assets/colors/turquoise.png", height=16, width=16
        )
        self.turquoise_btn = tk.Button(
            self.colours_frame,
            image=self.turquoise,
            compound=tk.LEFT,
            text="",
            width=20,
            height=20,
            border=0,
            command=lambda e=self.selected_color: self.select_color("#00a8f3"),
        )
        self.turquoise_btn.pack(
            side=tk.LEFT, padx=(4, 4), pady=(0, 0), ipadx=0, ipady=0
        )
        # Select custom color tool
        self.color_choser_icon = tk.PhotoImage(
            file="./assets/color_choser_icon.png", height=16, width=16
        )
        self.color_choser_button = ttk.Button(
            self.colours_frame,
            image=self.color_choser_icon,
            compound=tk.LEFT,
            text="",
            width=2,
            command=self.chose_color,
        )  # Chose color
        self.color_choser_button.pack(side=tk.LEFT, padx=2, pady=0, ipadx=4, ipady=4)
        ToolTip(
            self.color_choser_button,
            msg="Color Choser.",
            bg="#FAFAFD",
            fg="#1A1A1B",
            bd=0,
        )

        # Select Pen Type tool
        self.pen_type_combobox = ttk.Combobox(
            self.pen_type_frame,
            values=self.pen_types,
            state="readonly",
            width=12,
            font=("Fira Code", 10, "bold"),
        )
        self.pen_type_combobox.current(0)
        self.pen_type_combobox.pack(side=tk.TOP, padx=5, pady=5)
        self.pen_type_combobox.bind(
            "<<ComboboxSelected>>",
            lambda event: self.select_pen_type(self.pen_type_combobox.get()),
        )

    def setup_events(self):
        """Bind the nessesary events to the Canvas widget.\n
        Bind <B1-Motion> to draw. \n
        Bind <ButtonRelease-1> to trigger the Button Release. \n
        Bind CTRL+S , CTRL+Z to Save and Undo.\n
        """
        self.root.bind("<Control-s>", self.save_as)  # Save file using CTRL+S
        self.root.bind("<Control-z>", self.undo)  # UNDO using CTRL+Z
        self.root.bind("<Control-n>", self.clear_canvas)  # UNDO using CTRL+Z

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.release)

    def select_pen_tool(self):
        """Define pen tool function to change the selected pen."""
        self.selected_tool = "pen"
        self.selected_color = "#000000"
        self.current_color_label.configure(
            background=self.selected_color,
            text=self.selected_tool,
            foreground="#FFFFFF",
        )
        self.canvas.unbind("<ButtonPress-1>")
        self.setup_events()

    def select_eraser_tool(self):
        """Define eraser tool function to change the selected pen to eraser."""
        self.selected_tool = "eraser"
        self.selected_color = "#FFFFFF"
        self.current_color_label.configure(
            background=self.selected_color,
            text=self.selected_tool,
            foreground="#000000",
        )
        self.canvas.unbind("<ButtonPress-1>")
        self.setup_events()

    def select_size(self, size):
        """Define select pen size function to change the size of the pen tool."""
        self.selected_size = size

    def select_text_size(self, size):
        """Define text size function to change the size of the text tool."""
        self.selected_text_size = size

    def select_font_family(self, font_name):
        """Define font family function to change the font of the text tool."""
        self.selected_fonts_families = font_name
        self.fonts_families_combobox.configure(font=(font_name, 8, ""))

    def select_color(self, color):
        """Define color pen function to change the color of the pen tool."""
        self.selected_color = color
        self.current_color_label.configure(background=self.selected_color)

    def select_pen_type(self, pen_type):
        """Define select pen type function to change the type of the pen tool."""
        self.selected_pen_type = pen_type

    def draw(self, event):
        """Define the Draw function that allow the user to draw on the Canvas widget, depending on the selected pen type."""
        if self.selected_tool == "pen" or self.selected_tool == "eraser":
            if self.prev_x is not None and self.prev_y is not None:
                if self.selected_pen_type == "line":
                    self.canvas.create_line(
                        self.prev_x,
                        self.prev_y,
                        event.x,
                        event.y,
                        fill=self.selected_color,
                        width=self.selected_size,
                        smooth=True,
                    )
                elif self.selected_pen_type == "round":
                    x1 = event.x - self.selected_size
                    y1 = event.y - self.selected_size
                    x2 = event.x + self.selected_size
                    y2 = event.y + self.selected_size
                    self.canvas.create_oval(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=self.selected_color,
                        outline=self.selected_color,
                    )
                elif self.selected_pen_type == "square":
                    x1 = event.x - self.selected_size
                    y1 = event.y - self.selected_size
                    x2 = event.x + self.selected_size
                    y2 = event.y + self.selected_size
                    self.canvas.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=self.selected_color,
                        outline=self.selected_color,
                    )
                elif self.selected_pen_type == "arrow":
                    x1 = event.x - self.selected_size
                    y1 = event.y - self.selected_size
                    x2 = event.x + self.selected_size
                    y2 = event.y + self.selected_size
                    self.canvas.create_polygon(
                        x1,
                        y1,
                        x1,
                        y2,
                        event.x,
                        y2,
                        fill=self.selected_color,
                        outline=self.selected_color,
                    )
                elif self.selected_pen_type == "diamond":
                    x1 = event.x - self.selected_size
                    y1 = event.y
                    x2 = event.x
                    y2 = event.y - self.selected_size
                    x3 = event.x + self.selected_size
                    y3 = event.y
                    x4 = event.x
                    y4 = event.y + self.selected_size
                    self.canvas.create_polygon(
                        x1,
                        y1,
                        x2,
                        y2,
                        x3,
                        y3,
                        x4,
                        y4,
                        fill=self.selected_color,
                        outline=self.selected_color,
                    )
            self.prev_x = event.x
            self.prev_y = event.y

    def release(self, event):
        """Define the release function that allow inialize the prev_x and prev_y coordinates to zeros."""
        self.prev_x = None
        self.prev_y = None

    def clear_canvas(self, event=False):
        """Define the clear Canvas function that allow to delete all objects from Canvas."""
        self.canvas.delete("all")

    def draw_rectangle(self):
        """Define the rectangle function that allow to bind start and stop events to draw a rectangle."""
        self.selected_color = "#000000"
        self.current_color_label.configure(
            background=self.selected_color, foreground="#FFFFFF"
        )
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<ButtonPress-1>", self.start_draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw_rectangle)

    def start_draw_rectangle(self, event):
        """Define the draw rectangle function that allow inialize the prev_x and prev_y coordinates."""
        self.selected_tool = "rectangle"
        self.prev_x, self.prev_y = event.x, event.y
        self.current_color_label.configure(text=self.selected_tool)

    def stop_draw_rectangle(self, event):
        """Define the draw rectangle function that allow to draw a rectangle."""
        if self.selected_tool == "rectangle":
            if self.prev_x is not None and self.prev_y is not None:
                self.canvas.create_rectangle(
                    self.prev_x,
                    self.prev_y,
                    event.x,
                    event.y,
                    outline=self.selected_color,
                    width=self.selected_size,
                )
                self.prev_x = None
                self.prev_y = None

    def draw_filled_rectangle(self):
        """Define the filled rectangle function that allow to bind start and stop events to draw a filled rectangle."""
        self.selected_color = "#000000"
        self.current_color_label.configure(
            background=self.selected_color, foreground="#FFFFFF"
        )
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<ButtonPress-1>", self.start_draw_filled_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw_filled_rectangle)

    def start_draw_filled_rectangle(self, event):
        """Define the draw filled rectangle function that allow inialize the prev_x and prev_y coordinates."""
        self.selected_tool = "frectangle"
        self.prev_x, self.prev_y = event.x, event.y
        self.current_color_label.configure(text=self.selected_tool)

    def stop_draw_filled_rectangle(self, event):
        """Define the draw filled rectangle function that allow to draw a filled rectangle."""
        if self.selected_tool == "frectangle":
            if self.prev_x is not None and self.prev_y is not None:
                self.canvas.create_rectangle(
                    self.prev_x,
                    self.prev_y,
                    event.x,
                    event.y,
                    outline=self.selected_color,
                    fill=self.selected_color,
                    width=self.selected_size,
                )
                self.prev_x = None
                self.prev_y = None

    def draw_text(self):
        """Define the draw text function that allow to bind start and stop events to draw a text."""
        self.current_color_label.configure(
            background=self.selected_color, foreground="#FFFFFF"
        )
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<ButtonPress-1>", self.start_draw_text)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw_text)

    def start_draw_text(self, event):
        """Define the draw text function that allow inialize the prev_x and prev_y coordinates."""
        self.selected_tool = "text"
        self.prev_x, self.prev_y = event.x, event.y
        self.current_color_label.configure(text=self.selected_tool)

    def stop_draw_text(self, event):
        """Define the draw text function that allow to draw a text."""
        if self.selected_tool == "text" and self.entry_text.get() != "":
            if self.prev_x is not None and self.prev_y is not None:
                self.canvas.create_text(
                    event.x,
                    event.y,
                    anchor="w",
                    fill=self.selected_color,
                    text=self.entry_text.get(),
                    font=(
                        self.selected_fonts_families,
                        self.selected_text_size,
                        "bold",
                    ),
                )
                self.prev_x = None
                self.prev_y = None
        else:
            messagebox.showinfo("Info", "Entry text is empty")

    def chose_color(self):
        """Define the choose color function."""
        self.choosecolor = colorchooser.askcolor()
        self.selected_color = self.choosecolor[1]
        self.current_color_label.configure(background=self.selected_color)

    def draw_circle(self):
        """Define the circle function that allow to bind start and stop events to draw a circle."""
        self.selected_color = "#000000"
        self.current_color_label.configure(
            background=self.selected_color, foreground="#FFFFFF"
        )
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<ButtonPress-1>", self.start_draw_circle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw_circle)

    def start_draw_circle(self, event):
        """Define the draw circle function that allow inialize the prev_x and prev_y coordinates."""
        self.selected_tool = "circle"
        self.prev_x, self.prev_y = event.x, event.y
        self.current_color_label.configure(text=self.selected_tool)

    def stop_draw_circle(self, event):
        """Define the draw circle function that allow to draw a circle."""
        if self.selected_tool == "circle":
            if self.prev_x is not None and self.prev_y is not None:
                self.canvas.create_oval(
                    event.x,
                    event.y,
                    self.prev_x,
                    self.prev_y,
                    outline=self.selected_color,
                    width=self.selected_size,
                )
                self.prev_x = None
                self.prev_y = None

    def draw_filled_circle(self):
        """Define the filled circle function that allow to bind start and stop events to draw a filled circle."""
        self.selected_color = "#000000"
        self.current_color_label.configure(
            background=self.selected_color, foreground="#FFFFFF"
        )
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<ButtonPress-1>", self.start_draw_filled_circle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw_filled_circle)

    def start_draw_filled_circle(self, event):
        """Define the draw filled circle function that allow inialize the prev_x and prev_y coordinates."""
        self.selected_tool = "fcircle"
        self.prev_x, self.prev_y = event.x, event.y
        self.current_color_label.configure(text=self.selected_tool)

    def stop_draw_filled_circle(self, event):
        """Define the draw filled circle function that allow to draw a filled circle."""
        r = 3
        if self.selected_tool == "fcircle":
            if self.prev_x is not None and self.prev_y is not None:
                self.canvas.create_oval(
                    event.x,
                    event.y,
                    self.prev_x,
                    self.prev_y,
                    outline=self.selected_color,
                    fill=self.selected_color,
                    width=self.selected_size,
                )

                self.prev_x = None
                self.prev_y = None

    def draw_line(self):
        """Draw a line\n
        Unbidding the olds canvas bind and setting new bind to the Canvas.\n
        Unbind <B1-Motion> and <ButtonRelease-1> from Canvas.\n
        Bind <ButtonPress-1> to start the draw line.\n
        Bind <ButtonRelease-1> to stop the draw line and create line with coordinates.
        """
        self.selected_color = "#000000"
        self.current_color_label.configure(
            background=self.selected_color, foreground="#FFFFFF"
        )
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<ButtonPress-1>", self.start_draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw_line)

    def start_draw_line(self, event):
        """Start the drawing by setting the previous x and y to event.x and event.y

        Args:
            event (_type_): _description_
        """
        self.selected_tool = "line"
        self.prev_x, self.prev_y = event.x, event.y
        self.current_color_label.configure(text=self.selected_tool)

    def stop_draw_line(self, event):
        """Stop the drawing line.\n
        Create line on canvas by grabing the coordinates from previous prev_x and prev_y and the new coords event.x and event.y\n
        Also setting the fill color and width of the line.

        Args:
            event (_type_): _description_
        """
        if self.selected_tool == "line":
            if self.prev_x is not None and self.prev_y is not None:
                self.canvas.create_line(
                    event.x,
                    event.y,
                    self.prev_x,
                    self.prev_y,
                    fill=self.selected_color,
                    width=self.selected_size,
                )

                self.prev_x = None
                self.prev_y = None

    def save_as(self, event=False):
        """Open a dialog to save the drawing as .jpg or .png files.

        Args:
            event (bool, optional): _description_. Defaults to False.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPG files", "*.jpg"), ("PNG files", "*.png")],
        )
        if file_path:
            try:
                x = self.root.winfo_rootx() + self.canvas.winfo_x()
                y = self.root.winfo_rooty() + self.canvas.winfo_y()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()
                ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
                messagebox.showinfo("Save Drawing", "Image file saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the image file: {e}")

    def undo(self, event=False):
        """Undo the last changes in the canvas. delete the last drawing object from Canvas.\n
        Also you can use the CTRL + Z to undo the last changes.

        Args:
            event (bool, optional): _description_. Defaults to False.
        """
        items = self.canvas.find_all()
        if items:
            self.canvas.delete(items[-1])
            # self.stack.append(items[-1])

    def about(self):
        """Open the About Window, that contain the app name, logo and version."""
        WIDTH = 450
        HEIGHT = 250
        root_window_width = self.root.winfo_screenwidth()
        root_window_height = self.root.winfo_screenheight()

        # Toplevel object which will be treated as a new window
        aboutWindow = tk.Toplevel(self.root)
        # sets the title of the Toplevel widget
        aboutWindow.title("About Paint")
        aboutWindow.resizable(False, False)
        aboutWindow.attributes("-alpha", 0.9)

        # Make the about window at the center of the screen.
        x = int((root_window_width / 2) - (WIDTH / 2))
        y = int((root_window_height / 2) - (HEIGHT / 2))

        aboutWindow.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

        about_window_frame = ttk.Frame(aboutWindow, border=2)
        about_window_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.main_icon = tk.PhotoImage(
            file="./assets/paint_64.png", height=64, width=64
        )

        tk.Label(
            about_window_frame,
            compound=tk.TOP,
            justify=tk.CENTER,
            image=self.main_icon,
            text="",
            height=64,
            width=WIDTH,
        ).pack(padx=2, pady=2, ipadx=5, ipady=5, fill=tk.BOTH)

        tk.Label(
            about_window_frame,
            foreground="black",
            justify=tk.LEFT,
            width=WIDTH,
            font=("Fira Code", 12, "bold"),
            text=PAINTVERSION,
        ).pack(side=tk.TOP, padx=2, pady=2, ipadx=5, ipady=5)

        tk.Label(
            about_window_frame,
            width=WIDTH,
            foreground="black",
            justify=tk.LEFT,
            font=("Fira Code", 12, "bold"),
            text="Developed by:\n       EL KHOUAJA KHALID\n\nCopyright @ 2024. All rights reserved.\n",
        ).pack(side=tk.TOP, padx=2, pady=2, ipadx=5, ipady=5)


if __name__ == "__main__":
    # Inilialize the Splash Screen first.
    splash_screen = tk.Tk()
    splash_screen_w = 512  # 300x200
    splash_screen_h = 341
    splash_screen.resizable(False, False)

    splash_screen.configure(bg="")
    splash_screen.overrideredirect(True)
    splash_screen.lift()
    splash_screen.wm_attributes("-topmost", True)
    splash_screen.wm_attributes("-disabled", True)
    splash_screen.wm_attributes("-transparentcolor", "white")

    splash_screen.attributes("-alpha", 1)
    splash_screen.configure(bd=0, borderwidth=0, border=0)

    # Make the Splash Screen window at the center of the screen.
    x = int((splash_screen.winfo_screenwidth() / 2) - (splash_screen_w / 2))
    y = int((splash_screen.winfo_screenheight() / 2) - (splash_screen_h / 2))
    splash_screen.geometry(f"{splash_screen_w}x{splash_screen_h}+{x}+{y}")

    bg_screen_img = tk.PhotoImage(
        file="./assets/sc_512_341.png", width=splash_screen_w, height=splash_screen_h
    )
    label_bg = tk.Label(
        splash_screen,
        bg="#FFFFFF",
        image=bg_screen_img,
        justify=tk.CENTER,
        width=splash_screen_w,
        height=splash_screen_h,
        compound=tk.TOP,
        font=("Fira Code", 16, "bold"),
    )
    label_bg.place(x=0, y=0, relwidth=1, relheight=1)

    def destroy_ss():
        """Close the Splash Screen and open the main window of Paint App."""
        splash_screen.destroy()

    # Destroy the Splash Screen after 1S and show the main window.
    splash_screen.after(1000, destroy_ss)
    splash_screen.mainloop()

    root = tk.Tk()
    root.title("Paint Application")
    # getting screen width and height of display
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    root.geometry("%dx%d" % (width, height))  # setting tkinter window size
    root.state("zoomed")  # make it full window zoomed
    root.configure(bg="#F9F9F9")
    root.iconbitmap("paint.ico")  # Add an icon to the main app
    app = PaintApp(root)  # Creating an object of the PaintApp class.
    root.mainloop()
