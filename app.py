from flask import Flask, render_template, request, redirect
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    category = request.form['category']
    amount = request.form['amount']

    with open('expenses.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount])
    
    return redirect('/')

@app.route('/view')
def view():
    expenses = []
    total = 0
    try:
        with open('expenses.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                expenses.append(row)
                total += float(row[2])
    except FileNotFoundError:
        pass
    return render_template('view.html', expenses=expenses, total=total)

@app.route('/summary')
def summary():
    categories = defaultdict(float)
    try:
        with open('expenses.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                categories[row[1]] += float(row[2])

        if categories:
            labels = list(categories.keys())
            values = list(categories.values())
            plt.figure(figsize=(6,6))
            plt.pie(values, labels=labels, autopct='%1.1f%%')
            plt.title('Expense Summary by Category')
            plt.savefig('static/summary.png')
            plt.close()
    except:
        pass

    return redirect('/summary_display')

@app.route('/summary_display')
def summary_display():
    return '''
    <h2>Category Summary</h2>
    <img src="/static/summary.png" width="400"><br><br>
    <a href="/">← Back to Home</a>
    '''

if __name__== '__main__':
    app.run(debug=True)