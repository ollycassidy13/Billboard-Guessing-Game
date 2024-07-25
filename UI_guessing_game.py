import customtkinter as ctk
import billboard
import requests
from PIL import Image, ImageTk
import io

def get_top_tracks(chart_name="hot-100", limit=100):
    chart = billboard.ChartData(chart_name)
    title = [entry.title for entry in chart.entries[:limit]]
    artist = [entry.artist for entry in chart.entries[:limit]]
    images = [entry.image for entry in chart.entries[:limit]]  # Get album cover images
    return title, artist, images

# Define the game logic
class BillboardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Billboard Top 100 Game")
        self.root.minsize(400, 500)
        
        ctk.set_appearance_mode("dark")  # Enable dark mode
        ctk.set_default_color_theme("dark-blue.json")  # Load the custom theme
        
        self.title, self.artist, self.images = get_top_tracks()
        self.n = 0
        self.attempts = 2
        self.correct_guess = False
        
        self.image_label = ctk.CTkLabel(root, text="")
        self.image_label.pack(pady=10)

        self.title_label = ctk.CTkLabel(root, text="Song 1: " + self.title[self.n])
        self.title_label.pack(pady=20)
        
        self.artist_label = ctk.CTkLabel(root, text="Who is the artist?")
        self.artist_label.pack(pady=10)
        
        self.entry = ctk.CTkEntry(root)
        self.entry.pack(pady=10)
        
        self.result_label = ctk.CTkLabel(root, text="")
        self.result_label.pack(pady=10)
        
        self.submit_button = ctk.CTkButton(root, text="Submit", command=self.on_button_click)
        self.submit_button.pack(pady=10)
        
        self.attempts_label = ctk.CTkLabel(root, text="3 attempts remaining")
        self.attempts_label.pack(pady=10)
    
    def on_button_click(self):
        if self.correct_guess:
            self.next_song()
        else:
            self.check_artist()
    
    def check_artist(self):
        guess = self.entry.get().replace(',', ' ').replace('&', ' ').lower().replace('featuring', ' ').replace(' ', '')
        correct_artist = self.artist[self.n].replace(',', ' ').replace('&', ' ').lower().replace('featuring', ' ').replace(' ', '')
        self.entry.delete(0, 'end')  # Clear the input box
        
        if guess == correct_artist:
            self.result_label.configure(text="Correct! The artist was: " + self.artist[self.n])
            self.display_image(self.images[self.n])  # Display the image
            self.correct_guess = True
            self.submit_button.configure(text="Continue")
            self.artist_label.pack_forget()
            self.entry.pack_forget()
        else:
            self.attempts -= 1
            if self.attempts > 0:
                self.result_label.configure(text="Incorrect, try again")
                self.attempts_label.configure(text=str(self.attempts) + " attempts remaining")
            else:
                self.result_label.configure(text="Game Over :( You scored " + str(self.n))
                self.submit_button.configure(state="disabled")
    
    def next_song(self):
        self.n += 1
        self.correct_guess = False
        self.attempts = 2  # Reset attempts for the next song
        if self.n < len(self.title):
            self.title_label.configure(text="Song " + str(self.n + 1) + ": " + self.title[self.n])
            self.attempts_label.configure(text="3 attempts remaining")
            self.result_label.configure(text="")
            self.image_label.configure(image=None)  # Remove the image
            self.submit_button.configure(text="Submit")
            self.artist_label.pack(pady=10)
            self.entry.pack(pady=10)
        else:
            self.result_label.configure(text="You won! You scored 100")
            self.submit_button.configure(state="disabled")
    
    def display_image(self, image_url):
        try:
            response = requests.get(image_url)
            image_data = io.BytesIO(response.content)
            img = Image.open(image_data)
            img = img.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo, text="")  # Ensure no text is displayed
            self.image_label.image = photo  # Keep a reference
        except Exception as e:
            self.result_label.configure(text=f"Image load error: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = BillboardGame(root)
    root.mainloop()
