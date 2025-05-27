from flask import Flask, render_template, request, redirect
from models import db, User, Item
from sqlalchemy import or_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db.init_app(app)




with app.app_context():
    db.create_all()
    print('db created')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form

        print(data)

        user = User.query.filter_by(username=data['username'], password=data['password']).first()
        print(user, 'user')
        if user:
            user = User.query.all()
            return render_template('dashboard.html', user=user)
        else:
            print('user not found')
            return render_template('login.html')
    if request.method == 'GET':
        return '<h1> Hello World</h1>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user.username == data['username']:
            print('Username already used')
            return render_template('register.html')
        else:
            if data['password'] == data['confirm_password']:
                
                new_user = User(username=data['username'], password=data['password'])
                db.session.add(new_user)
                db.session.commit()
                return render_template('login.html')
            else:
                print('password and confirm password didnt match')
                return render_template('register.html')
            

@app.route('/dashboard')
def dashboard():
    user = User.query.all()
    return render_template('dashboard.html', user=user)

@app.route('/inventory')
def inventory():
    
    item = Item.query.all()

    return render_template('inventory.html', item=item)




@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.form

    new_data = Item(item_name=data['item_name'], item_price=data['item_price'], item_amount=data['item_amount'], item_exp_date=data['item_exp_date'])

    db.session.add(new_data)
    db.session.commit()
    
    
    item = Item.query.all()


    return render_template('inventory.html', item=item)

@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    return 'test'


@app.route('/update_item/<int:item_id>', methods=['POST', 'GET'])
def update_item(item_id):
    if request.method == 'GET':
        data = Item.query.get_or_404(item_id)
        
        return render_template('partials/item_row.html', data=data)
    
    elif request.method == 'POST':
        form = request.form
        item = Item.query.get_or_404(item_id)

        item.item_id = form['item_id']
        item.item_name = form['item_name']
        item.item_price = form['item_price']
        item.item_amount = form['item_amount']
        item.item_exp_date = form['item_exp_date']
        
        db.session.commit()

        data = Item.query.get_or_404(item_id)

        
        


        return render_template('partials/item_row_final.html', data=data)




# @app.route('/update_item/<int:item_id>', methods=['POST', 'GET'])
# def update_item(item_id):
#     data = request.form
#     item = Item.query.get_or_404(item_id)
#     if request.method == 'GET':
        
#         return render_template('partials/item_row.html', item=item)
#     elif request.method == 'POST':
#         item.item_name = data['item_name']
#         item.item_price = data['item_price']
#         item.item_amount = data['item_amount']
#         item.item_exp_date = data['item_exp_date']
#         db.session.commit()

#         return '', 204
    


@app.route('/search_item', methods=['POST'])
def search_item():
    search = request.form
    

    item = Item.query.filter(
        or_(
            Item.item_name.ilike(f"%{search['search']}%")
        )
    ).all()
    


    print(item)

    return render_template('partials/item_table.html', item=item)


@app.route('/setting')
def setting():
    
    return render_template('setting.html')



@app.route('/print_item/<int:item_id>', methods=['POST'])
def print_item(item_id):
    item = Item.query.get_or_404(item_id)

    print(item, 'hii')
    return render_template('partials/print_item.html',  item=item)









if __name__ == '__main__':
    app.run(debug=True)