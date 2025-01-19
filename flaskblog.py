from flask import Flask,render_template
app=Flask(__name__)
posts=[
{
    "title":"First Post",
    "author":"Chitransh Gaur",
    "Date_Posted":"19/01/25",
    "content":"aise hi likh rha hu ainwaiyyn"
}

]

@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template("about.html", title="About")

if __name__=="__main__":
    app.run(debug=True)