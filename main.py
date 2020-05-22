from cs50 import SQL
from datetime import date 
import datetime
import math
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = "aikidoka17"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_dict_for_all_templates():
    db = SQL("sqlite:///database.db")
    first_name = None
    if "user_id" in session:
        first_name = db.execute("SELECT first_name FROM personal_infos WHERE user_id = :id" , id = session["user_id"])
    return dict(first_name = first_name) 
       

@app.route("/" , methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        email = request.form.get("m-l-email")   
        db = SQL("sqlite:///database.db")
        db.execute("INSERT INTO mailling_list (email) VALUES (?)", email)
        return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact-us" , methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        full_name = request.form.get("name")    
        email = request.form.get("email")
        message = request.form.get("message")
        db = SQL("sqlite:///database.db")
        db.execute("INSERT INTO contact_inquiries (full_name , email , message) VALUES (?,?,?)", full_name , email , message)
        flash("Thank you for getting in touch! " , "info")
        return redirect("/contact-us")


@app.route("/login" , methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            return redirect("/dashboard")
        return render_template("login.html")
    else:
        username = request.form.get("username")    
        password = request.form.get("password") 
        db = SQL("sqlite:///database.db")
        rows = db.execute("SELECT * FROM users WHERE username = :username AND password = :password" ,username=username , password=password)
        if len(rows) == 0:
            flash("username or password is incorrect " , "info")
            return redirect("/login")
        session["user_id"] = rows[0]["id"]
        return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html") 

    else:
        first_name = request.form.get("f-name")
        last_name = request.form.get("l-name")
        email =  request.form.get("email")
        birth = request.form.get("birth")
        gender = request.form.get("gender")
        country = request.form.get("country")
        zipcode = request.form.get("zipcode")
        current_weight = request.form.get("current-weight") 
        height = request.form.get("height")
        goal_weight = request.form.get("goalweight")
        activity = request.form.get("activity")
        progress = request.form.get("progress")
        username = request.form["username"]
        password = request.form.get("password") 
        password2 = request.form.get("password2") 

        db = SQL("sqlite:///database.db")
        email_check = db.execute("SELECT * FROM users WHERE email = :email " , email = email )
        username_check = db.execute("SELECT * FROM users WHERE username = :username " , username = username )
       
        errors = False

        if len(email_check) != 0:
            flash("email address already exist!" ,"error") 
            errors = True   

        if username == '':
            flash("username field can't be empty!" ,"error") 
            errors = True  
        elif len(username_check) != 0:
            flash("username already exist!" ,"error") 
            errors = True  

        if  password != password2:
            flash("Passwords does not match" ,"error")    
            errors = True  
        
        if errors == True:
            return redirect("/signup")
        
        # CALCULATE AGE:
        birth_array = birth.split("-")
        age = calculateAge(date(int(birth_array[0]), int(birth_array[1]), int(birth_array[2])))
        
         # CALCULATE TOTAL CALORIES:
        total_calories = None

        if gender == "male":
            BMR = (int(current_weight) * 10) + (int(height) * 6.25) - (age * 5 ) + 5
            total_calories =  math.floor((BMR * float(activity)) - int(progress))
        elif gender == "female":
            BMR = (int(current_weight) * 10) + (int(height) * 6.25) - (age * 5 ) - 161
            total_calories =  math.floor((BMR * float(activity)) - int(progress))
        
        # CALCULATE MACROS: 
        total_proteins = math.floor(total_calories * 0.40 / 4)
        total_carbs =  math.floor(total_calories * 0.35 / 4)
        total_fats =  math.floor(total_calories * 0.25 / 9)
 
        db = SQL("sqlite:///database.db")
        db.execute("INSERT INTO users (username , email , password) VALUES (?,?,?)", username , email , password)
        db.execute("INSERT INTO personal_infos (first_name , last_name , birth , gender , country , zipcode) VALUES (?,?,?,?,?,?)",
        first_name , last_name , birth , gender , country , zipcode)
        db.execute("INSERT INTO health_infos (age , current_weight , height , goal_weight , activity , progress ,total_calories , total_proteins, total_carbs, total_fats) VALUES (?,?,?,?,?,?,?,?,?,?)",
         age , current_weight , height , goal_weight , activity , progress ,total_calories , total_proteins, total_carbs, total_fats)
        return redirect("/login")


@app.route("/dashboard")
@login_required
def dashboard():
    db = SQL("sqlite:///database.db")
    row = db.execute("SELECT * FROM health_infos WHERE user_id= :sessionId" , sessionId = session["user_id"])
    now = datetime.datetime.now()
    day = now.strftime("%A")
    month =now.strftime("%B")
    dayNum = now.strftime("%d")
    year = now.strftime("%Y")
    food_rows = db.execute("SELECT * FROM food_entries WHERE user_id= :sessionId " , sessionId = session["user_id"])

    rem_cals= int(row[0]["total_calories"])
    rem_prot= int(row[0]["total_proteins"])
    rem_carbs= int(row[0]["total_carbs"])
    rem_fats= int(row[0]["total_fats"])

    for r in food_rows:
        rem_cals -= int(r["calories"])
        rem_prot -= int(r["proteins"])
        rem_carbs -= int(r["carbs"])
        rem_fats -= int(r["fats"])

    row_len = len(food_rows)
    return render_template("dashboard.html" , calories=int(row[0]["total_calories"]) , proteins=int(row[0]["total_proteins"]) ,
   carbs= int(row[0]["total_carbs"]) , fats=int(row[0]["total_fats"]) , c_weight=row[0]["current_weight"]  ,
     g_weight=row[0]["goal_weight"] , day=day , month=month , dayNum=dayNum , year=year ,food_rows=food_rows, 
     row_len=row_len , rem_cals=rem_cals , rem_prot=rem_prot , rem_carbs=rem_carbs , rem_fats=rem_fats)




@app.route("/myfood", methods=["GET", "POST"])
@login_required
def myfood():
    if request.method == "GET":
        db = SQL("sqlite:///database.db")
        rows = db.execute("SELECT * FROM food_entries WHERE user_id= :sessionId " , sessionId = session["user_id"])
        row_len = len(rows)
        return render_template("myfood.html",rows=rows, row_len=row_len, s_id=session["user_id"])
    else:
        user_id = session["user_id"]
        meal = request.form.get("meal")
        food = request.form.get("food")
        calories = request.form.get("calories")
        proteins = request.form.get("proteins")
        carbs = request.form.get("carbs")
        fats = request.form.get("fats")   

        db = SQL("sqlite:///database.db")
        db.execute("INSERT INTO food_entries (user_id, meal, food ,calories , proteins , carbs , fats) VALUES (?,?,?,?,?,?,?)",
         user_id, meal, food ,calories , proteins , carbs , fats)
         
        flash("Meal added!" , "info") 
        return redirect("/myfood")

@app.route("/delete_entry/<string:id>" , methods=["POST"])
@login_required
def delete_entry(id):
    db = SQL("sqlite:///database.db")
    db.execute("DELETE FROM food_entries WHERE meal_id = %s", [id])
    flash("Meal deleted!" , "error")
    return redirect("/myfood")

@app.route("/reset/<string:id>" , methods=["POST"])
@login_required
def reset(id):
    db = SQL("sqlite:///database.db")
    db.execute("DELETE FROM food_entries WHERE user_id = %s", [id])
    flash("Food entries has been successfully reset!" , "error")
    return redirect("/myfood")

@app.route("/nutrition-facts")
@login_required
def nutrition_facts():
    return render_template("nutritionfacts.html")

@app.route("/fitness")
@login_required
def fitness():
    return render_template("fitness.html")

@app.route("/healthy-recipes")
@login_required
def healthy_recipes():
    return render_template("healthyrecipes.html")

@app.route("/myaccount", methods=["GET", "POST"])
@login_required
def myaccount():
    if request.method == "GET":
        db = SQL("sqlite:///database.db")
        auth = db.execute("SELECT * FROM users WHERE id= :s_id" ,s_id = session["user_id"])
        row = db.execute("SELECT * FROM health_infos WHERE user_id = :id ",id = session["user_id"] )
        c_weight = row[0]["current_weight"]
        username = auth[0]["username"]
        email = auth[0]["email"]

        return render_template("myaccount.html" ,c_weight=c_weight ,username=username , email=email)
    else:
        new_password = request.form.get("newpassword")
        new_password2 = request.form.get("newpassword2")
        new_weight = request.form.get("newweight")

        errors = False
        if new_password != new_password2:
            flash("Passwords does not match" ,"error")    
            errors = True  

        if errors == True:
            return redirect("/myaccount")

        db = SQL("sqlite:///database.db")
        if new_password:
            db.execute("UPDATE users SET password=:password WHERE id=:id " , password=new_password , id=session["user_id"])
        if new_weight:     
            db.execute("UPDATE health_infos SET current_weight=:weight WHERE user_id=:id " , weight=new_weight , id=session["user_id"])

        flash("changes saved!" ,"info")   
        return redirect("/myaccount")

def calculateAge(birthDate): 
    days_in_year = 365.2425    
    age = int((date.today() - birthDate).days / days_in_year) 
    return age 

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == "__main__":
    app.run(debug=True)
   