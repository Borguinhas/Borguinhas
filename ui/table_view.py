
import customtkinter
import tkinter as tk
from tkinter import ttk

class TableView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=("Item", "Quality", "City Buy", "City Sell", "Buy Price", "Sell Price", "Unit Profit", "ROI", "Trip Profit", "Silver/KG"), show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Define headings
        self.tree.heading("Item", text="Item")
        self.tree.heading("Quality", text="Quality")
        self.tree.heading("City Buy", text="City Buy")
        self.tree.heading("City Sell", text="City Sell")
        self.tree.heading("Buy Price", text="Buy Price")
        self.tree.heading("Sell Price", text="Sell Price")
        self.tree.heading("Unit Profit", text="Unit Profit")
        self.tree.heading("ROI", text="ROI")
        self.tree.heading("Trip Profit", text="Trip Profit")
        self.tree.heading("Silver/KG", text="Silver/KG")

        # Optional: Adjust column widths
        self.tree.column("Item", width=150)
        self.tree.column("Quality", width=70, anchor=tk.CENTER)
        self.tree.column("City Buy", width=100)
        self.tree.column("City Sell", width=100)
        self.tree.column("Buy Price", width=90, anchor=tk.E)
        self.tree.column("Sell Price", width=90, anchor=tk.E)
        self.tree.column("Unit Profit", width=90, anchor=tk.E)
        self.tree.column("ROI", width=70, anchor=tk.E)
        self.tree.column("Trip Profit", width=90, anchor=tk.E)
        self.tree.column("Silver/KG", width=90, anchor=tk.E)

        # Add a scrollbar
        scrollbar = customtkinter.CTkScrollbar(self, orientation="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def update_table(self, data):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new data
        for row in data:
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("1200x600")
    app.title("Table View Test")

    table_view = TableView(app)
    table_view.pack(fill="both", expand=True, padx=10, pady=10)

    # Sample data
    sample_data = [
        ("Broadsword", 1, "Thetford", "Black Market", 1000, 1200, 200, 0.20, 2000, 0.5),
        ("Plate Armor", 2, "Lymhurst", "Black Market", 1500, 1800, 300, 0.20, 3000, 0.75),
        ("Fire Staff", 3, "Fort Sterling", "Black Market", 2000, 2500, 500, 0.25, 5000, 1.0),
    ]
    table_view.update_table(sample_data)

    app.mainloop()
