import speech_recognition as sr
import subprocess as sub
from tkinter import *
from PIL import ImageTk, Image, ImageSequence
import pyttsx3
import pywhatkit
import wikipedia
import datetime, time
import keyboard
import cam
import os
import threading as tr
from pygame import mixer
# Inicialización de pyttsx3
name = "juanita"
listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 145)
voices = engine.getProperty('voices')
# Declaración de los elementos de la ventana principal
main_window = Tk()
main_window.title("Juanita AI")
main_window.geometry("800x450")
main_window.configure(bg="#0082c8")
main_window.resizable(0, 0)
#Texto a mostrar de comandos 
comandos = """ 
    Comandos que puedes usar:
    - Reproduce..(canción)
    - Busca...(algo)
    - Abre...(página web o app)
    - Alarma..(hora en 24H)
    - Archivo...(nombre)
    - Colores (rojo, azul, amarillo)
    - Termina
"""
# Label del título y foto de Juanita
label_name = Label(main_window, text="Juanita AI", fg="#203A43", bg="#36D1DC",
                   font=('Arial', 35, 'bold')).pack(pady=10)
juanita_photo = ImageTk.PhotoImage(Image.open("juanita_photo.jpg"))
back_photo = Label(main_window, image=juanita_photo).pack(pady=10)
# Canvas en dónde se ubicarán los comandos
canvas = Canvas(bg="#0575E6", height=450, width=200)
canvas.place(x=0, y=0)
canvas.create_text(90, 80, text=comandos, fill='white', font='Arial 11')
# Texto en dónde se mostrará información de Wikipedia
text_info = Text(main_window, bg="#0575E6", fg="white")
text_info.place(x=0, y=175, height=350, width=200)
# Función de hablar
def talk(text):
    engine.say(text)
    engine.runAndWait()
    text_info.delete('1.0', 'end')
# Ventana en donde se pide el nombre del usuario
def give_name():
    global name_entry
    name_window = Toplevel()
    name_window.title("¿Cómo te llamas?")
    name_window.geometry('350x100')
    name_window.configure(bg="#434343")
    name_window.resizable(0,0)
    title_label = Label(name_window, text="¿Cómo te llamas?", fg="white", bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    name_entry = Entry(name_window, width=25)
    name_entry.pack(pady=1)
    button_save = Button(name_window, text="Guardar", bg='#16222A', fg="white", width=8, height=1, command=save_name).pack(pady=2)
def thread_give_name():
    t = tr.Thread(target=give_name)
    t.start()
# Función para guardar el nombre en una archivo txt
def save_name():
    name_user = name_entry.get()
    talk(f"Bienvenido {name_user}!")
    try:
        with open("nombre.txt", 'w') as f:
            f.write(name_user)
    except FileNotFoundError as e:
        file = open("nombre.txt", 'w')
        file.write(name_user)
# Función en donde Juanita saluda al usuario
def say_hello():
    try:
        with open("nombre.txt") as f:
            for name in f:
                talk(f"Hola {name}, bienvenido!")
    except FileNotFoundError as e:
        talk("Hola, ¿cómo te llamas?")
#Función que saluda con hilos
def thread_hello():
    t = tr.Thread(target=say_hello)
    t.start()
# Función que verifica si el usuario ha guardado su nombre
def check_name_window():    
    try:
        with open("nombre.txt") as f:
            pass
    except FileNotFoundError as e:
        thread_give_name()
# Invocación de la ventana del nombre y el saludo
check_name_window()
thread_hello()
# Funciones de cambio de voz
def mexican_voice():
    change_voice(0)
def spanish_voice():
    change_voice(1)
def english_voice():
    change_voice(2)
def change_voice(pos):
    engine.setProperty('voice', voices[pos].id)
    engine.setProperty('rate', 145)
    talk("Hola, soy Juanita!")
# Diccionarios para abrir apps, páginas web y archivos
def charge_data(dict, filed):
    try:
        with open(filed) as f:
            for line in f:
                (key,val) = line.split(",")
                val = val.rstrip("\n")
                dict[key] = val
    except FileNotFoundError as e:
        pass
sites = dict()
charge_data(sites, "sitios.txt")    
files = dict()
charge_data(files, "archivos.txt") 
programs = dict()
charge_data(programs, "apps.txt")
# Funciones de escuchar, escribir y leer
def read_talk():
    text = text_info.get("1.0", "end")
    talk(text)
def write_text(textc):
    text_info.insert(INSERT, textc)    
def listen():
    try:
        with sr.Microphone() as source:
            talk("Te escucho")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except:
        pass
    return rec
# Función principal de Juanita
def run_juanita():    
    while True:
        rec = listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca'in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            talk(wiki)
            write_text(search + ": " + wiki)
            break
        elif 'alarma' in rec:
            ta = tr.Thread(target=clock, args=(rec,))
            ta.start()
        elif 'colores' in rec:
            talk("Enseguida")
            t = tr.Thread(target=cam.capture)
            t.start()
        elif 'abre' in rec:
            task = rec.replace('abre', '')
            task = task.strip()
            if task in sites:
                for task in sites:             
                    if task in rec:
                        sub.call(f'start chrome.exe {sites[task]}', shell=True)
                        talk(f'Abriendo {task}')
            elif task in programs:      
                for task in programs:                
                    if task in rec:
                        talk(f'Abriendo {task}')
                        os.startfile(programs[task])
            else:
                talk("Parece que esa página o app no está agregada, usa los botones de agregar!")
        elif 'archivo' in rec:
            file = rec.replace('archivo', '')
            file = file.strip()
            if file in files:
                for file in files:
                    if file in rec:
                        sub.Popen([files[file]], shell=True)
                        talk(f'Abriendo {file}')
            else:
                talk("Parece que ese archivo no lo tienes agregado, usa el botón de agregar!")
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)
            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)
        elif 'cierra' in rec:
            for task in programs:
                if task in rec:
                    kill_task = programs[task].split("\\")
                    kill_task = kill_task[-1]
                    sub.call(f'taskkill /IM {kill_task} /F', shell=True)
                    talk(f"Cerrando {task}")
        elif 'ciérrate' in rec:
            talk("Adios!")
            sub.call('taskkill /IM python.exe /F', shell=True)
        elif 'termina' in rec:
            talk('Adios!')
            break
