import tkinter as tk


class LeftMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_widgets()

    def build_widgets(self):
        #Since everything here is a button, and using a list is impossible (and a matrix would work), a dictionary was a better choice to save everything
        #Text = The text of the button
        #Image_Route = The route to the image of the button
        #Command = the action the button performs
        items = [
            {
                "text": "Activities",
                "image_route": "resources/placeholder.png",
                "command": self.activities_button,
            },
            {
                "text": "Students",
                "image_route": "resources/placeholder.png",
                "command": self.students_button,
            },
            {
                "text": "Announcements",
                "image_route": "resources/placeholder.png",
                "command": self.announcements_button,
            },
            {
                "text": "Reports",
                "image_route": "resources/placeholder.png",
                "command": self.reports_button,
            },
            {
                "text": "Configuration",
                "image_route": "resources/placeholder.png",
                "command": self.configuration_button,
            },
            {
                "text": "Log off",
                "image_route": "resources/placeholder.png",
                "command": self.log_off_button,
            },
        ]
        # Keep references to the images so Tkinter can display them.
        # EDITOR'S NOTE: I DON'T HAVE ANY IDEA WHAT THIS DOES, BUT IF NOT PRESENT THE MENU WON'T SHOW AT ALL
        self.images = [] # <-- DON'T TOUCH


        # Since a dictionary was used, we can circle around every entry and create the buttons that way
        # I really love dictionaries
        for item in items:
            image = tk.PhotoImage(file=item["image_route"])
            self.images.append(image)

            button = tk.Button(
                self,
                text=item["text"],
                image=image,
                compound="left", #The allingment of the elements
                command=item["command"],
                anchor="w", #Link it to the left
                padx=10,
                pady=6,
            )
            button.pack(fill="x") #The button expands to fill the space in X

    def activities_button(self):
        pass

    def students_button(self):
        pass

    def announcements_button(self):
        pass

    def reports_button(self):
        pass

    def configuration_button(self):
        pass

    def log_off_button(self):
        pass
