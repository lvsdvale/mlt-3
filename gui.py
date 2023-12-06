import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import *
from communication import *

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("MLT Algorithm")

        self.message_label = ttk.Label(master, text="Mensagem Original:")
        self.message_label.grid(row=0, column=0, pady=5)

        self.binary_label = ttk.Label(master, text="Mensagem em Binário:")
        self.binary_label.grid(row=1, column=0, pady=5)

        self.mlt_label = ttk.Label(master, text="Forma de Onda após MLT:")
        self.mlt_label.grid(row=2, column=0, pady=5)

        self.encrypted_label = ttk.Label(master, text="Mensagem Criptografada:")
        self.encrypted_label.grid(row=3, column=0, pady=5)

        self.message_entry = ttk.Entry(master)
        self.message_entry.grid(row=0, column=1, pady=5)

        self.binary_entry = ttk.Entry(master, state="readonly")
        self.binary_entry.grid(row=1, column=1, pady=5)

        self.mlt_entry = ttk.Entry(master, state="readonly")
        self.mlt_entry.grid(row=2, column=1, pady=5)

        self.encrypted_entry = ttk.Entry(master, state="readonly")
        self.encrypted_entry.grid(row=3, column=1, pady=5)

        self.encrypt_button = ttk.Button(master, text="Criptografar", command=self.encrypt_message)
        self.encrypt_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.plot_frame = ttk.Frame(master)
        self.plot_frame.grid(row=0, column=2, rowspan=5)

    def encrypt_message(self):
        message = self.message_entry.get()
        binary_message = ''
        for char in message:
            binary_char = bin(ord(char))[2:].zfill(8)  
            binary_message += binary_char

        
        mlt_algorithm = MLTAlgorithm()
        encrypted_message = mlt_algorithm.apply_mlt(binary_message)

        self.binary_entry.config(state="normal")
        self.mlt_entry.config(state="normal")
        self.encrypted_entry.config(state="normal")

        self.binary_entry.delete(0, tk.END)
        self.binary_entry.insert(0, " ".join(map(str, binary_message)))

        self.mlt_entry.delete(0, tk.END)
        self.mlt_entry.insert(0, " ".join(map(str, encrypted_message)))

        self.encrypted_entry.delete(0, tk.END)
        self.encrypted_entry.insert(0, " ".join(map(str, encrypted_message)))

        self.binary_entry.config(state="readonly")
        self.mlt_entry.config(state="readonly")
        self.encrypted_entry.config(state="readonly")

        self.plot_mlt_transform(encrypted_message)

    def plot_mlt_transform(self, mlt_transform):
        fig, ax = plt.subplots()
        ax.plot(mlt_transform)
        ax.set_title("Forma de Onda após MLT")
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0)