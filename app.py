from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey123"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "register"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return "Username already exists"
        hashed_password = generate_password_hash(password)
        

        user = User(
            username=username,
            password= hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(
            username=username
        ).first()

        print("User Found:" , user)

        if user:
            print("Stored Password:" , user.password)
            print(
                "Password Match:" ,
                check_password_hash(user.password,password)
            )
            

        if user and check_password_hash(user.password , password):

            login_user(user)

            return redirect('/dashboard')

        return "Invalid Username or Password"

    return render_template('login.html')

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    return redirect("/register")





@app.route("/dashboard")
@login_required
def dashboard():

    total_expense = db.session.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id
    ). scalar()

    if total_expense is None:
        total_expense = 0
    
    total_transactions = Expense.query.filter_by(
        user_id = current_user.id
    ).count()

    category_totals = {}
    expenses= Expense.query.filter_by(
        user_id = current_user.id
    ).all()


    for expense in expenses:
        if expense.category in category_totals:
            category_totals[expense.category]+= expense.amount
        else:
            category_totals[expense.category] = expense.amount
    
    top_category = "No Data"

    if category_totals:
        top_category = max(category_totals , key = category_totals.get)

    recent_activity = Expense.query.filter_by(
        user_id = current_user.id
    ).order_by(
        Expense.id.desc()
    ).first()

    recent_expenses = Expense.query.filter_by(
        user_id = current_user.id
        ).order_by(
            Expense.id.desc()
        ).limit(5).all()


    return render_template(
        "dashboard.html" ,
        total_expense = total_expense,
        total_transactions = total_transactions,
        top_category = top_category,
        recent_activity = recent_activity,
        recent_expenses = recent_expenses)



@app.route('/add-expense' , methods=['GET','POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        category = request.form['category']

        expense = Expense(
            title = title,
            amount = float(amount),
            category = category,
            user_id = current_user.id
        )

        db.session.add(expense)
        db.session.commit()

        return redirect('/dashboard')
        
    return render_template('add_expense.html')


@app.route('/expenses')
@login_required
def expenses():

    search = request.args.get('search')

    if search:

        expenses = Expense.query.filter(
            Expense.title.contains(search),
            Expense.user_id == current_user.id
        ).all()

    else:

        expenses = Expense.query.filter_by(
            user_id = current_user.id
        ).all()

    return render_template(
        'expenses.html',
        expenses=expenses
    )



@app.route('/delete-expense/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(
        id = id,
        user_id = current_user.id
    ).first_or_404()

    db.session.delete(expense)
    db.session.commit()

    return redirect('/expenses')



@app.route('/edit-expense/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):

    expense = Expense.query.filter_by(
        id = id ,
        user_id = current_user.id
    ).first_or_404()

    if request.method == 'POST':

        expense.title = request.form['title']
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']

        db.session.commit()

        return redirect('/expenses')

    return render_template(
        'edit_expense.html',
        expense=expense
    )



@app.route('/analytics')
@login_required
def analytics():

    expenses = Expense.query.filter_by(
        user_id = current_user.id
    ).all()

    category_totals = {}

    for expense in expenses:

        if expense.category in category_totals:
            category_totals[expense.category] += expense.amount
        else:
            category_totals[expense.category] = expense.amount

    highest_expense = Expense.query.filter_by(
        user_id = current_user.id
    ).order_by(
        Expense.amount.desc()
    ).first()
        


    total_expense = db.session.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id
    ).scalar()

    if total_expense is None:
        total_expense = 0

    return render_template(
        'analytics.html',
        category_totals=category_totals,
        highest_expense=highest_expense,
        total_expense=total_expense
    )


@app.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():

    budget = Budget.query.filter_by(
        user_id = current_user.id
    ).first()

    if request.method == 'POST':

        amount = float(request.form['amount'])

        if budget:
            budget.amount = amount
        else:
            budget = Budget(
                amount=amount,
                user_id = current_user.id
                )
            db.session.add(budget)

        db.session.commit()

        return redirect('/budget')

    return render_template(
        'budget.html',
        budget=budget
    )

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect('/login')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


