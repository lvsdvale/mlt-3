import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import MLTAlgorithm
from communication import Communication
from cryptography.fernet import Fernet
import threading

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("MLT Algorithm")

        self.default_destination_ip = "127.0.0.1"  # IP padrão
        self.default_destination_port = 5001  # Porta padrão

        self.tab_control = ttk.Notebook(master)
        self.send_tab = ttk.Frame(self.tab_control)
        self.receive_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.send_tab, text="Enviar Mensagem")
        self.tab_control.add(self.receive_tab, text="Receber Mensagem")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_send_tab()
        self.setup_receive_tab()

        self.communication = Communication(port=5000)  # Ajuste a porta conforme necessário
        threading.Thread(target=self.start_server).start()

    def setup_send_tab(self):
        self.setup_send_widgets()
        self.setup_send_plot_frame()

    def setup_receive_tab(self):
        self.setup_receive_widgets()
        self.setup_receive_plot_frame()

    def setup_send_widgets(self):
        self.send_message_label = ttk.Label(self.send_tab, text="Mensagem a ser enviada:")
        self.send_message_label.grid(row=0, column=0, pady=5)

        self.send_message_entry = ttk.Entry(self.send_tab)
        self.send_message_entry.grid(row=0, column=1, pady=5)

        self.destination_ip_label = ttk.Label(self.send_tab, text="IP de Destino:")
        self.destination_ip_label.grid(row=1, column=0, pady=5)

        self.destination_ip_entry = ttk.Entry(self.send_tab)
        self.destination_ip_entry.grid(row=1, column=1, pady=5)
        self.destination_ip_entry.insert(0, self.default_destination_ip)

        self.destination_port_label = ttk.Label(self.send_tab, text="Porta de Destino:")
        self.destination_port_label.grid(row=2, column=0, pady=5)

        self.destination_port_entry = ttk.Entry(self.send_tab)
        self.destination_port_entry.grid(row=2, column=1, pady=5)
        self.destination_port_entry.insert(0, str(self.default_destination_port))

        self.send_button = ttk.Button(self.send_tab, text="Enviar Mensagem", command=self.send_message)
        self.send_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.binary_label = ttk.Label(self.send_tab, text="Mensagem em Binário:")
        self.binary_label.grid(row=1, column=2, pady=5)

        self.binary_entry = ttk.Entry(self.send_tab, state="readonly")
        self.binary_entry.grid(row=1, column=3, pady=5)

        self.encrypted_label = ttk.Label(self.send_tab, text="Mensagem Criptografada:")
        self.encrypted_label.grid(row=3, column=2, pady=5)

        self.encrypted_entry = ttk.Entry(self.send_tab, state="readonly")
        self.encrypted_entry.grid(row=3, column=3, pady=5)

        self.mlt_label = ttk.Label(self.send_tab, text="Forma de Onda após MLT:")
        self.mlt_label.grid(row=2, column=2, pady=5)

        self.mlt_entry = ttk.Entry(self.send_tab, state="readonly")
        self.mlt_entry.grid(row=2, column=3, pady=5)

    def setup_receive_widgets(self):
        self.received_message_label = ttk.Label(self.receive_tab, text="Mensagem Recebida:")
        self.received_message_label.grid(row=0, column=0, pady=5)

        self.received_message_entry = ttk.Entry(self.receive_tab, state="readonly")
        self.received_message_entry.grid(row=0, column=1, pady=5)

        self.binary_label_receive = ttk.Label(self.receive_tab, text="Mensagem em Binário:")
        self.binary_label_receive.grid(row=0, column=2, pady=5)

        self.binary_entry_receive = ttk.Entry(self.receive_tab, state="readonly")
        self.binary_entry_receive.grid(row=0, column=3, pady=5)

        self.encrypted_label_receive = ttk.Label(self.receive_tab, text="Mensagem Criptografada:")
        self.encrypted_label_receive.grid(row=1, column=2, pady=5)

        self.encrypted_entry_receive = ttk.Entry(self.receive_tab, state="readonly")
        self.encrypted_entry_receive.grid(row=1, column=3, pady=5)

        self.mlt_label_receive = ttk.Label(self.receive_tab, text="Forma de Onda após MLT:")
        self.mlt_label_receive.grid(row=2, column=2, pady=5)

        self.mlt_entry_receive = ttk.Entry(self.receive_tab, state="readonly")
        self.mlt_entry_receive.grid(row=2, column=3, pady=5)

    def setup_send_plot_frame(self):
        self.plot_frame_send = ttk.Frame(self.send_tab)
        self.plot_frame_send.grid(row=4, column=0, columnspan=4)

    def setup_receive_plot_frame(self):
        self.plot_frame_receive = ttk.Frame(self.receive_tab)
        self.plot_frame_receive.grid(row=3, column=0, columnspan=4)

    def start_server(self):
        while True:
            received_message = self.communication.receive_message()
            if received_message:
                decoded_message = self.decode_message(received_message)
                self.update_receive_tab(decoded_message)

    def generate_key(self):
        return Fernet.generate_key()

    def encrypt_message(self, message, key):
        cipher = Fernet(key)
        encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message, key):
        cipher = Fernet(key)
        decrypted_message = cipher.decrypt(encrypted_message).decode()
        return decrypted_message

    def encode_message(self, message):
        mlt_algorithm = MLTAlgorithm()
        binary_message = ' '.join(format(ord(char), '08b') for char in message)
        mlt_transform = mlt_algorithm.apply_mlt(binary_message)
        encrypted_message = self.encrypt_message(' '.join(map(str, mlt_transform[1:])), self.key)  # Iniciar a partir do segundo valor
        return encrypted_message, binary_message, mlt_transform

    def decode_message(self, encrypted_message):
        mlt_algorithm = MLTAlgorithm()
        decrypted_message = self.decrypt_message(encrypted_message[1], self.key)
        binary_message = ' '.join(format(ord(char), '08b') for char in decrypted_message)
        mlt_transform = mlt_algorithm.apply_mlt(binary_message)
        return decrypted_message, binary_message, mlt_transform

    def send_message(self):
        message = self.send_message_entry.get()
        destination_ip = self.destination_ip_entry.get() or self.default_destination_ip
        destination_port = int(self.destination_port_entry.get() or self.default_destination_port)

        self.key = self.generate_key()  # Gerar uma chave para cada mensagem

        _, encrypted_message, mlt_transform = self.encode_message(message)

        # Exibir informações no transmissor
        binary_message = ' '.join(format(ord(char), '08b') for char in message)
        self.binary_entry.config(state="normal")
        self.binary_entry.delete(0, tk.END)
        self.binary_entry.insert(0, binary_message)
        self.binary_entry.config(state="readonly")

        self.encrypted_entry.config(state="normal")
        self.encrypted_entry.delete(0, tk.END)
        self.encrypted_entry.insert(0, " ".join(map(str, encrypted_message)))
        self.encrypted_entry.config(state="readonly")

        mlt_algorithm = MLTAlgorithm()
        self.mlt_entry.config(state="normal")
        self.mlt_entry.delete(0, tk.END)
        self.mlt_entry.insert(0, " ".join(map(str, mlt_transform[1:])))  # Iniciar a partir do segundo valor
        self.mlt_entry.config(state="readonly")

        self.plot_mlt_transform(mlt_transform, self.plot_frame_send)

        # Ajuste a porta para a comunicação
        destination = (destination_ip, destination_port)

        success = self.communication.send_message(destination, (self.key, encrypted_message))

    def update_receive_tab(self, message):
        self.received_message_entry.config(state="normal")
        self.received_message_entry.delete(0, tk.END)
        self.received_message_entry.insert(0, " ".join(map(str, message[0])))
        self.received_message_entry.config(state="readonly")

        binary_message = ' '.join(format(ord(char), '08b') for char in message[0])
        self.binary_entry_receive.config(state="normal")
        self.binary_entry_receive.delete(0, tk.END)
        self.binary_entry_receive.insert(0, binary_message)
        self.binary_entry_receive.config(state="readonly")

        mlt_algorithm = MLTAlgorithm()
        self.mlt_entry_receive.config(state="normal")
        self.mlt_entry_receive.delete(0, tk.END)
        self.mlt_entry_receive.insert(0, " ".join(map(str, message[2][1:])))  # Iniciar a partir do segundo valor
        self.mlt_entry_receive.config(state="readonly")

        self.plot_mlt_transform(message[2], self.plot_frame_receive)

    def plot_mlt_transform(self, mlt_transform, frame):
        fig, ax = plt.subplots()
        ax.plot(mlt_transform)
        ax.set_title("Forma de Onda após MLT")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0)

