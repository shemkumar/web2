from flask import Flask, request, render_template, make_response, redirect
import jwt

app = Flask(__name__)

SECRET_KEY = "supersonic"  # Replace with a secure key
ADMIN_PASSWORD = "thepasswordisnotea5ytog3tsohackthiswebsite"
FLAG = "root@localhost{P@ssw0rDS_r_0pti0n4l}"

@app.route('/', methods=['GET'])
def login_page():
    # Render the login page
    return render_template("index.html")

@app.route('/', methods=['POST'])
def attempt_login():
    username = request.form.get('user')
    password = request.form.get('pass')

    # Check login credentials
    if username == "demo" and password == "demo":
        pass
    elif username == "root" and password == ADMIN_PASSWORD:
        pass
    else:
        return "Invalid login.", 401  # Unauthorized error

    # Generate JWT token
    new_jwt = jwt.encode({"user": username}, SECRET_KEY, algorithm="HS256")
    if isinstance(new_jwt, bytes):
        new_jwt = new_jwt.decode('utf-8')  # Ensure the token is a string

    # Redirect to the dashboard with token in cookie
    resp = make_response(redirect("/dashboard"))
    resp.set_cookie("token", new_jwt)
    return resp

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Get the token from cookies
    token = request.cookies.get('token')
    if not token:
        return redirect("/")  # Redirect to login if no token

    try:
        # Decode and verify the JWT token
        claims = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "Token has expired.", 403  # Forbidden error
    except jwt.InvalidTokenError:
        return "Invalid token.", 403  # Forbidden error

    user = claims.get('user', 'Unknown')

    # Customize the dashboard message
    if user == "demo":
        status = "Welcome demo user! In the real app, you'd see your confidential system info here!"
    elif user == "root":
        status = f"Welcome, root@localhost! Here is your flag: {FLAG}"
    else:
        status = "User not recognized."

    # Render the dashboard
    return render_template("dashboard.html", user=user, status=status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2024, debug=True)

