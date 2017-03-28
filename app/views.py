#!/usr/local/bin/python
# coding: utf-8

from flask import render_template, flash, redirect, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, RegisterForm, ListingForm, CommentaryForm, ListingIndex, UserEditProfile, PassRecoveryForm
from .models import Users, Condo, Images, Comment, Reports
from .email import emailNotifComment, emailNotifRegister, emailNotifPassRecovery, emailNotifCondoMetCriteria, adminMailSend
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, COMMENTS_PER_PAGE, MAX_PICS
import datetime, random, os
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
from passlib.hash import sha256_crypt
from functools import wraps



####################     Required func     ###################
@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.lastSeen = datetime.datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
################################################################



####################     Helper func     ###################
def getCondoHighestId():
    arr = []
    tmp = Condo.query.all()
    for tm in tmp:
        arr.append(tm.condoId)
    return max(arr)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def passGenerator():
    chars = "abcdefghijklmnopqrstuvwxyz!@()0123456789"
    password = ""
    for i in range(8):
        next_index = random.randrange(len(chars))
        password += chars[next_index]
    return password

def searchQueryPlusArea(city, area, types, price, quad, rooms, floor, keyword):
    query = Condo.query.filter(Condo.city == city,
                               Condo.area == area,
                               Condo.types == types,
                               Condo.price >= price.split(',')[0],
                               Condo.price <= price.split(',')[1],
                               Condo.quadrature >= quad.split(',')[0],
                               Condo.quadrature <= quad.split(',')[1],
                               Condo.rooms >= rooms.split(',')[0],
                               Condo.rooms <= rooms.split(',')[1],
                               Condo.floor >= floor.split(',')[0],
                               Condo.floor <= floor.split(',')[1],
                               Condo.isApproved == 1,
                               or_(Condo.title.like(keyword),
                                   Condo.description.like(keyword))
                               ).order_by(Condo.price.asc()).all()
    return query

def searchQuery(city, types, price, quad, rooms, floor, keyword):
    query = Condo.query.filter(Condo.city == city,
                               Condo.types == types,
                               Condo.price >= price.split(',')[0],
                               Condo.price <= price.split(',')[1],
                               Condo.quadrature >= quad.split(',')[0],
                               Condo.quadrature <= quad.split(',')[1],
                               Condo.rooms >= rooms.split(',')[0],
                               Condo.rooms <= rooms.split(',')[1],
                               Condo.floor >= floor.split(',')[0],
                               Condo.floor <= floor.split(',')[1],
                               Condo.isApproved == 1,
                               or_(Condo.title.like(keyword),
                                   Condo.description.like(keyword))
                               ).order_by(Condo.price.asc()).all()
    return query

### DECORATOR
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admins = Users.query.filter(Users.isAdmin == 1).all()
        if g.user is None or g.user not in admins:
            flash('Бараната страна е само за администратори!')
            return redirect(url_for('profile'))
        return f(*args, **kwargs)
    return decorated_function
################################################################



####################     Error request Handlers     ###################
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

@app.errorhandler(405)
def no_access_error(error):
    return render_template('errors/405.html'), 405

@app.errorhandler(500)
def db_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
########################################################################



####################     Ajax     ###################
@app.route('/condoStatusChange', methods=['POST'])
@login_required
def condoStatusChange():
    if request.method == "POST":
        cid = request.json['conId']
        qry = Condo.query.get(cid)
        if qry.available:
            setattr(qry, 'available', '0')
        else:
            setattr(qry, 'available', '1')
        db.session.commit()
    return "."

@app.route('/savePreferences', methods=['POST'])
@login_required
def savePreferences():
    if request.method == "POST":
        j = request.json

        usr = j['userid']
        qry = Users.query.get(usr)

        if request.json['tick'] == 0:
            setattr(qry, 'interestedIn', '0-')
        else:
            if j['city'] != 'Скопје':
                area = 'None'
            else:
                area = j['area']
            string = "{}-{}-{}-{}-{}-{}".format(j['tick'], j['city'], area, j['types'], j['od'], j['doo'])
            setattr(qry, 'interestedIn', string)
        db.session.commit()
    return "."

