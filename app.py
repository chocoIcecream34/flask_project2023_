from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

app= Flask(__name__)
app.config["SECRET_KEY"] = "helloosp"
DB = DBhandler()


@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route("/signup")
def signUp():
    return render_template("signUp.html")


@app.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = data.get('pw')
    print("Password:", pw)
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signUp.html")


@app.route("/productList")
def productList():
    return render_template("productList.html")


@app.route("/productRegister")
def productRegister():
    return render_template("productRegister.html")


@app.route("/reviewRegister")
def reviewRegister():
    return render_template("reviewRegister.html")


@app.route("/myReview")
def myReview():
    return render_template("myReview.html")


@app.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/img/{}".format(image_file.filename))
    data = request.form
    if data['price_method'] == "일반거래":
        data['normal_price'] = request.form.get("normal-price")
        data['auction_end_time'] = None
        data['auction_min_bid'] = None
        data['auction_max_bid'] = None
    elif data['price_method'] == "경매":
        data['normal_price'] = None
        data['auction_end_time'] = request.form.get("auction-end-time")
        data['auction_min_bid'] = request.form.get("auction-min-bid")
        data['auction_max_bid'] = request.form.get("auction-max-bid")
    DB.insert_item(data['name'], data, image_file.filename)

    return render_template("productSubmitResult.html", data=data, img_path="static/img/{}".format(image_file.filename))


@app.route("/myPage")
def myPage():
    # 여기에 마이페이지 로직 추가하기!
    return render_template("myPage.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')