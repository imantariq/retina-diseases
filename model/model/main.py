from prediction import predictImage
import cv2
from tkinter import *
from tkinter import filedialog
import base64
from PIL import ImageTk, Image




def browseFiles():
    py = r"*jpeg"
    global result
    global img
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("images",py),("all files","*.*")))
    # check if file is jpeg
    if filename.endswith(".jpeg"):
        # predict the image
        img = cv2.imread(filename) #read the image 
        result = predictImage(img) #call the predict image function where the dip techniques are applied
        print(result)
        output_text.insert(END, result)
        # Encode image to base64
        _, buffer = cv2.imencode('.jpg', img)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # send a request to the server http://127.0.0.1:5000
        import requests
        url = "http://127.0.0.1:5000/insertInFirestore" #url that connects to the firebase where data saved 
        # read the image and convert it into bytes 
        img_name = filename.split("/")[-1]
        data = {"name":fullname_entry.get(), "age":age_entry.get(), "result":result, "image":image_base64, "img_name":img_name}
        response = requests.post(url, data=data)
        print(response.text)
        # select_label.config(text=filename)
    if filename == "":
        return

window = Tk()

# Set window title
window.title('Retina Analysis and Disease Detection')

# Set window size
window.geometry("800x600")

# Set window background color
window.config(background="#e8a010")
# Load background image
bg_image = Image.open("images.jpg")
bg_image = bg_image.resize((800, 600), Image.ANTIALIAS)
bg_image = ImageTk.PhotoImage(bg_image)

# Create canvas and set background image
canvas = Canvas(window, width=800, height=600)
canvas.pack(fill=BOTH, expand=True)
canvas.create_image(0, 0, image=bg_image, anchor=NW)
# Create label for title
title_label = Label(window, text="Retina Analysis and Disease Detection", font=("Helvetica", 22, "bold"), fg="#17202A",bg="#e8a010")
title_label.place(relx=0.5, rely=0.1, anchor=CENTER)

# Create label for full name
fullname_label = Label(window, text="Full Name", font=("Helvetica", 14), fg="#2C3E50", bg="#e8a010")
fullname_label.place(x=200, y=180)

# Create text box for full name
fullname_entry = Entry(window, font=("Helvetica", 12), bg="#e8a010", bd=0, highlightthickness=0)
fullname_entry.place(x=320, y=180, width=250, height=30)

# Create label for age
age_label = Label(window, text="Age", font=("Helvetica", 14), fg="#2C3E50", bg="#e8a010")
age_label.place(x=200, y=240)

# Create text box for age
age_entry = Entry(window, font=("Helvetica", 12), bg="#e8a010", bd=0, highlightthickness=0)
age_entry.place(x=320, y=230, width=250, height=30)

# Create "Browse Files" button
browse_button = Button(window, text="Browse Files", font=("Helvetica", 14), fg="#FFFFFF", bg="#e8a010", bd=0, highlightthickness=0, activebackground="#2ECC71", cursor="hand2", command=browseFiles)
browse_button.place(x=300, y=300, width=150, height=40)


select_label = Label(window, text="(Select an image)", font=("Helvetica", 10), fg="#2C3E50", bg="#e8a010")
select_label.place(x=310, y=270) 

# Create output label and text box
output_label = Label(window, text="Output:", font=("Helvetica", 12, "bold"), bg="#e8a010")
output_label.place(x=100, y=360)
output_text = Text(window, font=("Helvetica", 12), width=50, height=5,bg="#e8a010")
output_text.place(x=100, y=380)

# call addDataToDatabase function when button is clicked
# button1.config(command=addDataToDatabase)
window.mainloop()
