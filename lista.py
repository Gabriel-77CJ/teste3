import os
import tkinter as tk
from tkinter import messagebox, simpledialog

CONTACTS_DIR = "contacts"

if not os.path.exists(CONTACTS_DIR):
    os.makedirs(CONTACTS_DIR)

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contacts List")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.contact_listbox = tk.Listbox(root, font=("Arial", 12))
        self.contact_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.contact_listbox.bind("<<ListboxSelect>>", self.load_contact)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="➕ Add", width=10, command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="✏️ Edit", width=10, command=self.edit_contact).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="🗑️ Delete", width=10, command=self.delete_contact).grid(row=0, column=2, padx=5)

        # Contact info
        self.details = tk.Text(root, height=6, font=("Arial", 11))
        self.details.pack(fill="x", padx=10, pady=5)
        self.details.config(state="disabled")

        self.load_contacts()

    def load_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        for filename in os.listdir(CONTACTS_DIR):
            if filename.endswith(".txt"):
                self.contact_listbox.insert(tk.END, filename[:-4])

    def load_contact(self, event):
        selection = self.contact_listbox.curselection()
        if not selection:
            return
        name = self.contact_listbox.get(selection[0])
        filepath = os.path.join(CONTACTS_DIR, name + ".txt")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            self.details.config(state="normal")
            self.details.delete("1.0", tk.END)
            self.details.insert(tk.END, content)
            self.details.config(state="disabled")

    def add_contact(self):
        name = simpledialog.askstring("New Contact", "Enter name:")
        if not name:
            return
        filename = os.path.join(CONTACTS_DIR, name + ".txt")
        if os.path.exists(filename):
            messagebox.showerror("Error", "Contact already exists.")
            return

        phone = simpledialog.askstring("Phone Number", "Enter phone:")
        email = simpledialog.askstring("Email Address", "Enter email:")

        with open(filename, "w") as f:
            f.write(f"Name: {name}\nPhone: {phone}\nEmail: {email}")
        self.load_contacts()

    def edit_contact(self):
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showinfo("Edit Contact", "Select a contact to edit.")
            return

        name = self.contact_listbox.get(selection[0])
        filepath = os.path.join(CONTACTS_DIR, name + ".txt")
        if not os.path.exists(filepath):
            return

        with open(filepath, "r") as f:
            lines = f.readlines()

        name_val = lines[0].split(":", 1)[1].strip()
        phone_val = lines[1].split(":", 1)[1].strip()
        email_val = lines[2].split(":", 1)[1].strip()

        new_name = simpledialog.askstring("Edit Name", "Enter name:", initialvalue=name_val)
        new_phone = simpledialog.askstring("Edit Phone", "Enter phone:", initialvalue=phone_val)
        new_email = simpledialog.askstring("Edit Email", "Enter email:", initialvalue=email_val)

        # Update file
        os.remove(filepath)
        new_filepath = os.path.join(CONTACTS_DIR, new_name + ".txt")
        with open(new_filepath, "w") as f:
            f.write(f"Name: {new_name}\nPhone: {new_phone}\nEmail: {new_email}")
        self.load_contacts()

    def delete_contact(self):
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showinfo("Delete Contact", "Select a contact to delete.")
            return
        name = self.contact_listbox.get(selection[0])
        filepath = os.path.join(CONTACTS_DIR, name + ".txt")
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete {name}?")
        if confirm:
            os.remove(filepath)
            self.load_contacts()
            self.details.config(state="normal")
            self.details.delete("1.0", tk.END)
            self.details.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()