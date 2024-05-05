from flask import Flask, render_template, request, redirect, url_for

import sqlite3
conn = sqlite3.connect('complaints.db')
cursor = conn.cursor()
cursor.execute("select * from complaints")
data=cursor.fetchall()
print(data)

complaints_list = []
for i in data:
    for j in i:
        dbdict={'id':j[0],'phone_number':j[5],'description':j[4],'status':j[3]}
        complaints_list.append(dbdict)


app = Flask(__name__)

# Sample data (replace with actual data)
total_complaints = 10
pending_complaints = 5
processed_complaints = 5
# recent_complaints = [
#     {'id': 1, 'complainee': 'dummy user', 'registered_on': '16/04/2024', 'status': 'Success'},
#     {'id': 2, 'complainee': 'dummy user', 'registered_on': '16/04/2024', 'status': 'Pending'},
#     {'id': 3, 'complainee': 'dummy user', 'registered_on': '16/04/2024', 'status': 'Success'},
#     {'id': 4, 'complainee': 'dummy user', 'registered_on': '16/04/2024', 'status': 'Success'},
#     {'id': 5, 'complainee': 'dummy user', 'registered_on': '16/04/2024', 'status': 'Pending'}
# ]



# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        dept_id = request.form.get('dept_id')
        password = request.form.get('password')
        # Validate department ID and password (replace with your validation logic)
        if validate_login(dept_id, password):
            # Redirect to dashboard upon successful login
            return redirect(url_for('dashboard', dept_id=dept_id))
        else:
            # Display error message for invalid login
            error_message = 'Invalid department ID or password. Please try again.'
    # Render login template with error message
    return render_template('login.html', error_message=error_message)

def validate_login(dept_id, password):
    # Replace this with your actual validation logic (e.g., querying a database)
    if password == dept_id + '@123':
        return True
    else:
        return False


# Route for dashboard
@app.route('/dashboard')
def dashboard():
    dept_id = request.args.get('dept_id', default='', type=str)
   
    # Add logic to fetch and display dashboard data here
    return render_template('dashboard.html', dept_id=dept_id,total_complaints=total_complaints, pending_complaints=pending_complaints, processed_complaints=processed_complaints, recent_complaints=complaints_list)




@app.route('/complaint')
def complaint():
    return render_template('complaint.html', complaints=complaints_list)

@app.route('/update_status', methods=['POST'])
def update_status():
    complaint_id = request.form.get('complaint_id')
    new_status = 'Closed'  # Assume status change from Pending to Closed

    # Update status in database (replace this with actual database update logic)
    for complaint in complaints_list:
        if complaint['id'] == int(complaint_id):
            complaint['status'] = new_status
            return redirect(url_for('complaint'))

if __name__ == '__main__':
    app.run(debug=True)
