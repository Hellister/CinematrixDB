from flask import Flask, render_template, redirect, url_for, request, g, flash
from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, SubmitField
from wtforms.validators import DataRequired

import sqlite3

app = Flask(__name__)

app.secret_key = 'super secret key'
DATABASE = 'cinematrix.db'

#fetches the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#form for buying tickets
class TicketForm(FlaskForm):
        email = EmailField("Email", validators=[DataRequired()])
        tickets = IntegerField("Number of tickets", validators=[DataRequired()])
        submit = SubmitField("Buy now")

#routing to home page
@app.route('/')
def home():
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT vw.auditorium_id, vw.date_time as time, mv.title, mv.price, vw.id
        FROM viewing as vw, movie as mv
        WHERE vw.movie_id=mv.id
        ORDER BY time
        LIMIT 5
        """)
    
    top5 = [dict(id=row[0], time=row[1], title=row[2], price=row[3], w_id=row[4]) for row in cursor.fetchall()]

    cursor = get_db().cursor()
    cursor.execute("""
        SELECT vw.auditorium_id, vw.date_time as time, mv.title, mv.price, vw.id
        FROM viewing as vw, movie as mv
        WHERE vw.movie_id=mv.id
        ORDER BY time
        """)
    
    entries = [dict(id=row[0], time=row[1], title=row[2], price=row[3], w_id=row[4]) for row in cursor.fetchall()]
    return render_template('home.html', top5=top5, entries=entries)

#routing to movie/ticket info
@app.route('/ticket/<int:id>', methods=["GET", "POST"])
def ticket(id):
    #gets a list of all customer emails
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT email
        FROM customer""")
    users = [row[0] for row in cursor.fetchall()]
    cursor.close()

    #counts the total amount of tickets purchased for a viewing
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT ticket_amount
        FROM ticket
        WHERE viewing_id=?""", [id])
    tkt = sum([row[0] for row in cursor.fetchall()])
    cursor.close()

    #gets the capacity of the auditorium selected
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT capacity
        FROM auditorium as ad, viewing as vw
        WHERE ad.id = vw.auditorium_id AND vw.id=?""", [id])
    capacity = [row[0] for row in cursor.fetchall()]
    cursor.close()

    #gets the detailed info for the movie to display
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT auditorium_id, date_time, title, vw.id, description, price, capacity, mv.id
        FROM viewing as vw, movie as mv, auditorium as ad
        WHERE auditorium_id=ad.id AND movie_id=mv.id AND vw.id=?""", [id])
    data = [dict(a_id=row[0], time=row[1], title=row[2], v_id=row[3], desc=row[4], price=row[5], cap=row[6], m_id=row[7]) for row in cursor.fetchall()]
    cursor.close()

    #gets the current people that have tickets
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT first_name, last_name, customer.email, customer.phone, ticket_amount
        FROM ticket, customer
        WHERE ticket.email=customer.email AND viewing_id=?
        ORDER BY last_name""", [id])
    tickets = [dict(fname=row[0], lname=row[1], email=row[2], phone=row[3], amount=row[4]) for row in cursor.fetchall()]
    cursor.close()

    form = TicketForm()
    if form.validate_on_submit():
        cursor = get_db().cursor()

        #checks that the email is valid (its in the customer database)
        if form.email.data not in users:
            flash("Please enter a valid email address")

        #checks that you do not exceed the amount of seats left
        elif (form.tickets.data + tkt) > capacity[0]:
            flash("Please enter a valid ticket amount")
            
        else:
            #gets a list of customers that have made a purchase
            cursor = get_db().cursor()
            cursor.execute("""
                SELECT email
                FROM ticket
                WHERE viewing_id=?""", [id])
            ticket_users = [row[0] for row in cursor.fetchall()]
            cursor.close()

            #checks if the customer already has bought tickets for that viewing
            if form.email.data in ticket_users:
                #gets the current number of tickets for a email address to the viewing
                cursor = get_db().cursor()
                cursor.execute("""
                    SELECT ticket_amount
                    FROM ticket
                    WHERE email=? AND viewing_id=?""", [form.email.data, id])
                ticket_amount = [row[0] for row in cursor.fetchall()]
                cursor.close()
                
                #calculates new amount of tickets for the customer
                new_amount = ticket_amount[0] + int(form.tickets.data)

                #updates the customer's ticket amount in the database to the new amount
                cursor = get_db().cursor()
                cursor.execute("""
                    UPDATE ticket
                    SET ticket_amount=?
                    WHERE email=? AND viewing_id=?""", [new_amount, form.email.data, id])
                cursor.close()

            #if the customer does not already own tickets, it adds them to the ticket database
            else:
                cursor = get_db().cursor()
                cursor.execute(
                "INSERT INTO ticket(ticket_amount, viewing_id, email) VALUES (?,?,?)",
                    [
                        form.tickets.data,
                        id,
                        form.email.data
                    ]
                )
            
        cursor.close()
        return redirect(url_for('ticket', id=id))
    
    return render_template('ticket.html', data=data, tickets=tickets, form=form, users=users, capacity=capacity[0]-tkt)