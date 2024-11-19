from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip, json
from cryptography.fernet import Fernet
import base64

# ---------------------------- Encryption/Decryption Initialization ------------------------------- #
secret_pw ="secret_password"
key = base64.b64encode(f"{secret_pw:<32}".encode("utf-8"))
encryptor = Fernet(key=key)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pass():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    selected_char = [choice(letters) for index in range(randint(8, 10))]

    selected_symbol = [choice(symbols) for index in range(randint(2, 4))]

    selected_num = [choice(numbers) for index in range(randint(2, 4))]

    password_list = selected_num + selected_symbol + selected_char
    shuffle(password_list)

    password = "".join(password_list)

    pass_entry.delete(0, END)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    web_val = web_entry.get()
    email_val = email_entry.get()
    pass_val = pass_entry.get()
    pass_val = encryptor.encrypt(pass_val.encode("utf-8")).decode(encoding="utf-8")
    new_data = {
        web_val: {
            "email": email_val,
            "password": pass_val
        }
    }

    if len(web_val) == 0 or len(pass_val) == 0:
        messagebox.showerror(title="Oops!", message="Please do not leave the fields empty!")
    else:
        try:
            with open("data.json", "r",encoding="utf-8") as data_file:
                pass
        except FileNotFoundError:
            with open("data.json", "w",encoding="utf-8") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "r",encoding="utf-8") as data_file:
                data = json.load(data_file)
                data.update(new_data)
            with open("data.json", "w",encoding="utf-8") as data_file:
                json.dump(data, data_file, indent=4)

        web_entry.delete(0, END)
        pass_entry.delete(0, END)

# ---------------------------- SEARCH PW ------------------------------- #


def find_password():
    web_val = web_entry.get()
    try:
        with open("data.json", "r",encoding="utf-8") as data_file:
            data = json.load(data_file)[web_val]
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    except KeyError:
        messagebox.showinfo(title="Error", message="No details for the website exists")
    else:
        email = data["email"]
        password = data["password"]
        password = encryptor.decrypt(password).decode("utf-8")
        messagebox.showinfo(title=web_val, message=f"Email: {email}\nPassword: {password}\n")
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(pady=40, padx=40)
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Label
web_label = Label(text="Website: ", font=("Montserrat", 10))
web_label.grid(column=0, row=1)

email_label = Label(text="Email/Username: ", font=("Montserrat", 10))
email_label.grid(column=0, row=2)

pass_label = Label(text="Password: ", font=("Montserrat", 10))
pass_label.grid(column=0, row=3)
# Entry

web_entry = Entry(width=32)
web_entry.grid(column=1, row=1)
web_entry.focus()

email_entry = Entry(width=50)
email_entry.grid(columnspan=2, column=1, row=2)
email_entry.insert(END, "someemail@gmail.com")
pass_entry = Entry(width=32)
pass_entry.grid(column=1, row=3)
# Button

search_btn = Button(text="Search", width=13, command=find_password)
search_btn.grid(column=2, row=1)

generate_btn = Button(text="Generate Password", command=generate_pass)
generate_btn.grid(column=2, row=3)

add_btn = Button(text="Add", width=43, command=save_data)
add_btn.grid(column=1, columnspan=2, row=4)

window.mainloop()