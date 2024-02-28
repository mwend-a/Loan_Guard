from flask import Flask, render_template, request, jsonify
import pandas as pd 
import pickle
import numpy as np
# import loan_guard

model = pickle.load (open('../model.pkl', 'rb'))

# Mapping education levels 

education_mapping= {'option1':0, 'option2':1}
employment_mapping = {'option1':0, 'option2':1}


app = Flask (__name__)


@app.route('/')
def home():
    return render_template('pred.html')


@app.route('/predict', methods=["POST","GET"])
def predict():
    data1 = float(request.form['input1'])
    data2 = float(request.form['input2'])
    data3 = float(request.form['input3'])
    data4 = float(request.form['input4'])
    data5 = float(request.form['input5'])
    data6 = float(request.form['input6'])  
    data7 = float(request.form['input7'])
    data8 = float(request.form['input8'])
    data9 = float(request.form['input9'])  
    data10 = education_mapping[request.form['education']]
    data11 = employment_mapping[request.form['employment']]
    data12 = float(request.form['input12'])
    input_data = [[data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12]]
    prediction = model.predict(input_data)
    return render_template('results.html', prediction= prediction)

#df = pd.read_csv('../loan_app_dataset.csv')

@app.route('/add_data', methods = ['POST'])
def add_data():
        global df
        new_data={
        'loan_id':request.form['loan_id'],
        'no_of_dependents':request.form['no_of_dependents'],
        'education':request.form['education'],
        'self_employed':request.form['self_employed'],
        'income_annum':request.form['income_annum'],
        'loan_amount':request.form['loan_amount'],
        'loan_term':request.form['loan_term'],
        'credit_score':request.form['credit_score'],
        'residential_assets_value':request.form['residential_assets_value'],
        'commercial_assets_value':request.form['commercial_assets_value'],
        'luxury_assets_value':request.form['luxury_assets_value'],
        'bank_assets_value':request.form['bank_asset_value'],  
    }
        new_df = pd.DataFrame(new_data, index=[len(df)])
        
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv('data.csv', index = False)
        return 'Data added successfully'
        
results_df = pd.read_csv('../loan_app_dataset.csv')

@app.route('/pred', methods=['GET', 'POST'])
def predict_loan_status():
    print('prediction hit')

    if request.method == 'POST':
        user_loan_id = request.form['loan_id']
        print(user_row.columns)
        if user_loan_id in results_df['loan_id'].astype(str).values:
            user_row = results_df[results_df['loan_id'].astype(str) == user_loan_id]
            user_prediction = user_row['Predicted_Loan_Status'].iloc[0]
            return f"Predicted Loan Status for Loan ID {user_loan_id}: {user_prediction}"
        else:
            return f"Loan with ID {user_loan_id} not found in the results DataFrame."
    return render_template('pred.html')


@app.route('/predict.j', methods=['POST'])
def predict_loan():
    print('a hit')
    user_loan_id = request.form['loan_id']
    print(type(user_loan_id))
    if user_loan_id in results_df['loan_id'].astype(str).values:
        user_row = results_df[results_df['loan_id'].astype(str) == user_loan_id]
        user_prediction = user_row['Predicted_Loan_Status'].iloc[0]
        return jsonify({'prediction': f"Predicted Loan Status for Loan ID {user_loan_id}: {user_prediction}"})
    else:
        return jsonify({'error': f"Loan with ID {user_loan_id} not found in the results DataFrame."})


if __name__ == "__main__":
    app.run(debug =True)
    print('running')