from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

app = Flask(__name__)

# Define a function to calculate attendance
def calculate_attendance(df, roll_no):
    x = np.array(df.iloc[:, 2])
    y = np.array(df.iloc[:, 3:])
    if roll_no in x:
        b = np.where(x == roll_no)[0][0]
        pc = 0
        ac = 0
        for i in y[b]:
            if i == "Present":
                pc += 1
            elif i == "Absent":
                ac += 1
        return pc, ac
    else:
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            print("File uploaded:", request.files['file'])
            file = request.files['file']
            print("File contents:", file.read())
            file.seek(0)  # Reset the file pointer
            try:
                df = pd.read_csv(file)
                print("CSV data:", df.head())
            except pd.errors.EmptyDataError:
                print("Error: Empty CSV file")
                return 'Error: Empty CSV file'
            except pd.errors.ParserError:
                print("Error: Invalid CSV file format")
                return 'Error: Invalid CSV file format'
            
            roll_no = request.form['roll_no']
            print("Roll number:", roll_no)
            
            try:
                pc, ac = calculate_attendance(df, roll_no)
                print("Attendance:", pc, ac)
            except ValueError:
                print("Error: Invalid roll number")
                return 'Error: Invalid roll number'
            
            if pc is not None and ac is not None:
                fig, ax = plt.subplots(figsize=(5, 4))
                ax.pie([pc, ac], labels=['Present', 'Absent'], autopct='%0.2f%%')
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                
                # Save the plot to a bytes buffer
                img = BytesIO()
                fig.savefig(img, format='png')
                img.seek(0)
                
                # Send the image as a response
                return send_file(img, mimetype='image/png')
            else:
                return 'Invalid roll number'
        except Exception as e:
            print(f"Error: {e}")
            return 'Error occurred while processing request'
    else:
        return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)