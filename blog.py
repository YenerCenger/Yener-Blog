from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,g
from flask_mysqldb import MySQL
from flask import send_from_directory
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
import os
from werkzeug.utils import secure_filename


# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","danger")
            return redirect(url_for("login"))
    return decorated_function

#Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim:" , validators=[
        validators.length(4,25),
        validators.DataRequired("Lütfen bir isim belirleyin.")
        ])
    username = StringField("Kullanıcı Adı:" , validators=[
        validators.length(5,35),
        validators.DataRequired("Lütfen bir kullanıcı adı belirleyin.")
        ])
    email = StringField("Email Adresi:" , validators=[
        validators.Email(message="Lütfen Geçerli bir email adresi giriniz..."),
        validators.DataRequired("Lütfen bir email adresi belirleyin.")
        ])
    password = PasswordField("Parola:" , validators=[
        validators.length(8,25),
        validators.DataRequired("Lütfen bir parola belirleyin."),
        validators.EqualTo(fieldname="confirm",message="Parolanız uyuşmuyor....")
    ])
    confirm = PasswordField("Parola Doğrulama:")

# Kullanıcı Giriş Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

# Makale Formu
class ArticleForm(Form):
    title = StringField("Makale Başlığı",validators=[validators.length(min=5,max=100)])
    content = TextAreaField("Makale İçeriği",validators=[validators.length(min=10)])


# Dosya Yükleme
UPLOAD_FOLDER = r"C:\uploads"
ALLOWED_EXTENSIONS = {"png","jpeg","jpg","gif"}

app = Flask(__name__)
app.secret_key= "yenerblog"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "yenerblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Makale Sayfası
@app.route("/articles")
@login_required
def articles():
    cursor = mysql.connection.cursor()
    result = cursor.execute("Select * From articles")

    if (result > 0 ):
        articles = cursor.fetchall()
        return render_template("articles.html", articles = articles)
    else:
        return render_template("articles.html")

#Kayıt Olma
@app.route("/register",methods = ["GET","POST"] )
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        
        cursor = mysql.connection.cursor()

        sorgu2 = "Select * from users where username = %s"

        result = cursor.execute(sorgu2,(username,))

        if (result == 0):
            cursor = mysql.connection.cursor()

            sorgu3 = "Select * from users where email = %s"

            result2 = cursor.execute(sorgu3,(email,))

            if (result2 == 0):
                cursor = mysql.connection.cursor()

                sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"

                cursor.execute(sorgu,(name,email,username,password))

                mysql.connection.commit()

                cursor.close()
                flash("Başarıyla Kayıt oldunuz.", category= "success")
                return redirect(url_for("login"))
            else:
                flash("Bu email adresi halihazırda kullanılıyor.","danger")
                return redirect(url_for("register"))
        else:
            flash("Bu kullanıcı adı halihazırda kullanılıyor.","danger")
            return redirect(url_for("register"))
    else:
        return render_template("register.html",form=form)

#Login İşlemi
@app.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()

        sorgu = "Select * From users where username = %s"

        result = cursor.execute(sorgu,(username,))

        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]

            if sha256_crypt.verify(password_entered,real_password):
                flash("Başarıyla Giriş Yaptınız.","success")

                session["logged_in"] = True
                session["username"] = username
                
                return redirect(url_for("index"))
            else:
                flash("Kullanıcı Adı veya Parola Hatalı...",category="warning")
                return redirect(url_for("login"))


        else:
            flash("Böyle Bir kullanıcı bulunmuyor...", category="danger")
            return redirect(url_for("login"))

    else:
        return render_template("login.html", form = form)

# Detay Sayfası
@app.route("/article/<string:id>")
def article(id):
    cursor = mysql.connection.cursor()

    result = cursor.execute("Select * from articles where id = %s",(id,))

    if (result > 0):
        article = cursor.fetchone()
        return render_template("article.html",article = article)
    else:
        return render_template("article.html")


#Logout İşlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

#Kontrol Paneli
@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()

    result = cursor.execute("Select * From articles where author = %s",(session["username"],))

    if ( result > 0 ):
        articles = cursor.fetchall()
        return render_template("dashboard.html",articles = articles)
    else:
        return render_template("dashboard.html")

# Dosya Upload
    
