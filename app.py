from flask import Flask, request, render_template
import pickle
import numpy as np

# logistic Model File
model = pickle.load(open("affair_model.pkl", "rb"))
app = Flask(__name__)


# Processing data
def ocupationList(data):
    lis = [0, 0, 0, 0, 0]
    if data == 1:
        return lis

    lis[data-2] = lis[data-2] + 1
    print("done ", lis )

    return lis


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods=["POST"])
def predict():
    try :

        if request.method == 'POST':
            # Storing data from Form
            occupation = int(request.form.get("occup"))
            h_occupation = int(request.form.get("Hoccup"))
            age = float(request.form.get("age"))
            year_of_marriage = float(request.form.get("yom"))
            children = int(request.form.get("child"))
            religious = int(request.form.get("religious"))
            marriage_rating = int(request.form.get('Mrate'))
            education = int(request.form.get("education"))

            print(occupation, h_occupation, age, year_of_marriage, children,
                  marriage_rating, education,religious)

            # transforming Data
            a = ocupationList(occupation)
            b = ocupationList(h_occupation)
            print("a,b recived")
            lis = [marriage_rating, age, year_of_marriage, children, religious, education]
            print("lis : ", lis)
            # Hstacking data

            data = [list(np.hstack(([1], a, b, lis)))]
            print(data)

            result = model.predict(data)[0]
            print(result)

        return render_template("result.html", result=result)
    except Exception as e:
        print(e)
        return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)
