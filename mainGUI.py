import tkinter as tk
import my_math_fx as my_math
from node import RSAKeyGenerator 


def format_encryp_message(encrypted_list: list[int]) -> str:
    if not encrypted_list:
        return ""  # Handle empty list

    max_length = max(len(str(num)) for num in encrypted_list)  # Find the length of the largest integer

    formatted_message = ""
    for num in encrypted_list:
        num_str = str(num)
        padded_num = num_str.zfill(max_length)  # Pad with leading zeros
        formatted_message += padded_num

    return formatted_message

def validate_values():
    try:
        p_value = int(entry_p.get())
        q_value = int(entry_q.get())
        e_value = int(entry_e.get())
        p2_value = int(entry_p2.get())
        q2_value = int(entry_q2.get())
        e2_value = int(entry_e2.get())

        # Check that p and p2 are prime
        if not my_math.check_prime(p_value):     
            label_output.config(text="p must be prime")
            return
        if not my_math.check_prime(p2_value):     
            label_output.config(text="p2 must be prime")
            return
        
        # Check that q and q2 are prime
        if not my_math.check_prime(q_value):  
            label_output.config(text="q must be prime")
            return
        if not my_math.check_prime(q2_value):  
            label_output.config(text="q2 must be prime")
            return
        
        # Check that e and e2 are coprime to their respective Euler totients
        the_euler1 = (p_value - 1) * (q_value - 1)
        the_euler2 = (p2_value - 1) * (q2_value - 1)
        
        if not my_math.are_coprime(e_value, the_euler1):
            label_output.config(text=f"e must be coprime to {the_euler1}")
            return
        if not my_math.are_coprime(e2_value, the_euler2):
            label_output.config(text=f"e2 must be coprime to {the_euler2}")
            return
        computer_one = RSAKeyGenerator(p_value, q_value, e_value)
        computer_two = RSAKeyGenerator(p2_value, q2_value, q2_value)
        # Open success window if all values are valid
        the_message = open_message_window() 
        showCalculation(the_message, computer_one, computer_two)

    except ValueError:
        label_output.config(text="Please enter valid integers for P, Q, and E.")

def open_message_window() -> str:
    """Opens a window and prompts the user for a message, returns the message as a string."""
    window = tk.Toplevel(root)
    window.title("Enter your message")
    window.geometry("250x150")

    tk.Label(window, text="Enter your message:").grid(row=0, column=0, padx=10, pady=5)
    entry_message = tk.Entry(window, width=20)
    entry_message.grid(row=1, column=0, padx=10, pady=5)

    message_var = tk.StringVar()  # Variable to store user input

    def on_submit():
        message_var.set(entry_message.get())  # Store input in the variable
        window.destroy()  # Close the window

    submit_button = tk.Button(window, text="Submit", command=on_submit)
    submit_button.grid(row=2, column=0, padx=10, pady=5)

    window.wait_window()  # Pause execution until the window is closed
    return message_var.get()  # Return the user input after the window closes



def showCalculation(message: str, computer_one: RSAKeyGenerator, computer_two: RSAKeyGenerator):
    """Shows the process of signing -> encrypting -> decrypting."""
    window = tk.Toplevel(root)
    window.title("Encryption Process")

    # Configure window resizing
    window.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    window.grid_columnconfigure(0, weight=1) # Allow column 0 to expand

    # Create a text widget to display information (initially disabled)
    text_area = tk.Text(window, height=15, width=70, wrap="word", state=tk.DISABLED)
    text_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") #make sticky

    def log(text):
        """Appends text to the text area."""
        text_area.config(state=tk.NORMAL)  # Enable text area to insert text
        text_area.insert(tk.END, text + "\n")
        text_area.config(state=tk.DISABLED)  # Disable text area again
        text_area.see(tk.END)  # Auto-scroll

    # Encrypting message
    log(f"Encrypting message with Computer Two's public keys: {message}")
    
    encrypted_message = computer_one.encrypt(message, computer_two)
    formated_en_message = format_encryp_message(encrypted_message)
    log(f"Encrypted message: {formated_en_message}")

    # Signing the message
    log(f"Computer One is signing: {message}")
    signature = computer_one.sign(message)

    # Receiving message
    log("Computer Two has received the encrypted message.")

    # Verifying signature
    verify = computer_two.verify(computer_one, str(message), signature )

    log(f"Computer Two is verifying the signature using Computer One's public keys: ({computer_one.n}, {computer_one.e})\n Verify status: {verify}")

    # Decrypting message
    decrypted_message = computer_two.decrypt(encrypted_message)
    log(f"Computer Two is decrypting using it's private key: {formated_en_message} -> {decrypted_message}")

    # Additional details about computers
    log(f"Computer One: {computer_one}\nComputer Two: {computer_two}")




# Create main window
root = tk.Tk()
root.resizable(False, False) #makes not able to be resized


root.title("P, Q, and E Input")
root.geometry("350x400")

# Labels and entry fields for P, Q, E
bold_font = ("Arial", 12, "bold")  # Font family, size, and style (bold)
tk.Label(root, text="Computer One", font=bold_font).grid(row=0, column=0, columnspan=2, pady=5, sticky='W')



tk.Label(root, text="Enter P:").grid(row=1, column=0, padx=10, pady=5)
entry_p = tk.Entry(root, width=20)
entry_p.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Enter Q:").grid(row=2, column=0, padx=10, pady=5)
entry_q = tk.Entry(root, width=20)
entry_q.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Enter E:").grid(row=3, column=0, padx=10, pady=5)
entry_e = tk.Entry(root, width=20)
entry_e.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Computer Two", font = bold_font).grid(row=4, column=0, columnspan=2, pady=5, sticky='W')
tk.Label(root, text="Enter P2:").grid(row=5, column=0, padx=10, pady=5)
entry_p2 = tk.Entry(root, width=20)
entry_p2.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Enter Q2:").grid(row=6, column=0, padx=10, pady=5)
entry_q2 = tk.Entry(root, width=20)
entry_q2.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Enter E2:").grid(row=7, column=0, padx=10, pady=5)
entry_e2 = tk.Entry(root, width=20)
entry_e2.grid(row=7, column=1, padx=10, pady=5)

# Submit button with validation
button = tk.Button(root, text="Submit", command=validate_values)
button.grid(row=8, column=0, columnspan=2, pady=10)

# Label to display results or errors
label_output = tk.Label(root, text="", font=("Arial", 12))
label_output.grid(row=9, column=0, columnspan=2, pady=10)




# Run the GUI
root.mainloop()