@app.route('/commentDelete', methods=['POST'])
@login_required
def commentDelete():
    if request.method == "POST":
        cid = request.json['comId']
        Comment.query.filter(Comment.commendId == cid).delete()
        db.session.commit()
    return "."

@app.route('/reportDelete', methods=['POST'])
@login_required
@admin_only
def reportDelete():
    if request.method == "POST":
        rid = request.json['repId']
        qry = Reports.query.get(rid)
        setattr(qry, 'actedOn', '1')
        db.session.commit()
    return "."

@app.route('/acceptCondo', methods=['POST'])
@login_required
@admin_only
def acceptCondo():
    if request.method == "POST":
        cid = request.json['cid']
        qry = Condo.query.get(cid)
        setattr(qry, 'isApproved', '1')
        db.session.commit()
    return "."

@app.route('/denyCondo', methods=['POST'])
@login_required
@admin_only
def denyCondo():
    if request.method == "POST":
        cid = request.json['cid']
        qry = Condo.query.get(cid)
        setattr(qry, 'actedOn', '1')
        db.session.commit()
    return "."

@app.route('/permaDelete', methods=['POST'])
@login_required
@admin_only
def permaDelete():
    if request.method == "POST":
        cid = request.json['cid']
        listingDelete(cid)
    return "."

@app.route('/adminSendEmail', methods=['POST'])
@login_required
@admin_only
def adminSendEmail():
    if request.method == "POST":
        body = request.json['body']
        email = request.json['email']
        subject = request.json['subject']
        adminMailSend(email, subject, body)
    return "."

@app.route('/reportComment', methods=['POST'])
def reportComment():
    if request.method == "POST":
        js = request.json
        rep = Reports(js['body'], js['reason'], js['cid'], js['comId'], js['userId'])
        db.session.add(rep)
        db.session.commit()
    return "."
#####################################################




####################     Dummy routes     ###################
@app.route('/about')
def about():
    return render_template('about.html', title='За сајтот')

@app.route('/terms')
def terms():
    return render_template('terms.html', title='Услови за користење')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Контактирајте не')
############################################################




