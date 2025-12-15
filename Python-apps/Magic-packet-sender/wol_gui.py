import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading

def wake_on_lan(mac_address, broadcast_ip="255.255.255.255", port=9):
    """Send a Wake-on-LAN magic packet to wake up a PC."""
    try:
        # Clean MAC address format
        mac_address = mac_address.replace(":", "").replace("-", "").lower()
        if len(mac_address) != 12:
            raise ValueError("Invalid MAC address format.")

        # Create the magic packet
        magic_packet = bytes.fromhex("FF" * 6 + mac_address * 16)

        # Send the packet over UDP broadcast
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, (broadcast_ip, port))

        return True, f"Magic packet sent to {mac_address.upper()}"
    except Exception as e:
        return False, f"Error: {str(e)}"

class WakeOnLANApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wake-on-LAN")
        self.root.geometry("320x180")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Wake-on-LAN", 
                                font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 15))
        
        # MAC Address input
        mac_frame = ttk.Frame(main_frame)
        mac_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(mac_frame, text="MAC Address:").pack(anchor=tk.W)
        self.mac_entry = ttk.Entry(mac_frame, width=30)
        self.mac_entry.pack(fill=tk.X, pady=(5, 0))
        self.mac_entry.insert(0, "")
        
        # Wake button
        self.wake_button = tk.Button(
            main_frame, 
            text="🔑 WAKE PC",
            command=self.send_magic_packet,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            activebackground="#45a049",
            activeforeground="white"
        )
        self.wake_button.pack(fill=tk.X, ipady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", 
                                      font=("Arial", 9))
        self.status_label.pack(pady=(10, 0))
        
    def send_magic_packet(self):
        """Send the magic packet in a separate thread."""
        mac = self.mac_entry.get().strip()
        
        if not mac:
            messagebox.showwarning("Input Error", "Please enter a MAC address.")
            return
        
        # Disable button during send
        self.wake_button.config(state=tk.DISABLED)
        self.status_label.config(text="Sending...", foreground="blue")
        
        # Run in thread to prevent GUI freeze
        thread = threading.Thread(target=self._send_packet, args=(mac,))
        thread.daemon = True
        thread.start()
    
    def _send_packet(self, mac):
        """Actually send the packet."""
        success, message = wake_on_lan(mac)
        
        # Update UI from thread
        self.root.after(0, self._update_status, success, message)
    
    def _update_status(self, success, message):
        """Update the status label and re-enable button."""
        if success:
            self.status_label.config(text="✅ Packet sent!", foreground="green")
        else:
            self.status_label.config(text=f"❌ {message}", foreground="red")
        
        self.wake_button.config(state=tk.NORMAL)
        
        # Clear status after 3 seconds
        self.root.after(3000, lambda: self.status_label.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = WakeOnLANApp(root)
    root.mainloop()
