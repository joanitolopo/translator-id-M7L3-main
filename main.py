# Impor modul
from flask import Flask, render_template,request, redirect
# Menghubungkan perpustakaan basis data
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Menghubungkan SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Membuat sebuah db
db = SQLAlchemy(app)
# Membuat sebuah tabel

# Tugas #1. membuat sebuah db
class Card(db.Model):
    # membuat kolom
    #id
    id = db.Column(db.Integer, primary_key=True)
    # judul
    title = db.Column(db.String(100), nullable=False)
    # penjelasan
    subtitle = db.Column(db.String(300), nullable=False)
    # Text
    text = db.Column(db.Text, nullable=False)

    # Luaran
    def __repr__(self):
        return f'<Card {self.id}>'


# Menjalankan halaman dengan konten
@app.route('/')
def index():
    # Luaran objek dari DB
    # Tugas #2. Buatlah agar objek DB ditampilkan di index.html
    cards = Card.query.order_by(Card.id).all()

    return render_template('index.html', cards=cards)

# Menjalankan halaman dengan kartu
@app.route('/card/<int:id>')
def card(id):
    # Tugas #2. Gunakan id untuk menunjukkan kartu yang tepat
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Menjalankan halaman dengan inisialisasi kartu
@app.route('/create')
def create():
    return render_template('create_card.html')

# Bentuk kartu
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Membuat objek untuk diteruskan ke DB

        # Tugas #2. Membuat cara untuk menyimpan data dalam DB
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)