####################    M A I N   FUNCS     ###################


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    """
    indCondos = Condo.query.all()
    indexCondos = random.sample(indCondos, 15)

    forms = ListingIndex()

    lastSubmitedCondo = Condo.query.filter(Condo.isApproved == 1).order_by(Condo.timestamp.desc()).first()
    mostVisitedCondo = Condo.query.filter(Condo.isApproved == 1).order_by(Condo.timesVisited.desc()).first()
    randCon = Condo.query.filter(Condo.isApproved == 1).all()
    randomCondo = random.choice(randCon)
    random.choice(randCon, )

    return render_template("index.html",
                           title='Дома',
                           forms=forms,
                           lastCondo=lastSubmitedCondo,
                           mostVisited=mostVisitedCondo,
                           randomCondo=randomCondo,
                           indexCondos=indexCondos
                           ) """
    return render_template("simple.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    price = request.args.get('price')
    quad = request.args.get('quadrature')
    floor = request.args.get('floor')
    rooms = request.args.get('rooms')
    city = request.args.get('city')
    area = request.args.get('area')
    types = request.args.get('types')
    keyword = request.args.get('keyword')

    critList = [city, area, types, price, quad, floor, rooms, keyword]

    if keyword == "":
        keyword = "%%"
    else:
        keyword = "%{}%".format(keyword)

    if city == 'Скопје':
        if area == 'сите':
            query = searchQuery(city, types, price, quad, rooms, floor, keyword)
        else:
            query = searchQueryPlusArea(city, area, types, price, quad, rooms, floor, keyword)
    else:
        query = searchQuery(city, types, price, quad, rooms, floor, keyword)

    forms = ListingIndex()

    lastSubmitedCondo = Condo.query.filter(Condo.isApproved == 1).order_by(Condo.timestamp.desc()).first()
    mostVisitedCondo = Condo.query.order_by(Condo.timesVisited.desc()).first()
    randCon = Condo.query.all()
    randomCondo = random.choice(randCon)

    return render_template("index.html",
                           title='Пребарај',
                           city=city,
                           forms=forms,
                           critList=critList,
                           lastCondo=lastSubmitedCondo,
                           mostVisited=mostVisitedCondo,
                           randomCondo=randomCondo,
                           indexCondos=query
                           )

            ######## User management #####

####################### User management ##############
@app.route('/login', methods=['GET', 'POST'])
def login():

    if g.user is not None and g.user.is_authenticated:
        flash('Веќе сте најавени!')
        return redirect(url_for('index'))

    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form, title='Најава')

    if request.method == 'POST' and form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        session['remember_me'] = form.remember_me.data

        cuser = Users.query.filter(Users.email == email).first()

        if cuser and not sha256_crypt.verify(password, cuser.password):
            flash('Не постои таков корисник')
            return redirect(url_for('login'))
        if cuser is not None:
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(cuser, remember=remember_me)
            flash('Добредојдовте {} :)'.format(cuser.fullName))
            return redirect(request.args.get('next') or url_for('profile'))
        else:
            flash('Не постои таков корисник')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Најава')

