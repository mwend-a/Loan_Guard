from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import csv
#import loan_guard
#from loan_guard import check_loan_status, x_test, y_pred


app = Flask (__name__, static_url_path='/static')


# Load model

with open('classifier.pkl', 'rb') as f:
        classifier = pickle.load(f)
    

# Defining attributes
df = pd.read_csv('loan_app_dataset.csv')
new_user_df = pd.read_csv('loan_csv.csv')


# Define a function to check loan status
def check_loan_status(df, x_test, y_pred, user_loan_id):
    results_df = pd.DataFrame({
        'loan_id': df.loc[x_test.index, 'loan_id'],
        'Predicted_Loan_Status': ['Approved' if pred == 1 else 'Rejected' for pred in y_pred]
    })

    if user_loan_id in results_df['loan_id'].astype(str).values:
        user_row = results_df[results_df['loan_id'].astype(str) == user_loan_id]
        user_prediction = user_row['Predicted_Loan_Status'].iloc[0]
        return f"Predicted Loan Status for Loan ID {user_loan_id}: {user_prediction}"
    else:
        return f"Loan with ID {user_loan_id} not found in the results DataFrame."


@app.route('/pred', methods=['GET','POST'])
def pred():
     loan_status= ''
     if request.method == 'POST':
        loan_id = request.form['loan_id']
        print(f"Received loan_id: {loan_id}")

        loan_row = new_user_df[new_user_df['loan_id'] == int(loan_id)]
        if loan_row.empty:
            loan_status = 'Loan ID not found'
        else:
            loan_status = loan_row['loan_status'].iloc[0]
            loan_status_mapping = {1: 'Approved', 0: 'Rejected'}
            loan_status = loan_status_mapping.get(loan_status, 'Unknown')
            print(f"Received loan_status: {loan_status}")
   
        # Handle GET request (if needed)
     return render_template('pred.html', result=f"The Loan ID was:{loan_status}")
  
      #if request.method == 'POST':
        # Get user Inputs
        #user_loan_id = request.form['loan_id'].strip()
        #x_test = pd.DataFrame(df)
        #y_pred = classifier.predict(x_test)
        #result = check_loan_status(df,df, y_pred, user_loan_id)
        #return render_template('pred.html', result=result)
      #else:
        # Handle GET request (e.g., render a form)
        #return render_template('pred.html')
    
@app.route('/')
def login():
    return render_template('login.html')


#loan_dataset = pd.DataFrame(columns=['loan_id', 'no_of_dependents', 'education', 'self_employed',
                                     # 'income_annum', 'loan_amount', 'loan_term', 'credit_score',
                                     # 'residential_assets_value', 'commercial_assets_value',
                                      #'luxury_assets_value', 'bank_asset_value', 'loan_status'])


@app.route('/home', methods =['POST', 'GET'])
def home():
    global loan_csv

    if request.method == 'POST':
        new_data= {
            'loan_id': request.form.get('loan_id'),
            'no_of_dependents': request.form.get('no_of_dependents'),
            'education': request.form.get('education'),
            'self_employed': request.form.get('self_employed'),
            'income_annum': request.form.get('income_annum'),
            'loan_amount': request.form.get('loan_amount'),
            'loan_term': request.form.get('loan_term'),
            'credit_score': request.form.get('credit_score'),
            'residential_assets_value': request.form.get('residential_assets_value'),
            'commercial_assets_value': request.form.get('commercial_assets_value'),
            'luxury_assets_value': request.form.get('luxury_assets_value'),
            'bank_asset_value': request.form.get('bank_asset_value'),
            'loan_status': request.form.get('loan_status'),
            
        }

        with open('loan_csv.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=new_data.keys())
            if file.tell()==0:
                writer.writeheader()
            writer.writerow(new_data)
        #return render_template('home.html')
        return 'Data Submited'
    else:
        return render_template('home.html')
        

         
    return render_template('home.html')


if __name__=='__main__':
    app.run(debug=True)