import sqlite3

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

    cursor.execute("SELECT coinvalue FROM user WHERE username=?", (receiver_un,))
    receiver_coinvalue = cursor.fetchone()[0]
    # Calculate the addition to the receiver's wallet
    addition = (txn_amount / coin_value) * receiver_coinvalue

    # Update receiver's balance (add the calculated amount)
    cursor.execute("UPDATE user SET wallet=wallet+? WHERE username=?", (addition, receiver_un))
    print("Updated recievers wallet by:")
    # Commit the changes
    conn.commit()
    # except Exception as e:
    #     print("Validation exception")
    #     conn.rollback()
    #     raise e
    # finally:
        # Close the database connection
    conn.close()