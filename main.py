import streamlit as st
from pathlib import Path
import random
import string
import json

class Bank:

    database = 'database.json'
    data = []

    # Load previous data
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("Database not found.")
    except Exception:
        pass

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        mix = alpha + digits
        random.shuffle(mix)
        return ''.join(mix)

    # ---------- Create Account ----------
    def createaccount(self, name, email, phone, pin):
        d = {
            'name': name,
            'email_id': email,
            'phone_no': phone,
            'pin': pin,
            'account_no': Bank.__accountno(),
            'balance': 0
        }

        if len(str(phone)) != 10:
            return "❌ Phone number must be 10 digits!"

        if len(str(pin)) != 4:
            return "❌ PIN must be 4 digits!"

        Bank.data.append(d)
        Bank.__update()
        return f"✅ Account Created Successfully!\nAccount No: {d['account_no']}"

    # ---------- Deposit Money ----------
    def deposit(self, accNo, pin, amount):
        user = [i for i in Bank.data if i['account_no'] == accNo and i['pin'] == pin]

        if not user:
            return "❌ Account not found!"

        if amount <= 0:
            return "❌ Invalid deposit amount."

        user[0]['balance'] += amount
        Bank.__update()

        return "💰 Amount Deposited Successfully!"

    # ---------- Withdraw Money ----------
    def withdraw(self, accNo, pin, amount):
        user = [i for i in Bank.data if i['account_no'] == accNo and i['pin'] == pin]

        if not user:
            return "❌ Account not found!"

        if amount <= 0:
            return "❌ Invalid withdrawal amount."

        if amount > user[0]['balance']:
            return "❌ Insufficient Balance!"

        user[0]['balance'] -= amount
        Bank.__update()
        return "🏧 Withdrawal Successful!"

    # ---------- Show Details ----------
    def details(self, accNo, pin):
        user = [i for i in Bank.data if i['account_no'] == accNo and i['pin'] == pin]

        if not user:
            return None

        return user[0]

    # ---------- Update Data ----------
    def update_data(self, accNo, pin, name, email, phone, new_pin):
        user = [i for i in Bank.data if i['account_no'] == accNo and i['pin'] == pin]

        if not user:
            return "❌ Account not found!"

        if phone and len(str(phone)) != 10:
            return "❌ Phone must be 10 digits!"

        if new_pin and len(str(new_pin)) != 4:
            return "❌ PIN must be 4 digits!"

        if name:
            user[0]['name'] = name
        if email:
            user[0]['email_id'] = email
        if phone:
            user[0]['phone_no'] = int(phone)
        if new_pin:
            user[0]['pin'] = int(new_pin)

        Bank.__update()
        return "✏️ Details Updated Successfully!"

    # ---------- Delete Account ----------
    def delete_account(self, accNo, pin):
        user = [i for i in Bank.data if i['account_no'] == accNo and i['pin'] == pin]

        if not user:
            return "❌ Account not found!"

        Bank.data = [i for i in Bank.data if not (i['account_no'] == accNo and i['pin'] == pin)]
        Bank.__update()

        return "🗑 Account Deleted Successfully!"


# ================== STREAMLIT UI ==================

st.title("🏦 Bank Management System")

bank = Bank()

menu = st.sidebar.radio(
    "Choose Option",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Account Details",
        "Update Account",
        "Delete Account"
    ]
)

# ---------- CREATE ACCOUNT ----------
if menu == "Create Account":
    st.header("🆕 Create New Account")

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone Number (10 digits)")
    pin = st.text_input("Enter a 4-digit PIN")

    if st.button("Create Account"):
        if name and email and phone and pin:
            result = bank.createaccount(name, email, int(phone), int(pin))
            st.success(result)
        else:
            st.error("All fields are required!")

# ---------- DEPOSIT MONEY ----------
elif menu == "Deposit Money":
    st.header("💰 Deposit Money")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN")
    amount = st.number_input("Enter Amount", min_value=1)

    if st.button("Deposit"):
        result = bank.deposit(acc, int(pin), amount)
        st.info(result)

# ---------- WITHDRAW MONEY ----------
elif menu == "Withdraw Money":
    st.header("🏧 Withdraw Money")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN")
    amount = st.number_input("Enter Amount", min_value=1)

    if st.button("Withdraw"):
        result = bank.withdraw(acc, int(pin), amount)
        st.info(result)

# ---------- SHOW DETAILS ----------
elif menu == "Show Account Details":
    st.header("📄 Account Details")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN")

    if st.button("Show"):
        details = bank.details(acc, int(pin))
        if details:
            st.json(details)
        else:
            st.error("❌ Account not found!")

# ---------- UPDATE ACCOUNT ----------
elif menu == "Update Account":
    st.header("✏️ Update Account Details")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter Old PIN")

    name = st.text_input("New Name (Optional)")
    email = st.text_input("New Email (Optional)")
    phone = st.text_input("New Phone Number (Optional)")
    new_pin = st.text_input("New PIN (Optional)")

    if st.button("Update"):
        result = bank.update_data(acc, int(pin), name, email, phone, new_pin)
        st.info(result)

# ---------- DELETE ACCOUNT ----------
elif menu == "Delete Account":
    st.header("🗑 Delete Account")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN")

    if st.button("Delete"):
        result = bank.delete_account(acc, int(pin))
        st.warning(result)
