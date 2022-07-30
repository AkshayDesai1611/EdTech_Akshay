from flask import Flask, render_template, request
#from flask_cors import cross_origin
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()


app = Flask(__name__)
model = pickle.load(open('edtechrandommodel1.pkl', 'rb'))

@app.route('/',methods=['GET'])
#@app.route("/")
#@cross_origin()
def Home():
    return render_template('index.html')

standard_to = StandardScaler()

@app.route("/predict", methods = ['POST'])
#@cross_origin()
def predict():
    if request.method == 'POST':
        Institute_brand_value = request.form['Institute_brand_value']
        if (Institute_brand_value=='Medium'):
            Institute_brand_value=2
        elif (Institute_brand_value=='High'):
            Institute_brand_value=0
        else:
            Institute_brand_value=1
        Course_Offered = request.form['Course_Offered']
        if (Course_Offered=='Tableau'):
            Course_Offered=4
        elif (Course_Offered=='Data_Science'):
            Course_Offered=1
        elif (Course_Offered=='AI'):
            Course_Offered=0
        elif (Course_Offered=='Ethical_hacking'):
            Course_Offered=2
        else:
            Course_Offered=3
        Course_level = request.form['Course_level']
        if (Course_level=='Intermediate'):
            Course_level = 2
        elif (Course_level=='Beginers'):
            Course_level = 1
        else:
            Course_level = 0
        Total_Course_Hours = int(request.form['Total_Course_Hours'])
        
        Webportal_LifetimeAccess =request.form['Webportal_LifetimeAccess']
        
        if (Webportal_LifetimeAccess =='Yes'):
            Webportal_LifetimeAccess=1
        else:
            Webportal_LifetimeAccess=0
        Certification_Exam = request.form['Certification_Exam']
        
        if (Certification_Exam=='Yes'):
            Certification_Exam=2
        elif(Certification_Exam=='Not Applicable'):
            Certification_Exam=1
        else:
            Certification_Exam=0
        
        Placement_Offered = request.form['Placement_Offered']
        if (Placement_Offered=='Yes'):
            Placement_Offered=1
        else:
            Placement_Offered=0
        data = [Institute_brand_value,Course_Offered,Course_level,Total_Course_Hours,Webportal_LifetimeAccess,Certification_Exam,Placement_Offered]
        data = lb.fit_transform(data)
        prediction=model.predict([data])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you have no course at this price")
        else:
            return render_template('index.html',prediction_text="The price of your course is {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
