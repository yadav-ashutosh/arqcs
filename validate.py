import sqlite3
from publish import publish_channel
def validate_txn(username, receiver_un , txn_amount):
    # Connect to the database
    conn = sqlite3.connect("arqdb.db")
    cursor = conn.cursor()
    # Check the sender's balance
    cursor.execute("SELECT wallet,coinvalue FROM user WHERE username=?", (username,))
    result = cursor.fetchone()
    wallet_balance = 0 
    coin_value = 1 

    if result:
        wallet_balance = result[0]  # Access the first column (wallet balance)
        coin_value = result[1]     # Access the second column (coin value)
        print("Wallet Balance:", wallet_balance)
        print("Coin Value:", coin_value)

    if wallet_balance < txn_amount:
        raise ValueError("Insufficient balance to perform the transaction")

    # Deduct the transaction amount from the sender's balance
    new_sender_balance = wallet_balance - txn_amount
    # Update the sender's balance in the database
    try:
        cursor.execute("UPDATE user SET wallet=? WHERE username=?", (new_sender_balance, username))
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        conn.rollback()  # Rollback changes if an error occurs
    print("Updated sender wallet" )
    # Record the transaction in the transactions table
    #cursor.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)", (username, receiver_un, txn_amount))
    print("transactions updated")

    cursor.execute("SELECT wallet,coinvalue FROM user WHERE username=?", (receiver_un,))
    result = cursor.fetchone()
    receiver_coinvalue = result[0]
    receiver_wallet = result[1]
    # Calculate the addition to the receiver's wallet
    addition = (txn_amount / coin_value) * receiver_coinvalue
    print("added")
    # Update receiver's balance (add the calculated amount)
    cursor.execute("UPDATE user SET wallet=wallet+? WHERE username=?", (addition, receiver_un))
    print("Updated rc wallet")
    publish_channel(username=username,wallet_balance=wallet_balance, last_transaction="-"+str(txn_amount), n=3)
    publish_channel(username=receiver_un,wallet_balance=receiver_wallet, last_transaction="+"+str(txn_amount),n=3)
    
    print("Updated and published recievers wallet by:")
    # Commit the changes
    conn.commit()
    conn.close()