def allowed_file(filename):
    if "." not in filename:
        return False

    file_extension = filename.rsplit(".",1)[1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        return False
    return True

@app.route("/uploadfile",methods = ["GET","POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Dosya yüklenemedi.","danger")
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == "":
            flash("Herhangi bir dosya seçilmedi.","warning")
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
            return redirect(url_for("download_file",name = filename))
    
    else:
        return render_template("uploadfile.html")

@app.route("/uploads/<name>")
def download_file(name):
    flash("Dosya Başarıyla yüklendi.","success")
    return send_from_directory(app.config["UPLOAD_FOLDER"],name)

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True)
    
# Hesap
@app.route("/account")
@login_required
def account():
    cursor = mysql.connection.cursor()

    sorgu = "Select * from users where username = %s"

    result = cursor.execute(sorgu,(session["username"],))

    if (result > 0):
        user = cursor.fetchone()
        form = RegisterForm()

        name = user["name"]
        email = user["email"]
        id = user["id"]
        return render_template("account.html",id = id, name = name ,email = email )
    else:
        flash("Böyle bir hesap bulunmuyor","warning")
        return redirect(url_for("register"))

# Hesap Bilgisi Güncelleme
@app.route("/updateinfo/<string:id>",methods = ["GET","POST"])
@login_required
def updateinfo(id):
    if (request.method == "GET"):
        cursor = mysql.connection.cursor()

        sorgu = "Select * from users where id = %s and username = %s"

        result = cursor.execute(sorgu,(id,session["username"]))

        if (result == 0):
            flash("Böyle bir kullanıcı yok veya bu işleme yetkiniz yok.","danger")
            return redirect(url_for("register"))
        else:
            user = cursor.fetchone()
            form = RegisterForm()

            form.name.data = user["name"]
            form.username.data = user["username"]
            form.email.data = user["email"]

            return render_template("updateinfo.html",form = form)
    else:
        cursor = mysql.connection.cursor()

        sorgu3 = "Select * from users where id = %s"

        result2 = cursor.execute(sorgu3,(id,))

        if (result2 == 0):
            flash("Böyle bir kullanıcı yok veya bu işleme yetkiniz yok.","danger")
            return redirect(url_for("register"))
        else:
            data = cursor.fetchone()
            real_password = data["password"]
            
        form = RegisterForm(request.form)

        newName = form.name.data
        newUsername = form.username.data
        newEmail = form.email.data
        newPassword = sha256_crypt.encrypt(form.password.data)
        oldPassword = form.confirm.data

        if sha256_crypt.verify(oldPassword,real_password):

            sorgu2 = "Update users Set name = %s, username = %s, email = %s, password = %s where id = %s"

            cursor = mysql.connection.cursor()

            cursor.execute(sorgu2,(newName,newUsername,newEmail,newPassword,id))
            
            mysql.connection.commit()

            flash("Hesap bilgileri başarıyla güncellendi","success")

            session["logged_in"] = False

            return redirect(url_for("login"))
        else:
            flash("Lütfen şuanki şifrenizi doğru girin.","danger")
            return redirect(url_for("account", id = id))

#hesap silme
@app.route("/deleteaccount/<string:id>")
@login_required
def deleteaccount(id):
    cursor = mysql.connection.cursor()

    sorgu = "Select * from users where id = %s and username = %s"

    result = cursor.execute(sorgu,(id,session["username"]))

    if (result == 0):
        flash("Böyle bir hesap bulunmuyor veya silme yetkiniz yok!","danger")
        return redirect(url_for("index"))
    else:
        sorgu2 = "Delete from users where id = %s"

        cursor.execute(sorgu2,(id,))

        mysql.connection.commit()

        flash("Hesap başarıyla silindi.","success")

        session["logged_in"] = False

        return redirect(url_for("register"))

# Makale Ekleme
@app.route("/addarticle",methods = ["GET","POST"])
@login_required
def addarticle():
    form = ArticleForm(request.form)

    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data

        cursor = mysql.connection.cursor()

        cursor.execute("Insert into articles(title,author,content) VALUES(%s,%s,%s)",(title,session["username"],content))

        mysql.connection.commit()

        cursor.close()

        flash("Makale Başarıyla Eklendi.","success")

        return redirect(url_for("dashboard"))

    return render_template("addarticle.html",form = form)

# Makale Güncelleme
@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def edit(id):
    if (request.method == "GET"):
        cursor = mysql.connection.cursor()

        sorgu = "Select * from articles where id = %s and author = %s"

        result = cursor.execute(sorgu,(id,session["username"]))

        if (result == 0):
            flash("Böyle bir makale yok veya bu işleme yetkiniz yok.","danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()

            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html",form = form)

    else:
        # POST Request
        form = ArticleForm(request.form)

        newTitle = form.title.data
        newContent = form.content.data

        sorgu2 = "Update articles Set title = %s, content = %s where id = %s"

        cursor = mysql.connection.cursor()

        cursor.execute(sorgu2,(newTitle,newContent,id))

        mysql.connection.commit()

        flash("Makale başarıyla güncellendi","success")

        return redirect(url_for("dashboard"))

# Makale Silme
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()

    sorgu = "Select * from articles where author = %s and id = %s"

    result = cursor.execute(sorgu,(session["username"] ,id))

    if result > 0:
        sorgu2 = "Delete from articles where id = %s"

        cursor.execute(sorgu2,(id,))

        mysql.connection.commit()
        
        return redirect(url_for("dashboard"))
    else:
        sorgu3 = "Select * from articles where id = %s"

        result2 = cursor.execute(sorgu3,(id,))

        if result2 > 0:
            flash("Bu Makaleyi Silme Yetkiniz Yok.","danger")
            return redirect(url_for("index"))
        else:
            flash("Böyle Bir Makale Yok.","warning")
            return redirect(url_for("index"))

# Arama URL
@app.route("/search",methods = ["GET","POST"])
def search():
    if (request.method == "GET"):
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")

        cursor = mysql.connection.cursor()

        sorgu = "Select * from articles where title like '%" + keyword + "%' "

        result = cursor.execute(sorgu)

        if (result == 0):
            flash("Aranan kelimeye uygun makale bulunamadı...","warning")
            return redirect(url_for("articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html",articles = articles)
        
if (__name__ == "__main__"):
    app.run(debug=True)