# Función para escribir una nota en un archivo
def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)
# Función del despertador (esto para usar hilos)
def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            mixer.init()
            mixer.music.load("auronplay-alarma.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break
# Función para detener el despertador
def stop_music():
    mixer.music.stop()
# Ventanas para agregar cosas
def open_file_window():
    global namef_entry, rutef_entry
    file_win = Toplevel()
    file_win.title("Agregar archivos")
    file_win.geometry('300x200')
    file_win.configure(bg="#434343")
    file_win.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(file_win)} center')
    title_label = Label(file_win, text="Agrega un archivo", fg="white", bg="#434343", font=('Arial', 15, 'bold')).pack(pady=3)
    text_name = Label(file_win, text="Nombre del archivo", fg="white", bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    namef_entry = Entry(file_win)
    namef_entry.pack(pady=1)
    text_rute = Label(file_win, text="Ruta del archivo", fg="white", bg="#434343",font=('Arial', 10, 'bold')).pack(pady=2)
    rutef_entry = Entry(file_win, width=30)
    rutef_entry.pack(pady=1)
    button_add = Button(file_win, text="Agregar", bg='#16222A', fg="white", width=8, height=1, command=add_files).pack(pady=5)
def open_page_window():
    global namep_entry, rutep_entry
    file_win = Toplevel()
    file_win.title("Agregar páginas")
    file_win.geometry('300x200')
    file_win.configure(bg="#434343")
    file_win.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(file_win)} center')
    title_label = Label(file_win, text="Agrega una página web", fg="white", bg="#434343", font=('Arial', 15, 'bold')).pack(pady=3)
    text_name = Label(file_win, text="Nombre de la página", fg="white", bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    namep_entry = Entry(file_win)
    namep_entry.pack(pady=1)
    text_rute = Label(file_win, text="URL de la página", fg="white", bg="#434343",font=('Arial', 10, 'bold')).pack(pady=2)
    rutep_entry = Entry(file_win, width=30)
    rutep_entry.pack(pady=1)
    button_add = Button(file_win, text="Agregar", bg='#16222A', fg="white", width=8, height=1, command=add_sites).pack(pady=5)
def open_app_window():
    global namea_entry, rutea_entry
    file_win = Toplevel()
    file_win.title("Agregar apps")
    file_win.geometry('300x200')
    file_win.configure(bg="#434343")
    file_win.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(file_win)} center')
    title_label = Label(file_win, text="Agrega una app", fg="white", bg="#434343", font=('Arial', 15, 'bold')).pack(pady=3)
    text_name = Label(file_win, text="Nombre de la app", fg="white", bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    namea_entry = Entry(file_win)
    namea_entry.pack(pady=1)
    text_rute = Label(file_win, text="Ruta de la app", fg="white", bg="#434343",font=('Arial', 10, 'bold')).pack(pady=2)
    rutea_entry = Entry(file_win,width=30)
    rutea_entry.pack(pady=1)
    button_add = Button(file_win, text="Agregar", bg='#16222A', fg="white", width=8, height=1, command=add_apps).pack(pady=5)
# Funciones para agregar cosas a los diccionarios
def add_files():
    namef = namef_entry.get()
    rutef = rutef_entry.get()
    files[namef] = rutef
    save_files("archivos.txt", namef, rutef)
    namef_entry.delete(0, "end")
    rutef_entry.delete(0, "end")
def add_sites():
    namep = namep_entry.get()
    rutep = rutep_entry.get()
    sites[namep] = rutep
    save_files("sitios.txt", namep, rutep)
    namep_entry.delete(0, "end")
    rutep_entry.delete(0, "end")
def add_apps():
    namea = namea_entry.get()
    rutea = rutea_entry.get()
    programs[namea] = rutea
    save_files("apps.txt", namea, rutea)
    namea_entry.delete(0, "end")
    rutea_entry.delete(0, "end")
def save_files(file, name, route):
    try:
        with open(file, 'a') as f:
            f.write(name + "," + route + "\n")
    except FileNotFoundError as e:
        file = open(file, 'a')
        file.write(name + "," + route + "\n")
# Función para que Juanita diga que cosas ha guardado el usuario
def talk_files():
    if bool(files) == True:
        talk("Has agregado los siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("Aún no has agregado archivos!")
def talk_sites():
    if bool(sites) == True:
        talk("Has agregado los siguientes sitios web!")
        for site in sites:
            talk(site)
    else:
        talk("Aún no has agregado sitios web!")
def talk_apps():
    if bool(programs) == True:
        talk("Has agregado las siguientes aplicaciones")
        for app in programs:
            talk(app)
    else:
        talk("Aún no has agregado aplicaciones!")
# Botones main_window
button_voice1 = Button(main_window, text="Voz México", bg='#0f9b0f', fg="white", font=('Arial', 10, 'bold'), command=mexican_voice) \
    .place(x=645, y=90, height=30, width=100)
button_voice2 = Button(main_window, text="Voz España", bg='#FF0000', fg="white", font=('Arial', 10, 'bold'), command=spanish_voice) \
    .place(x=645, y=125, height=30, width=100)
button_voice3 = Button(main_window, text="Voz USA", bg='#0575E6', fg="white", font=('Arial', 10, 'bold'), command=english_voice) \
    .place(x=645, y=160, height=30, width=100)
button_speak = Button(main_window, text="Hablar", bg='#b6fbff', fg="black", font=('Arial', 10, 'bold'), command=read_talk) \
    .place(x=645, y=195, height=30, width=100)
button_stop = Button(main_window, text="Deten alarma", bg='#b6fbff', fg="black", font=('Arial', 10, 'bold'), command=stop_music) \
    .place(x=645, y=230, height=30, width=100)
button_files = Button(main_window, text="Agregar archivos", bg='#16222A', fg="white", font=('Arial', 10, 'bold'), command=open_file_window) \
    .place(x=630, y=300, height=30, width=130)
button_web = Button(main_window, text="Agregar páginas", bg='#16222A', fg="white", font=('Arial', 10, 'bold'), command=open_page_window) \
    .place(x=630, y=335, height=30, width=130)
button_apps = Button(main_window, text="Agregar apps", bg='#16222A', fg="white", font=('Arial', 10, 'bold'), command=open_app_window) \
    .place(x=630, y=370, height=30, width=130)
button_listen = Button(main_window, text="Escuchar", bg='#b6fbff', fg="black", height=2, width=30, font=('Arial', 10, 'bold'), command= run_juanita)
button_listen.pack(pady=10)
button_add_f = Button(main_window, text="Archivos agregados", bg='#16222A', fg="white", font=('Arial', 7, 'bold'), command=talk_files) \
    .place(x=235, y=400, height=30, width=100)
button_add_p = Button(main_window, text="Páginas agregadas", bg='#16222A', fg="white", font=('Arial', 7, 'bold'), command=talk_sites) \
    .place(x=355, y=400, height=30, width=100)
button_add_a = Button(main_window, text="Apps agregadas", bg='#16222A', fg="white", font=('Arial', 7, 'bold'), command=talk_apps) \
    .place(x=475, y=400, height=30, width=100)
# Ejecución de mainloop()
main_window.mainloop()
