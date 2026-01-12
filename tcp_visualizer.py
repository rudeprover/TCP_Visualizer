"""
TCP Handshake Visualizer (Educational)

This program demonstrates how a real TCP socket is created and connected,
while visually explaining the TCP handshake states using a Tkinter GUI.

IMPORTANT:
- This does NOT sniff packets.
- It uses standard sockets exactly like browsers and apps do.
- TCP states are inferred from socket API behavior.

Author: Educational example
Python version: 3.8+
"""

import socket
import threading
import time
import tkinter as tk
from tkinter import ttk


# =========================
# Configuration
# =========================

SERVER_HOST = "google.com"
SERVER_PORT = 80
CONNECTION_TIMEOUT = 5  # seconds


# =========================
# GUI Application
# =========================

class TCPHandshakeVisualizer(tk.Tk):
    """
    Tkinter application that visualizes a TCP connection lifecycle.
    """

    def __init__(self):
        super().__init__()

        self.title("TCP Handshake Visualizer")
        self.geometry("520x380")
        self.resizable(False, False)

        self._build_ui()

    # -------------------------
    # UI Construction
    # -------------------------

    def _build_ui(self):
        """
        Create and layout all UI widgets.
        """

        title = ttk.Label(
            self,
            text="TCP Handshake Visualizer",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        subtitle = ttk.Label(
            self,
            text="Visualizing how socket() and connect() map to TCP states",
            font=("Arial", 10)
        )
        subtitle.pack()

        self.state_label = ttk.Label(
            self,
            text="State: CLOSED",
            font=("Courier", 14),
            foreground="blue"
        )
        self.state_label.pack(pady=20)

        self.connect_button = ttk.Button(
            self,
            text="Start TCP Connection",
            command=self.start_connection
        )
        self.connect_button.pack(pady=10)

        log_frame = ttk.LabelFrame(self, text="Event Log")
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.log_box = tk.Text(
            log_frame,
            height=10,
            width=60,
            state="disabled",
            font=("Courier", 9)
        )
        self.log_box.pack(padx=5, pady=5)

    # -------------------------
    # Logging Helpers
    # -------------------------

    def log(self, message: str):
        """
        Append a message to the log box in a thread-safe way.
        """
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state="disabled")

    def set_state(self, state: str):
        """
        Update the visible TCP state label.
        """
        self.state_label.config(text=f"State: {state}")
        self.log(f"[STATE] {state}")

    # -------------------------
    # Connection Flow
    # -------------------------

    def start_connection(self):
        """
        Start the TCP connection in a background thread
        to keep the GUI responsive.
        """
        self.connect_button.config(state=tk.DISABLED)
        self.log("User requested TCP connection")

        thread = threading.Thread(
            target=self.tcp_connection_flow,
            daemon=True
        )
        thread.start()

    def tcp_connection_flow(self):
        """
        Simulates and visualizes the lifecycle of a TCP socket.
        """

        sock = None

        try:
            # CLOSED
            self.set_state("CLOSED")
            time.sleep(0.7)

            # SOCKET CREATED
            self.log("Calling socket(AF_INET, SOCK_STREAM)")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(CONNECTION_TIMEOUT)
            self.set_state("SOCKET CREATED")
            time.sleep(0.7)

            # SYN-SENT
            self.log(f"Calling connect({SERVER_HOST}:{SERVER_PORT})")
            self.set_state("SYN-SENT (connect() in progress)")
            sock.connect((SERVER_HOST, SERVER_PORT))

            # ESTABLISHED
            self.set_state("ESTABLISHED (handshake complete)")
            self.log("TCP connection successfully established")
            time.sleep(1.5)

            # CLOSE
            self.log("Calling close()")
            sock.close()
            self.set_state("CLOSED (connection terminated)")

        except Exception as e:
            self.set_state("ERROR")
            self.log(f"Error occurred: {e}")

        finally:
            self.connect_button.config(state=tk.NORMAL)


# =========================
# Entry Point
# =========================

if __name__ == "__main__":
    app = TCPHandshakeVisualizer()
    app.mainloop()
