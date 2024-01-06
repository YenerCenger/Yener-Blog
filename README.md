# Yener Blog

Bu basit blog uygulaması, kullanıcılara makalelerini paylaşma, kullanıcı hesapları oluşturma, makaleleri düzenleme veya silme, dosya yükleme ve arama gibi çeşitli özelliklere sahiptir.

## Kullanım

1. **Uygulamayı Çalıştırma:**
    - Uygulamayı başlatmak için terminal veya komut istemcisine gidin ve `app.py` dosyasının bulunduğu dizinde şu komutu çalıştırın:
      ```bash
      python app.py
      ```
    - Uygulama `http://127.0.0.1:5000/` adresinde çalışacaktır.

2. **Ana Sayfa:**
    - Tarayıcınızdan `http://127.0.0.1:5000/` adresini ziyaret edin.
    - Blog makalelerini keşfedin ve buradan diğer sayfalara geçiş yapın.

3. **Kayıt Olma:**
    - Yeni bir kullanıcı hesabı oluşturmak için `http://127.0.0.1:5000/register` adresine gidin.
    - Adınızı, kullanıcı adınızı, e-posta adresinizi ve parolanızı girin.
    - Hesap oluşturduktan sonra giriş yapın.

4. **Giriş Yapma:**
    - Hesabınıza giriş yapmak için `http://127.0.0.1:5000/login` adresine gidin.
    - Kullanıcı adınızı ve parolanızı girin.

5. **Makaleler:**
    - `http://127.0.0.1:5000/articles` adresinde tüm makaleleri görüntüleyin.
    - Kendi makalenizi eklemek için `http://127.0.0.1:5000/addarticle` adresine gidin.
    - Makale başlığı ve içeriğini girin, ardından makalenizi kaydedin.

6. **Makale Güncelleme ve Silme:**
    - Kendi makalenizi `http://127.0.0.1:5000/dashboard` adresindeki kontrol panelinden düzenleyebilir veya silebilirsiniz.
    - Her makale için düzenle ve sil seçenekleri bulunmaktadır.

7. **Dosya Yükleme:**
    - `http://127.0.0.1:5000/uploadfile` adresine giderek dosya yükleyin.
    - Sadece belirli uzantılardaki dosyaları yükleyebilirsiniz (png, jpeg, jpg, gif).

8. **Hesap Bilgileri Güncelleme ve Silme:**
    - Hesap bilgilerinizi `http://127.0.0.1:5000/account` adresinden görüntüleyebilir ve güncelleyebilirsiniz.
    - Hesabınızı silmek için `http://127.0.0.1:5000/deleteaccount` adresine gidin.

9. **Makale Arama:**
    - `http://127.0.0.1:5000/search` adresinden arama yaparak istediğiniz kelimeye uygun makaleleri bulun.

## Kullanılan Teknolojiler

- Flask: Web uygulaması geliştirmek için kullanılmıştır.
- Flask-MySQLdb: MySQL veritabanı ile etkileşim sağlamak için kullanılmıştır.
- WTForms: Formları oluşturmak ve doğrulama yapmak için kullanılmıştır.
- Passlib: Parola şifreleme için kullanılmıştır.
- Werkzeug: Güvenli dosya yükleme işlemleri için kullanılmıştır.

## Geliştirme

1. Kodu bilgisayarınıza indirin:
    ```bash
    git clone https://github.com/kullanici/yener-blog.git
    cd yener-blog
    ```

2. Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

3. Uygulamayı çalıştırın:
    ```bash
    python app.py
    ```

## Katkıda Bulunma

- Hataları bildirmek veya önerilerde bulunmak için [GitHub proje sayfası](https://github.com/kullanici/yener-blog) üzerinden "Issues" bölümünü kullanabilirsiniz.
- Kodunuza katkıda bulunmak için "Pull Requests" gönderebilirsiniz.

## Lisans

Bu proje, [MIT lisansı](LICENSE) altında lisanslanmıştır.

---

# Yener Blog

This simple blog application offers various features such as sharing articles, creating user accounts, editing or deleting articles, file uploads, and searching.

## Usage

1. **Run the Application:**
    - Go to the terminal or command prompt and run the following command in the directory where the `app.py` file is located:
      ```bash
      python app.py
      ```
    - The application will run at `http://127.0.0.1:5000/`.

2. **Home Page:**
    - Visit `http://127.0.0.1:5000/` from your browser.
    - Explore blog articles and navigate to other pages from here.

3. **Registration:**
    - Go to `http://127.0.0.1:5000/register` to create a new user account.
    - Enter your name, username, email address, and password.
    - After creating an account, log in.

4. **Login:**
    - To log in to your account, visit `http://127.0.0.1:5000/login`.
    - Enter your username and password.

5. **Articles:**
    - View all articles at `http://127.0.0.1:5000/articles`.
    - To add your own article, go to `http://127.0.0.1:5000/addarticle`.
    - Enter the article title and content, then save your article.

6. **Article Update and Delete:**
    - You can edit or delete your own article from the control panel at `http://127.0.0.1:5000/dashboard`.
    - Edit and delete options are available for each article.

7. **File Upload:**
    - Upload files by visiting `http://127.0.0.1:5000/uploadfile`.
    - You can only upload files with specific extensions (png, jpeg, jpg, gif).

8. **Account Information Update and Delete:**
    - View and update your account information at `http://127.0.0.1:5000/account`.
    - To delete your account, go to `http://127.0.0.1:5000/deleteaccount`.

9. **Article Search:**
    - Search for articles by visiting `http://127.0.0.1:5000/search`.
    - Find articles that match your desired keyword.

## Technologies Used

- Flask: Used for developing web applications.
- Flask-MySQLdb: Used to interact with the MySQL database.
- WTForms: Used for creating forms and performing validation.
- Passlib: Used for password encryption.
- Werkzeug: Used for secure file upload operations.

## Development

1. Clone the code to your computer:
    ```bash
    git clone https://github.com/kullanici/yener-blog.git
    cd yener-blog
    ```

2. Install the necessary libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python app.py
    ```

## Contribution

- To report bugs or make suggestions, you can use the "Issues" section on the [GitHub project page](https://github.com/kullanici/yener-blog).
- To contribute to the code, you can submit "Pull Requests".

## License

This project is licensed under the [MIT License](LICENSE).
