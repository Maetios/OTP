from flask import Flask, render_template, request
from flask_mail import Mail, Message
from random import randint

app = Flask(__name__)

# Configurazione di Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'youremail@gmail.com'  # Inserisci qui l'indirizzo email del mittente
app.config['MAIL_PASSWORD'] = 'password'  # Inserisci qui la password dell'account email del mittente

mail = Mail(app)

# Dizionario per memorizzare i codici OTP generati
otp_dict = {}

# Pagina iniziale con il form di login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Controlla le credenziali inserite dall'utente
        username = request.form['username']
        password = request.form['password']
        if username == "youremail@gmail.com" and password == "1234":
            # Genera un codice OTP casuale
            otp = str(randint(1000, 9999))
            # Memorizza il codice OTP associato all'utente
            otp_dict[username] = otp

            # Invia il codice OTP all'indirizzo email specificato
            send_otp_email(username, otp)

            # Reindirizza l'utente alla pagina per inserire il codice OTP
            return render_template('otp.html', username=username)

    return render_template('loginotp.html')

# Pagina per l'inserimento del codice OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    username = request.form['username']
    otp = request.form['otp']

    # Controlla se l'utente ha un codice OTP associato
    if username in otp_dict:
        # Recupera il codice OTP generato per l'utente
        generated_otp = otp_dict[username]

        # Controlla se il codice OTP inserito corrisponde a quello generato
        if otp == generated_otp:
            # Accesso effettuato correttamente
            return render_template('successotp.html', username=username)
        else:
            # Codice OTP non valido
            return render_template('otp.html', username=username, error=True)
    else:
        # Utente non valido o codice OTP scaduto
        return render_template('otp.html', username=username, error=True)

# Funzione per inviare l'email con il codice OTP utilizzando Flask-Mail
def send_otp_email(email, otp):
    msg = Message('Codice OTP', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Il tuo codice OTP è: {otp}"
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
