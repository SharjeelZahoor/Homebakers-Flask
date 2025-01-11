from flask import render_template,request,redirect,url_for,flash
from homebaker import app,db
from homebaker.forms import *
from homebaker.models import *
# for login
from flask_login import login_user,LoginManager,login_required,logout_user,current_user
# for file uploading
from werkzeug.utils import secure_filename
from uuid import uuid1
import os
from sqlalchemy import or_
# page title
title='Home Bakers '
# flask login 
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You are logged out!",category="danger")
    return redirect(url_for('index'))

@app.route('/')
def index():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty

    page ='Home'
    sub_page='Home'
    pgTitle=title+' | '+page

    return render_template("index.html", page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/login', methods=['GET','POST'])
def login():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Login'
    sub_page='Login'
    pgTitle=title+' | '+page
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(loginid=form.loginid.data).first()
        if user:
            if user.password == form.password.data:
                flash(f'Login successfull for {form.loginid.data}',category='success')
                login_user(user);
                return redirect(url_for('index'))
            else:
                flash(f'Incorrect Password. Try Again!',category='danger')
        else :
            flash(f'Invalid User ID / Password. Try Again!',category='danger')

    return render_template("login.html",form=form, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/register', methods=['GET','POST'])
def register():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Register'
    sub_page='Register'
    pgTitle=title+' | '+page
    form = RegisterForm()
    if form.validate_on_submit():
        u=Users(loginid=form.loginid.data,name=form.name.data,contact=form.contact.data,email=form.email.data,password=form.password.data,address=form.address.data)
        # u.utype='Admin'
        db.session.add(u)
        db.session.commit()
        flash(f'User Registration is Successfull.',category='success')
        return redirect(url_for('login'))

    return render_template("register.html",form=form, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Profile'
    sub_page='Profile'
    pgTitle=title+' | '+page
    record = Users.query.get_or_404(userId)
    form = ProfileForm()
    if form.validate_on_submit():
        record.name=form.name.data
        record.contact=form.contact.data
        record.email=form.email.data
        record.address=form.address.data
        # record.utype='Customer'
        db.session.commit()
        flash(f'Profile info updated successfully.',category='success')
        return redirect(url_for('profile'))
    
    form.address.default = record.address
    form.process()
    return render_template("profile.html",form=form,user=record, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)


@app.route('/types')
def types():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Types'
    sub_page='Cake Types'
    pgTitle=title+' | '+page
    records = Types.query.all()
    print(records)
    return render_template("types.html",records=records, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/add-type', methods=['GET','POST'])
@login_required
def add_type():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Types'
    sub_page='Add Cake Type'
    pgTitle=title+' | '+page
    form = CakeTypeForm()
    if form.validate_on_submit():
        type=Types(title=form.title.data)
        db.session.add(type)
        db.session.commit()
        flash(f'Cake type created with title {form.title.data}',category='success')
        return redirect(url_for('types'))

    return render_template("type-form.html",form=form, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/update-type/<int:id>', methods=['GET','POST'])
@login_required
def update_type(id):
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Types'
    sub_page='Update Cake Type'
    pgTitle=title+' | '+page
    record = Types.query.get_or_404(id)
    form = CakeTypeForm()
    if form.validate_on_submit():
        record.title=form.title.data
        db.session.commit()
        flash(f'Cake type updated with title {form.title.data}',category='success')
        return redirect(url_for('types'))

    return render_template("type-form.html",form=form,record=record, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/delete-type/<int:id>', methods=['GET'])
@login_required
def delete_type(id):
    record = Types.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash(f'Cake type with title {record.title} deleted',category='success')
    return redirect(url_for('types'))

@app.route('/sizes')
def sizes():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Sizes'
    sub_page='Cake Sizes'
    pgTitle=title+' | '+page
    records = Sizes.query.all()
    print(records)
    return render_template("sizes.html",records=records, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/add-size', methods=['GET','POST'])
@login_required
def add_size():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Sizes'
    sub_page='Add Cake Size'
    pgTitle=title+' | '+page
    form = CakeSizeForm()
    if form.validate_on_submit():
        type=Sizes(title=form.title.data)
        db.session.add(type)
        db.session.commit()
        flash(f'Cake size created with title {form.title.data}',category='success')
        return redirect(url_for('sizes'))

    return render_template("size-form.html",form=form, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/update-size/<int:id>', methods=['GET','POST'])
@login_required
def update_size(id):
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Sizes'
    sub_page='Update Cake Size'
    pgTitle=title+' | '+page
    record = Sizes.query.get_or_404(id)
    form = CakeSizeForm()
    if form.validate_on_submit():
        record.title=form.title.data
        db.session.commit()
        flash(f'Cake size updated with title {form.title.data}',category='success')
        return redirect(url_for('sizes'))

    return render_template("size-form.html",form=form,record=record, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/delete-size/<int:id>', methods=['GET'])
@login_required
def delete_size(id):
    record = Sizes.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash(f'Cake size with title {record.title} deleted',category='success')
    return redirect(url_for('sizes'))

@app.route('/flavors')
def flavors():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Flavors'
    sub_page='Cake Flavors'
    pgTitle=title+' | '+page
    records = Flavors.query.all()
    print(records)
    return render_template("flavors.html",records=records, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/add-flavor', methods=['GET','POST'])
@login_required
def add_flavor():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Flavors'
    sub_page='Add Cake Flavor'
    pgTitle=title+' | '+page
    form = CakeFlavorForm()
    if form.validate_on_submit():
        type=Flavors(title=form.title.data)
        db.session.add(type)
        db.session.commit()
        flash(f'Cake flavor created with title {form.title.data}',category='success')
        return redirect(url_for('flavors'))

    return render_template("flavor-form.html",form=form, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/update-flavor/<int:id>', methods=['GET','POST'])
@login_required
def update_flavor(id):
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cake Flavors'
    sub_page='Update Cake Flavor'
    pgTitle=title+' | '+page
    record = Flavors.query.get_or_404(id)
    form = CakeFlavorForm()
    if form.validate_on_submit():
        record.title=form.title.data
        db.session.commit()
        flash(f'Cake Flavor Record updated with title {form.title.data}',category='success')
        return redirect(url_for('flavors'))

    return render_template("flavor-form.html",form=form,record=record, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/delete-flavor/<int:id>', methods=['GET'])
@login_required
def delete_flavor(id):
    record = Flavors.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash(f'Cake Flavor with title {record.title} deleted',category='success')
    return redirect(url_for('flavors'))

@app.route('/cakes', methods=['GET'])
def cakes():
    userId=0
    cCount=0
    is_admin=0
    page ='Cakes'
    sub_page='Cakes'
    if current_user.is_authenticated:
        if current_user.utype == 'Admin':
            is_admin=1
            sub_page='Our Cakes'
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    pgTitle=title+' | '+page
    records=[]
    result=0
    qf = request.args.get('qf')
    if qf:
        search = "%{}%".format(qf)
        records = Cakes.query.filter(Cakes.cflavor.like(search)).all()
        result=1
    qs = request.args.get('qs')
    if qs:
        search = "%{}%".format(qs)
        records = Cakes.query.filter(Cakes.csize.like(search)).all()
        result=1
    qt = request.args.get('qt')
    if qt:
        search = "%{}%".format(qt)
        records = Cakes.query.filter(Cakes.ctype.like(search)).all()
        result=1
    q = request.args.get('q')
    if q:
        search = "%{}%".format(q)
        records = Cakes.query.filter(or_(Cakes.ctype.like(search),Cakes.csize.like(search),Cakes.cflavor.like(search),Cakes.title.like(search))).all()
        result=1
    if result==0 and is_admin == 0:
        records = Cakes.query.filter_by(status='Active').all()
    if result==0 and is_admin == 1:
        records = Cakes.query.all()
    form=SeacrchForm()
    return render_template("cakes.html",form=form,records=records,q=q,qf=qf,qs=qs,qt=qt, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/add-cake', methods=['GET','POST'])
@login_required
def add_cake():
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cakes'
    sub_page='Add Cake'
    pgTitle=title+' | '+page
    form = CakesForm()
    form.ctype.choices = [(t.title, t.title) for t in Types.query.order_by('title')]
    form.csize.choices = [(s.title, s.title) for s in Sizes.query.order_by('title')]
    form.cflavor.choices = [(f.title, f.title) for f in Flavors.query.order_by('title')]
    if form.validate_on_submit():
        cake=Cakes(title=form.title.data,ctype=form.ctype.data,csize=form.csize.data,cflavor=form.cflavor.data,price=form.price.data,details=form.details.data,status=form.status.data)
        db.session.add(cake)
        db.session.commit()
        flash(f'Cake record created with title {form.title.data}',category='success')
        return redirect(url_for('cakes'))

    return render_template("cake-form.html",form=form, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/update-cake/<int:id>', methods=['GET','POST'])
def update_cake(id):
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cakes'
    sub_page='Update Cake'
    pgTitle=title+' | '+page
    record = Cakes.query.get_or_404(id)
    form = CakesForm()
    form.ctype.choices = [(t.title, t.title) for t in Types.query.order_by('title')]
    form.csize.choices = [(s.title, s.title) for s in Sizes.query.order_by('title')]
    form.cflavor.choices = [(f.title, f.title) for f in Flavors.query.order_by('title')]
    if form.validate_on_submit():
        record.title=form.title.data
        record.csize=form.csize.data
        record.cflavor=form.cflavor.data
        record.ctype=form.ctype.data
        record.price=form.price.data
        record.details=form.details.data
        record.status=form.status.data
        db.session.commit()
        flash(f'Cake Record updated with title {form.title.data}',category='success')
        return redirect(url_for('cakes'))
    else:
        form.status.default = record.status
        form.ctype.default = record.ctype
        form.csize.default = record.csize
        form.cflavor.default = record.cflavor
        form.details.default = record.details
        form.process()

    return render_template("cake-form.html",form=form,record=record, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/upload-cake-photo/<int:id>', methods=['GET','POST'])
def upload_cake_photo(id):
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        carts=Carts.query.filter_by(customer_id=userId).all();
        for c in carts:
            cCount = cCount + c.qty
    page ='Cakes'
    sub_page='Upload Cake Photo'
    pgTitle=title+' | '+page
    record = Cakes.query.get_or_404(id)
    form = PhotoForm()
    if form.validate_on_submit():
        file=request.files['photo']        
        photoName=secure_filename(file.filename)
        picNewName=str(uuid1())+"_"+photoName
        file.save(os.path.join(app.root_path,'static/img',picNewName))
        record.photo=picNewName
        db.session.commit()
        flash(f'Cake Photo updated {picNewName}',category='success')
        return redirect(url_for('cakes'))

    return render_template("cake-photo-form.html",form=form,record=record, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/add_to_cart/<int:id>', methods=['GET'])
def add_to_cart(id):
    userId=0
    if current_user.is_authenticated:
        userId=current_user.id
    if userId == 0:
        flash(f'Please login to add cake in cart.',category='warning')
        return redirect(request.referrer)
    record = Cakes.query.get_or_404(id)
    cart=Carts.query.filter_by(customer_id=userId,product_id=id).first()
    if cart:
        cart.qty = cart.qty + 1;
        db.session.commit()
    else:
        c= Carts(customer_id=userId,product_id=id,qty=1)
        db.session.add(c)
        db.session.commit()
    flash(f'Cake with title {record.title} has been added to cart',category='success')
    return redirect(request.referrer)

@app.route('/update-customization/<int:id>', methods=['GET','POST'])
# @login_required
def update_customization(id):
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
    if userId == 0 :
        flash(f'Login Required.',category='warning')
        return redirect(request.referrer)
    record = Carts.query.get_or_404(id)
    if request.method == "POST":
        customization=request.form["customization"]
        ctext=request.form["ctext"]
        status=request.form["status"]
        if customization == "No":
            status = 'Pending'
            ctext=''
            record.cprice = 0.0
        if "cprice" in request.form:
            record.cprice=format(request.form["cprice"])
        record.status=status
        record.customization=customization
        record.ctext=ctext
        db.session.commit()
        flash(f'Customization info updated / has been Set to {customization}',category='success')
        return redirect(request.referrer)
    
@app.route('/remove_from_cart/<int:id>', methods=['GET'])
def remove_from_cart(id):
    userId=0
    if current_user.is_authenticated:
        userId=current_user.id
    if userId == 0:
        flash(f'Please login to remove cake in cart.',category='warning')
        return redirect(url_for('cakes'))
    record = Carts.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash(f'Cake has been removed tofrom cart',category='success')
    return redirect(request.referrer)

@app.route('/customizations')
def customizations():
    userId=0
    cCount=0
    records=[]
    if current_user.is_authenticated:
        userId=format(current_user.id)
        cart=Carts.query.filter_by(customer_id=userId).all();
        for c in cart:
            cCount = cCount + c.qty
    page ='Customization'
    sub_page='Customization'
    pgTitle=title+' | '+page
    records=Carts.query.filter_by(customization='Yes').all();
    for r in records:
        r.cake=Cakes.query.get(r.product_id);

    return render_template("customization.html",records=records, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/cart')
def cart():
    userId=0
    cCount=0
    records=[]
    if current_user.is_authenticated:
        userId=format(current_user.id)
        records=Carts.query.filter_by(customer_id=userId).all();
        for c in records:
            cCount = cCount + c.qty
    page ='Cart'
    sub_page='Cart'
    pgTitle=title+' | '+page
    for r in records:
        r.cake=Cakes.query.get(r.product_id);

    return render_template("cart.html",records=records, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/checkout/<int:id>', methods=['GET','POST'])
# @login_required
def checkout(id):
    userId=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
    if userId == 0 :
        flash(f'Login Required.',category='warning')
        return redirect(request.referrer)
    user=Users.query.get(userId)
    cart = Carts.query.get_or_404(id)
    cake=Cakes.query.get(cart.product_id)
    cprice=0
    ctext=''
    total=cake.price
    order=Orders(address=user.address,customer_id=userId)
    if cart.customization == 'Yes':
        ctext=cart.ctext
        cprice=cart.cprice
        total= total + cart.cprice
        order.pmethod='Advance'
    order.price=total
    db.session.add(order)
    db.session.commit()
    order_id=order.id
    item =Items(order_id=order_id,product_id=cart.product_id,customer_id=userId,cprice=cprice,customization=cart.customization,ctext=ctext,qty=cart.qty,price=cake.price)
    db.session.add(item)
    db.session.commit()
    db.session.delete(cart)
    db.session.commit()
    flash(f'Order Has been added with Order ID = {order_id}',category='success')
    return redirect(request.referrer)

@app.route('/orders')
def orders():
    userId=0
    cCount=0
    page ='Orders'
    sub_page='Orders'
    isAdmin=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        if current_user.utype == 'Admin' :
            sub_page='Customer Orders'
            isAdmin=1
        cart=Carts.query.filter_by(customer_id=userId).all();
        for c in cart:
            cCount = cCount + c.qty

    pgTitle=title+' | '+page
    records= Orders.query.filter_by(customer_id=userId).all()
    if isAdmin==1:
        records= Orders.query.all()

    return render_template("orders.html",records=records, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/delete-order/<int:id>', methods=['GET'])
def delete_order(id):
    userId=0
    if current_user.is_authenticated:
        userId=current_user.id
    if userId == 0:
        flash(f'Please login to delete order.',category='warning')
        return redirect(request.referrer)
    order = Orders.query.get_or_404(id)
    items = Items.query.filter_by(order_id=order.id).all()
    for item in items:
        db.session.delete(item)
        db.session.commit()
    db.session.delete(order)
    db.session.commit()
    flash(f'Order has been deleted successfully',category='success')
    return redirect(request.referrer)

@app.route('/details/<int:id>', methods=['GET'])
def details(id):
    userId=0
    cCount=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
        cart=Carts.query.filter_by(customer_id=userId).all();
        for c in cart:
            cCount = cCount + c.qty
    order = Orders.query.get_or_404(id)
    user = Users.query.get(order.customer_id)
    page ='Orders'
    sub_page='Order Details'
    pgTitle=title+' | '+page
    records = Items.query.filter_by(order_id=order.id).all()
    for item in records:
        item.cake=Cakes.query.get(item.product_id);
        order.customization=item.customization
    methods=['COD','EasyPaisa','JazzCash','Bank']
    if order.status == 'Pending':
        sts=['Pending','Confirmed','Shipped','Completed']
    elif order.status == 'Confirmed':
        sts=['Confirmed','Shipped','Completed']
    elif order.status == 'Shipped':
        sts=['Shipped','Completed']
    elif order.status == 'Completed':
        sts=['Completed']
    if order.customization == 'Yes':
        methods=['EasyPaisa','JazzCash','Bank']
    return render_template("details.html",order=order,user=user,records=records,sts=sts,methods=methods, page= page, sub_page=sub_page,pgTitle=pgTitle,cCount=cCount)

@app.route('/update-address', methods=['GET','POST'])
# @login_required
def update_address():
    userId=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
    if userId == 0 :
        flash(f'Login Required.',category='warning')
        return redirect(request.referrer)
    if request.method == "POST":
        order_id=request.form["order_id"]
        address=request.form["address"]
        record = Orders.query.get_or_404(format(order_id))
        record.address=address
        db.session.commit()
        flash(f'Order Shipping Address has been updated.',category='success')
        return redirect(request.referrer)
    
@app.route('/update-order', methods=['GET','POST'])
# @login_required
def update_order():
    userId=0
    if current_user.is_authenticated:
        userId=format(current_user.id)
    if userId == 0 :
        flash(f'Login Required.',category='warning')
        return redirect(request.referrer)
    if request.method == "POST":
        order_id=request.form["order_id"]
        shippment=request.form["shippment"]
        pmethod=request.form["pmethod"]
        status=request.form["status"]
        record = Orders.query.get_or_404(format(order_id))
        record.shippment=shippment
        record.pmethod=pmethod
        record.status=status
        db.session.commit()
        flash(f'Order has been updated.',category='success')
        return redirect(request.referrer)
@app.route('/cart', methods=['GET', 'POST'])
def choose_delivery_option():
    if request.method == 'POST':
        delivery_option = request.form['delivery_option']
        item_id = request.form.get('item_id')  # Use .get() to avoid KeyError if item_id is not provided
        if item_id:
            # Process the delivery option and associate it with the specific item
            return f'Selected delivery option for item {item_id}: {delivery_option}'
        else:
            # Process the general delivery option
            return f'Selected delivery option: {delivery_option}'
    return render_template('cart.html')