import requests
from flask import Flask, redirect, request, url_for, session
import urllib.parse

app = Flask(__name__)

# Credenciais do cliente OAuth2
# client_id = '6024824416511325'
# client_secret = 'HochGPffTDwqP2FK5p31gt6MtVdkoVQo'
# redirect_uri = 'https://www.google.com'  # Certifique-se de que esta URL está registrada no Mercado Livre
# authorization_base_url = 'https://auth.mercadolivre.com.br/authorization'
# token_url = 'https://api.mercadolibre.com/oauth/token'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Rota 01
@app.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        return redirect(url_for('get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button
        </form>
        """

if __name__ == '__main__':
    app.run()