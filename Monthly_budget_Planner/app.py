#Monthly Budget Planner:

# streamlit: Web app banane ke liye.

# datetime: (Abhi use nahi hua, future ke liye reserved).

# json: Data ko file me save karne ke liye.

# os: File check karne ke liye.

# random: Random tip dikhane ke liye.
import streamlit as st
from datetime import datetime
import json
import os
import random

# 🎯 Tips
tips = [
    "💡 'Don't save what is left after spending; spend what is left after saving.' – Warren Buffett",
    "📈 'A budget is telling your money where to go instead of wondering where it went.'",
    "🧠 'Beware of little expenses; a small leak will sink a great ship.' – Benjamin Franklin",
    "💸 'Track every rupee; every rupee counts.'",
    "📊 'Budgeting isn't about limiting yourself – it's about making the things that excite you possible.'"
]

# 🧠 Models
class BudgetItem:
    def __init__(self, description, amount, is_income):
        self.description = description
        self.amount = amount
        self.is_income = is_income

    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "is_income": self.is_income
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['description'], data['amount'], data['is_income'])

class BudgetPlanner:
    def __init__(self):
        self.items = []
        self.file_path = 'budget_data.json'
        self.load()

    def add_item(self, description, amount, is_income):
        self.items.append(BudgetItem(description, amount, is_income))
        self.save()

    def delete_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.save()

    def clear_all(self):
        self.items = []
        self.save()

    def total_income(self):
        return sum(item.amount for item in self.items if item.is_income)

    def total_expense(self):
        return sum(item.amount for item in self.items if not item.is_income)

    def total_savings(self):
        return self.total_income() - self.total_expense()

    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump([item.to_dict() for item in self.items], f)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.items = [BudgetItem.from_dict(item) for item in data]

    def get_items(self):
        return self.items

# 🖼️ UI Code
st.set_page_config(page_title="Monthly Budget Planner", page_icon="💰")

planner = BudgetPlanner()
st.title("💰 Monthly Budget Planner")
st.markdown("Plan your income, expenses and savings smartly ✨")

menu = ["➕ Add Entry", "📊 View Summary", "📋 All Records"]
choice = st.sidebar.selectbox("Menu", menu)

# ➕ Add Entry
if choice == "➕ Add Entry":
    st.subheader("Add New Income or Expense")
    desc = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, step=0.5)
    entry_type = st.radio("Type", ["Income", "Expense"])
    if st.button("Add"):
        if desc and amount > 0:
            planner.add_item(desc, amount, entry_type == "Income")
            st.rerun()
        else:
            st.warning("Please enter valid description and amount.")

# 📊 View Summary
elif choice == "📊 View Summary":
    st.subheader("Monthly Summary")
    st.metric("Total Income", f"Rs. {planner.total_income():,.2f}")
    st.metric("Total Expense", f"Rs. {planner.total_expense():,.2f}")
    st.metric("💸 Savings", f"Rs. {planner.total_savings():,.2f}")
    st.info(random.choice(tips))

# 📋 All Records
elif choice == "📋 All Records":
    st.subheader("All Transactions")
    items = planner.get_items()

    if items:
        for i, item in enumerate(items):
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                label = "🟢 Income" if item.is_income else "🔴 Expense"
                st.write(f"**{label}** - {item.description}: Rs. {item.amount:.2f}")
            with col2:
                st.write("")
            with col3:
                if st.button("❌ Delete", key=f"del_{i}"):
                    planner.delete_item(i)
                    st.rerun()

        st.markdown("---")
        if st.button("🧹 Clear All Records"):
            planner.clear_all()
            st.rerun()
    else:
        st.info("No records found. Add income or expense from sidebar.")

