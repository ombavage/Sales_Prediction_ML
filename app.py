from flask import Flask , render_template , redirect, request
import numpy as np
import pickle

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data', methods=['GET','POST'])
def data():
    columns=['Item_Weight', 'Item_Fat_Content', 'Item_Visibility', 'Item_MRP',
       'Outlet_Establishment_Year', 'Item_Type_Breads', 'Item_Type_Breakfast',
       'Item_Type_Canned', 'Item_Type_Dairy', 'Item_Type_Frozen Foods',
       'Item_Type_Fruits and Vegetables', 'Item_Type_Hard Drinks',
       'Item_Type_Health and Hygiene', 'Item_Type_Household', 'Item_Type_Meat',
       'Item_Type_Others', 'Item_Type_Seafood', 'Item_Type_Snack Foods',
       'Item_Type_Soft Drinks', 'Item_Type_Starchy Foods',
       'Outlet_Size_Medium', 'Outlet_Size_Small',
       'Outlet_Location_Type_Tier 2', 'Outlet_Location_Type_Tier 3',
       'Outlet_Type_Supermarket Type1', 'Outlet_Type_Supermarket Type2',
       'Outlet_Type_Supermarket Type3']
    
    user_input=np.zeros(27)
    
    user_input[0]=request.form['Item_Weight']

    def ifc():
        if request.form['Item Fat Content']=="Low_Fat":
                return 0
        else:
                return 1
    user_input[1]=ifc()

    user_input[2]=(float(request.form["Item_Visibility"]))**(1/3)

    user_input[3]=request.form["Item_MRP"]

    user_input[4]=(2022-int(request.form["Outlet_Establishment_Year"]))

    def item_type():
        if request.form["Item_Types"] == "Baking_Goods":
            user_input[5:20]=0
        else:
            index=columns.index(request.form["Item_Types"])
            user_input[index]=1
    item_type()

    def outlet_size():
        if request.form["Outlet_Size"] == "High":
            user_input[20:22]=0
        else:
            index=columns.index(request.form["Outlet_Size"])
            user_input[index]=1
    outlet_size()

    def outlet_Location_Type():
        if request.form["Outlet_Location_Type"] == "Tier1":
            user_input[22:24]=0
        else:
            index=columns.index(request.form["Outlet_Location_Type"])
            user_input[index]=1
    outlet_Location_Type()
    
    def Outlet_Type():
        if request.form["Outlet_Type"] == "Grocery_Store":
            user_input[24:]=0
        else:
            index=columns.index(request.form["Outlet_Type"])
            user_input[index]=1
    Outlet_Type()

    print(user_input)

    with open(r'C:\Users\Omkar Bavage\OneDrive\Desktop\Mock_Group\practise\sales\Artifacts\model.pkl','rb') as file:
        model=pickle.load(file)
    prediction= (model.predict([user_input]))**(1/0.226)
    print(prediction)
    return render_template("prediction.html",result=prediction[0])

if __name__=="__main__":
    app.run(debug=True)


    