@app.route('/logout')
def logout():
    if g.user is None or not g.user.is_authenticated:
        flash('Нема логиран корисник')
        return redirect(url_for('index'))
    logout_user()
    flash('Успешно се одјавивте од системот.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if g.user is not None and g.user.is_authenticated:
        flash('Веќе сте регистрирани и логирани!', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST' and form.validate_on_submit():
        f = request.form
        mailExists = Users.query.filter(Users.email == f['email']).first()
        if mailExists:
            flash('Веќе постои регистриран корисник со зададената емаил адреса.')
            return render_template('register.html', title='Регистрација', form=form)
        ip = request.remote_addr
        hashpass = sha256_crypt.encrypt(f['password'])
        cuser = Users(
            fullName=f['fullName'],
            email=f['email'],
            password=hashpass,
            telNumber=f['telNumber'],
            regIP=ip
        )

        db.session.add(cuser)
        db.session.commit()
        emailNotifRegister(cuser)
        flash('Успешно е регистриран нов корисник со е-маил адреса: {}'.format(f['email']))
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрација', form=form)

@app.route('/user/<userid>')
def user(userid):
    if not userid.isdigit():
        flash('Внесете број после \'user/\', не карактери !')
        return redirect(url_for('index'))
    cuser = Users.query.filter_by(userId=userid).first()
    if cuser is None:
        flash('Не постои таков корисник')
        return redirect(url_for('index'))
    form = ListingForm()
    boolCurrentUser = True
    if g.user.is_authenticated:
        if cuser.userId is not g.user.userId:
            boolCurrentUser = False
        else:
            return redirect(url_for('profile'))
    else:
        boolCurrentUser = False
    allCondos = cuser.condosOwned.order_by(Condo.timestamp.desc()).all()
    allComments = cuser.commentsOwned.order_by(Comment.commTimeStamp.desc()).all()
    freeCondos = len(cuser.condosOwned.filter(Condo.available == 1).order_by(Condo.timestamp.desc()).all())
    return render_template('profile.html',
                           form=form,
                           user=cuser,
                           title='Профил',
                           condos=allCondos,
                           comments=allComments,
                           bol=boolCurrentUser,
                           freeCondos=freeCondos
                           )

@app.route('/profile')
@login_required
def profile():
    form = ListingForm()
    bol = True
    cuser = current_user
    allComments = cuser.commentsOwned.order_by(Comment.commTimeStamp.desc()).all()
    allCondos = cuser.condosOwned.order_by(Condo.timestamp.desc()).all()
    freeCondos = len(cuser.condosOwned.filter(Condo.available == 1).all())
    return render_template('profile.html',
                           form=form,
                           user=cuser,
                           title='Мојот профил',
                           condos=allCondos,
                           comments=allComments,
                           bol=bol,
                           freeCondos=freeCondos)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profileEdit():
    form = UserEditProfile()
    cuser = current_user
    if request.method == 'POST' and form.validate_on_submit():
        f = request.form
        if not sha256_crypt.verify(f['currentPassword1'], cuser.password):
        # if f['currentPassword1'] != Users.query.get(cuser.userId).password:
            flash('Грешка во тековната лозинка!')
            return redirect(url_for('profileEdit'))
        if f['password1'] == '' and f['repeatPassword1'] == '':
            mydict = {'fullName': f['fullName'], 'telNumber': f['telNumber'], 'email': f['email']}
            usr = Users.query.filter(Users.userId == cuser.userId).first()
            for k, v in mydict.items():
                setattr(usr, k, v)
                db.session.commit()
            flash('Вашите нови податоци се зачувани.')
            return redirect(url_for('index'))
        elif f['password1'] != f['repeatPassword1']:
            flash('Лозинките не се совпаѓаат')
            return render_template('profileEdit.html', form=form, user=cuser, title='Промена на поставки')
        else:
            mydict = {'fullName': f['fullName'], 'telNumber': f['telNumber'], 'email': f['email'], 'password': sha256_crypt.encrypt(f['password1']) }
            usr = Users.query.filter(Users.userId == cuser.userId).first()
            for k, v in mydict.items():
                setattr(usr, k, v)
                db.session.commit()
            flash('Вашите нови податоци се зачувани.')
            return redirect(url_for('index'))
    return render_template('profileEdit.html', form=form, user=cuser, title='Промена на поставки')
            ###########################


          ######## Listings management #####
######################################################


############### Listing management #################
@app.route('/listing/new', methods=["GET", "POST"])
@login_required
def listingNew():
    form = ListingForm()
    if request.method == "POST" and form.validate_on_submit():
        f = request.form

        area = f['areas']
        if f['city'] != 'Скопје':
            area = 'None'

        condo = Condo(
            title=f['title'],
            description=f['description'],
            city=f['city'],
            area=area,
            address=f['address'],
            quadrature=100,
            rooms=f['rooms'],
            floor=f['floor'],
            price=f['price'],
            types=f['condoType'],
            user_id=current_user.userId
        )
        CondoID = int(getCondoHighestId() + 1)
        counter = 1
        files = request.files.getlist("file")
        if len(files) > MAX_PICS:
            flash('Дозволени се најмногу {} слики на оглас (10МB мах) !'.format(MAX_PICS))
            return render_template('listing.html', form=form, title='Нов оглас')
        if files:
            for file in files:
                if file and allowed_file(file.filename):
                    newName = 'cid{}-img{}.jpg'.format(CondoID, counter)
                    counter += 1
                    imgPath = os.path.join(UPLOAD_FOLDER, newName)
                    img = Images(
                        path=imgPath,
                        condo_id=CondoID
                    )
                    db.session.add(img)
                    file.save(os.path.join(UPLOAD_FOLDER, newName))

        db.session.add(condo)
        db.session.commit()

        allUsers = Users.query.all()
        for usr in allUsers:
            if usr.interestedIn.split('-')[0] == '1': # ako userot ima podeseno preferenci:
                if usr.interestedIn.split('-')[1] != f['city'] or usr.interestedIn.split('-')[2] != area or usr.interestedIn.split('-')[3] != f['condoType']:
                    print('ne biva')
                else:
                    if usr.interestedIn.split('-')[4] <= f['price'] <= usr.interestedIn.split('-')[5]:
                        if usr != current_user:
                            emailNotifCondoMetCriteria(usr, CondoID)

        flash('Успешно објавен нов стан.')
        return redirect(url_for('listingPreview', cid=CondoID))
    return render_template('listing.html', form=form, title='Нов оглас')

@app.route('/listing/preview/<int:cid>', methods=['GET', 'POST'])
@app.route('/listing/preview/<int:cid>/<int:comPage>', methods=['GET', 'POST'])
def listingPreview(cid, comPage=1):
    condoID = Condo.query.get(cid)

    if not condoID:
        flash('Не постои таков стан!')
        return redirect(url_for('index'))

    # work-around za brisenjeto na visokot slika pri buggot so application-octet
    if len(condoID.imgsPerCondo.all()) >= MAX_PICS:
        excessPic = condoID.imgsPerCondo.order_by(Images.path.desc()).first()
        db.session.delete(excessPic)
        db.session.commit()
        os.remove(excessPic.path)

    condoID.timesVisited += 1
    db.session.commit()
    condoPics = condoID.imgsPerCondo.all()
    comments = condoID.comsPerCondo.order_by(Comment.commTimeStamp.desc()).paginate(comPage, COMMENTS_PER_PAGE, False)
    similarCondos = Condo.query.filter(Condo.city == condoID.city, Condo.types == condoID.types, Condo.isApproved == 1).order_by(func.random().desc()).limit(5).all()
    comForm = CommentaryForm()
    return render_template('preview.html',
                           ccid=condoID,
                           cpics=condoPics,
                           coms=comForm,
                           comments=comments,
                           title='Преглед на стан',
                           simCon=similarCondos)

@app.route('/listing/edit/<int:cid>')
@login_required
def listingEdit(cid):
    form = ListingForm()
    condoID = Condo.query.get(cid)
    if not condoID:
        flash('Не постои таков стан!')
        return redirect(url_for('index'))
    if condoID.user_id is not current_user.userId:
        flash('Немате доволно привилегии за таква акција!')
        return redirect(url_for('index'))
    condoPics = condoID.imgsPerCondo.all()
    return render_template('listingEdit.html', ccid=condoID, cpics=condoPics, form=form, title='Измена на оглас')

@app.route('/listing/editedSubmit', methods=['POST'])
@login_required
def listingEditedSubmit():
    f = request.form

    pics2Delete = f.getlist('imgId')  # dobiva lista so slikite koi treba da se brisat
    files = request.files.getlist("file")  # novi sliki, dokolku gi ima

    cid = f['hiddenCondoId']  # id na tekovniot stan
    condo = Condo.query.get(cid)  # condo objekt

    highestIndexPic = condo.imgsPerCondo.order_by(Images.imgId.desc()).first()  # Zemi ja poslednata slika od setot
    counter = int(str(highestIndexPic).split('/')[3].split('-')[1].split('.')[0][3:]) + 1  # PAMETNO selektiranje na najvisokoto brojche od setot so sliki

    if pics2Delete:
        for picID in pics2Delete:
            pic = Images.query.get(picID)
            db.session.delete(pic)
            os.remove(pic.path)
        db.session.commit()

    picsLeft = len(condo.imgsPerCondo.all())
    if files:
        if len(files) + picsLeft > MAX_PICS + 1:
            flash('Вкупниот број на слики после бришење и додавање нови не смее да надмине {}!'.format(MAX_PICS))
            return redirect(url_for('listingEdit', cid=cid))
        for file in files:
            if file and allowed_file(file.filename):
                newName = 'cid{}-img{}.jpg'.format(cid, counter)
                counter += 1
                imgPath = os.path.join(UPLOAD_FOLDER, newName)
                img = Images(
                    path=imgPath,
                    condo_id=cid
                )
                db.session.add(img)
                file.save(os.path.join(UPLOAD_FOLDER, newName))

    area = f['areas']
    if f['city'] != 'Скопје':
        area = 'None'

    mydict = {'title': f['title'], 'description': f['description'], 'city': f['city'], 'address': f['address'],
              'area': area, 'quadrature': f['quadrature'], 'rooms': f['rooms'], 'floor': f['floor'],
              'price': f['price'], 'types':f['condoType'],'timestamp': datetime.datetime.utcnow(), 'isApproved':'0', 'actedOn':'0'}

    for k, v in mydict.items():
        setattr(condo, k, v)
    db.session.commit()

    allUsers = Users.query.all()
    for usr in allUsers:
        if usr.interestedIn.split('-')[0] == '1':  # ako userot ima podeseno preferenci:
            if usr.interestedIn.split('-')[1] != f['city'] or usr.interestedIn.split('-')[2] != area or usr.interestedIn.split('-')[3] != f['condoType']:
                print(' ')
            else:
                if usr.interestedIn.split('-')[4] <= f['price'] <= usr.interestedIn.split('-')[5]:
                    if usr != current_user:
                        emailNotifCondoMetCriteria(usr, cid)

    flash('Податоците беа успешно променети.')
    return redirect(url_for('listingPreview', cid=cid))

@app.route('/listing/delete/<int:cid>')
@login_required
def listingDelete(cid):
    condoID = Condo.query.get(cid)
    if not condoID:
        flash('Не постои таков стан!')
        return redirect(url_for('index'))
    if not g.user.is_admin:
        if condoID.user_id is not current_user.userId:
            flash('Немате доволно привилегии за таква акција!')
            return redirect(url_for('index'))
    condoPics = condoID.imgsPerCondo.all()
    condoComs = condoID.comsPerCondo.all()
    if condoPics:
        for pic in condoPics:
            db.session.delete(pic)
            os.remove(pic.path)
    if condoComs:
        for com in condoComs:
            db.session.delete(com)
    db.session.delete(condoID)
    db.session.commit()
    flash('Избришан е станот со наслов: {}'.format(condoID.title))
    return redirect(url_for('profile'))

@app.route('/comSub', methods=['POST'])
@login_required
def comSub():
    if request.method == "POST":
        condoId = request.form['condoId']
        comm = Comment(
            body=request.form['body'],
            user_id=current_user.userId,
            condo_id=condoId
        )
        db.session.add(comm)
        db.session.commit()
        condo = Condo.query.get(condoId)
        emailNotifComment(condo.condoOwner, condo)  # izvesti go oglasuvacot deka mu imat komentirano
        flash('Успешно додаден нов коментар.')
        return redirect(url_for('listingPreview', cid=condoId))
           ########################################
#########################################################


@app.route('/adminpanel', methods=['GET','POST'])
@login_required
@admin_only
def adminPanel():
    condos = Condo.query.filter(Condo.isApproved == 0).all()
    users = Users.query.all()
    reports = Reports.query.filter(Reports.actedOn == 0).all()
    return render_template('adminTemplate.html',
                           condos=condos,
                           users=users,
                           reports=reports,
                           title='Админ панел')

@app.route('/passRecovery', methods=['GET','POST'])
def passRecovery():
    form = PassRecoveryForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = request.form['email']
        user = Users.query.filter(Users.email == email).first()
        if user:
            text = 'Новата лозинка ви е испратена на вашата е-маил адреса.'
            newPass = passGenerator()
            newHashPass = sha256_crypt.encrypt(newPass)
            setattr(user, 'password', newHashPass)
            db.session.commit()
            emailNotifPassRecovery(user, newPass)
        else:
            text = 'Не постои корисник со таква е-маил адреса. <br>Обидете се повторно'
        return render_template('recoverPass.html', form=form, title='Заборавена лозинка', text=text)

    return render_template('recoverPass.html', form=form, title='Заборавена лозинка')
