from django.shortcuts import render
from django.conf import settings

from django.core.mail import EmailMessage



import string
import random
import MySQLdb
import sshtunnel




sshtunnel.SSH_TIMEOUT = 500
sshtunnel.TUNNEL_TIMEOUT = 500



TENPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)
def index(request):
    return render(request,"index.html")


def politicacookies(request):
    return render(request,"politicacookies.html")
def termeniconditii(request):
    return render(request,"termeniconditii.html")
def politicaconfidentialitate(request):
    return render(request,"politicaconfidentialitate.html")
def freeaccount(request):
    mesaj = None
    if request.method == "POST":
        mesaj = {}
        email = request.POST.get('email')
        with sshtunnel.SSHTunnelForwarder(
                ('ssh.pythonanywhere.com'),
                ssh_username=settings.SSH_USER, ssh_password=settings.SSH_PASS,
                remote_bind_address=(settings.SSH_ADDRESS, 3306)
                ) as tunnel:
                    connection = MySQLdb.connect(
                        user=settings.MYSQL_USER,
                        passwd=settings.MYSQL_PASS,
                        host='127.0.0.1', port=tunnel.local_bind_port,
                        db=settings.MYSQL_DB,
                    )

                    cursor = connection.cursor()


                    emdata = cursor.execute(
                    'SELECT * FROM accs WHERE email = %s', (email,))
                    emdata = cursor.fetchall()
                    if len(emdata)>0:
                        msg = "Acestui email ii este atribuit deja un cont. Alege altul!"
                        mesaj["msj"]= msg
                    else:
                        S = 5
                        usern = ''.join(random.choices(string.ascii_lowercase + string.digits, k = S))
                        passd = ''.join(random.choices(string.ascii_lowercase + string.digits, k = S))
                        sqle = "INSERT INTO accs (username, passwd, email, conectat) VALUES (%s, %s, %s, 0)"
                        valy = (usern, passd, email)
                        cursor.execute(sqle, valy)
                        msg = EmailMessage('RouletteBOT - Contul tau a fost generat cu succes', f'<html><head></head><body>Aplicatia si fisierele ei sunt atasate in acest EMAIL. Citeste cu atentie instructiunile inainte de folosirea aplicatiei!<br>Link descarcare: https://ufile.io/ngn29yfz <br>Datele de logare pentru aplicatie:<br>Nume de utilizator: {usern}<br>Parola: {passd}<br>Datele contului pot fi schimbate din <strong>Contul meu><a href="https://www.roulettebot.ro/contuser/">Schimbare nume de utilizator</a> sau <a href="https://www.roulettebot.ro/contparola/">Schimbare parola</a></strong>. Aplicatia si instructiunile se afla intr-o arhiva si o puteti dezarhiva cu <a href="https://www.win-rar.com/predownload.html?&L=0">Winrar</a> sau orice alta aplicatie de dezarhivare. Intrati pe acest link in caz ca aveti probleme cu dezarhivarea <a href="https://www.youtube.com/watch?v=njweDaCGa0E">https://www.youtube.com/watch?v=njweDaCGa0E</a>. Pentru mai multe intrebari vizitati <a href="https://www.roulettebot.ro/faq/">Intrebari frecvente</a>.</body></html>', settings.EMAIL_HOST_USER, [email])
                        msg.content_subtype = "html"
                        msg.send()
                        msg = "Contul a fost generat cu succes! Verifica-ti mail-ul."
                        mesaj["msj"] = msg
                    cursor.close()
                    connection.commit()

    return render(request,"freeaccount.html", mesaj)
