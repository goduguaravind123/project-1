import hashlib
import json
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext


# Block class definition
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


# Blockchain class definition
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), {"info": "Genesis Block"}, "0")
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_latest_block()
        new_block = Block(prev_block.index + 1, time.time(), data, prev_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def trace_drug(self, drug_id):
        trace = []
        for block in self.chain:
            data = block.data
            if isinstance(data, dict) and data.get("drug_id") == drug_id:
                trace.append(data)
        return trace

    def get_chain_data(self):
        return [block.__dict__ for block in self.chain]


# GUI Application
class BlockchainApp:
    def __init__(self, root):
        self.blockchain = Blockchain()
        self.root = root
        self.root.title("Drug Tracing Blockchain System")
        self.root.geometry("600x600")

        tk.Label(root, text="Drug Tracing in Supply Chain", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(root, text="➕ Add Drug Stage", command=self.add_drug_stage, width=25).pack(pady=5)
        tk.Button(root, text="🔍 Trace Drug by ID", command=self.trace_drug, width=25).pack(pady=5)
        tk.Button(root, text="🔗 View Full Blockchain", command=self.view_blockchain, width=25).pack(pady=5)
        tk.Button(root, text="✅ Validate Blockchain", command=self.validate_chain, width=25).pack(pady=5)

        self.output = scrolledtext.ScrolledText(root, height=20, width=70, wrap=tk.WORD)
        self.output.pack(pady=10)

    def add_drug_stage(self):
        drug_id = simpledialog.askstring("Drug ID", "Enter Drug ID:")
        stage = simpledialog.askstring("Stage", "Enter Stage (Manufactured / Shipped / Sold etc.):")
        entity = simpledialog.askstring("Entity", "Enter Entity Name:")
        location = simpledialog.askstring("Location", "Enter Location:")
        extra = simpledialog.askstring("Additional Info", "Enter Any Additional Info (optional):")

        if not drug_id or not stage or not entity or not location:
            messagebox.showwarning("Incomplete", "Please fill all required fields.")
            return

        data = {
            "drug_id": drug_id,
            "stage": stage,
            "entity": entity,
            "location": location,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        }

        if extra:
            data["extra_info"] = extra

        self.blockchain.add_block(data)
        messagebox.showinfo("Success", "Stage added to blockchain.")
        self.output.insert(tk.END, f"✅ Added stage: {stage} for drug {drug_id}\n\n")

    def trace_drug(self):
        drug_id = simpledialog.askstring("Trace Drug", "Enter Drug ID to trace:")
        if not drug_id:
            return

        trace = self.blockchain.trace_drug(drug_id)
        self.output.delete(1.0, tk.END)
        if trace:
            self.output.insert(tk.END, f"📦 Tracing Drug ID: {drug_id}\n\n")
            for data in trace:
                self.output.insert(tk.END, json.dumps(data, indent=4) + "\n\n")
        else:
            self.output.insert(tk.END, f"❌ No record found for Drug ID: {drug_id}\n")

    def view_blockchain(self):
        self.output.delete(1.0, tk.END)
        chain = self.blockchain.get_chain_data()
        for block in chain:
            self.output.insert(tk.END, json.dumps(block, indent=4) + "\n\n")

    def validate_chain(self):
        valid = self.blockchain.is_chain_valid()
        self.output.insert(tk.END, f"✅ Blockchain is valid.\n\n" if valid else "❌ Blockchain is invalid!\n\n")


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()
