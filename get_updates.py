import sqlite3

def get_updates_of_user(username):
    # Connect to the SQLite database
    conn = sqlite3.connect('arqdb.db')
    cursor = conn.cursor()

    # Initialize an empty dictionary to store the results
    result = {}

    # Get user information (username and wallet)
    cursor.execute('SELECT username, wallet FROM user WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    
    if user_data is not None:
        username, wallet = user_data
        result['Username'] = username
        result['Wallet'] = wallet
    else:
        result['Error'] = f'User {username} not found.'

    # Close the database connection
    conn.close()

    return result

# Call the function with the desired username
user_info = get_updates_of_user('desired_username')
print(user_info)