def contuser(request):
    errors = None
    if request.method == "POST":
        usernamenou = request.POST.get('usernamenou')
        usernamevechi = request.POST.get('usernamevechi')
        parola = request.POST.get('parola')
        errors = {}
        if usernamevechi == usernamenou:
            error = "Numele de utilizator nou nu poate fi acelasi ca cel vechi!"
            errors["eroare"] = error
        elif usernamevechi != usernamenou:
            with sshtunnel.SSHTunnelForwarder(
                ('ssh.pythonanywhere.com'),
                ssh_username=settings.SSH_USER, ssh_password=settings.SSH_PASS,
                remote_bind_address=(settings.SSH_ADDRESS, 3306)
                ) as tunnel:
                    connection = MySQLdb.connect(
                        user=settings.MYSQL_USER,
                        passwd=settings.MYSQL_PASS,
                        host='127.0.0.1', port=tunnel.local_bind_port,
                        db=settings.MYSQL_DB,
                    )

                    cursor = connection.cursor()


                    cdata = cursor.execute(
                    'SELECT * FROM accs WHERE username = %s', (usernamenou,))
                    cdata = cursor.fetchall()
                    if len(cdata)>0:
                        error = "Acest nume de utilizator este luat. Alege altul!"
                        errors["eroare"]= error
                    else:
                        xdata = cursor.execute(
                        'SELECT * FROM accs WHERE username = %s and passwd = %s', (usernamevechi,parola))
                        xdata = cursor.fetchall()
                        if len(xdata)>0:
                            if usernamevechi == xdata[0][1] and parola == xdata[0][2]:
                                #schimbam username
                                cursor.execute('UPDATE accs SET username=%s WHERE username = %s and passwd = %s',(usernamenou, usernamevechi, parola))
                                error = "Numele de utilizator a fost schimbat cu succes!"
                                errors["eroare"]= error
                        else:
                            error="Nume sau parola gresita."
                            errors["eroare"]= error
                    cursor.close()
                    connection.commit()

    return render(request,"contuser.html",errors)

def contparola(request):
    errors1 = None
    if request.method == "POST":
        username = request.POST.get('username')
        parolaveche = request.POST.get('parolaveche')
        parolanoua = request.POST.get('parolanoua')
        errors1 = {}
        if parolaveche == parolanoua:
            error1 = "Parola noua nu poate fi aceeasi ca cea veche!"
            errors1["eroare1"] = error1
        elif parolaveche != parolanoua:
            with sshtunnel.SSHTunnelForwarder(
                ('ssh.pythonanywhere.com'),
                ssh_username=settings.SSH_USER, ssh_password=settings.SSH_PASS,
                remote_bind_address=(settings.SSH_ADDRESS, 3306)
                ) as tunnel:
                    connection = MySQLdb.connect(
                        user=settings.MYSQL_USER,
                        passwd=settings.MYSQL_PASS,
                        host='127.0.0.1', port=tunnel.local_bind_port,
                        db=settings.MYSQL_DB,
                    )

                    cursor = connection.cursor()



                    ydata = cursor.execute(
                    'SELECT * FROM accs WHERE username = %s and passwd = %s', (username,parolaveche))
                    ydata = cursor.fetchall()
                    if len(ydata)>0:
                        if username == ydata[0][1] and parolaveche == ydata[0][2]:
                            #schimbam parola
                            cursor.execute('UPDATE accs SET passwd=%s WHERE username = %s and passwd = %s',(parolanoua, username, parolaveche))
                            error1 = "Parola a fost schimbata cu succes!"
                            errors1["eroare1"] = error1
                    else:
                        error1="Nume sau parola gresita."
                        errors1["eroare1"] = error1
                    cursor.close()
                    connection.commit()

    return render(request,"contparola.html",errors1)

def faq(request):
    return render(request,"faq.html")

def topjucatori(request):

    context ={}

    pointsdict = dataget()
    context = {
        'pointsdict':pointsdict
        }


    return render(request,"topjucatori.html", context)
def dataget():
    get_username=[]
    get_points=[]
    with sshtunnel.SSHTunnelForwarder(
                ('ssh.pythonanywhere.com'),
                ssh_username=settings.SSH_USER, ssh_password=settings.SSH_PASS,
                remote_bind_address=(settings.SSH_ADDRESS, 3306)
            ) as tunnel:
                connection = MySQLdb.connect(
                    user=settings.MYSQL_USER,
                    passwd=settings.MYSQL_PASS,
                    host='127.0.0.1', port=tunnel.local_bind_port,
                    db=settings.MYSQL_DB,
                )
                cursor = connection.cursor()
                data = cursor.execute(
                'SELECT * FROM accs ORDER BY pariuri_castigate DESC; ')
                data = cursor.fetchall()
                cursor.close()
                connection.commit()
    for i in range(0,10):
        get_username.append(data[i][1])
        get_points.append(data[i][5])
    zip_iterator = zip(get_username, get_points)
    user_dictionary = dict(zip_iterator)
    return user_dictionary


