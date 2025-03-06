import customtkinter as ctk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import subprocess
import os
import base64
import tempfile
import shutil

def select_bat_file():
    filename = filedialog.askopenfilename(
        title="Selecciona el archivo .bat",
        filetypes=[("Archivos BAT", "*.bat")]
    )
    bat_entry.delete(0, ctk.END)
    bat_entry.insert(0, filename)

def select_icon_file():
    filename = filedialog.askopenfilename(
        title="Selecciona el archivo de icono (.ico o .png)",
        filetypes=[("Archivos de icono", "*.ico *.png")]
    )
    icon_entry.delete(0, ctk.END)
    icon_entry.insert(0, filename)

def convert_bat_to_exe():
    bat_path = bat_entry.get()
    icon_path = icon_entry.get()

    if not bat_path or not os.path.isfile(bat_path):
        messagebox.showerror("Error", "Por favor, selecciona un archivo .bat válido.")
        return

    try:
        with open(bat_path, "r", encoding="utf-8") as f:
            bat_content = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer el archivo .bat: {e}")
        return

    generated_code = f'''import subprocess, tempfile, os
bat_content = {repr(bat_content)}
with tempfile.NamedTemporaryFile(delete=False, suffix=".bat", mode="w", encoding="utf-8") as f:
    f.write(bat_content)
bat_file = f.name
subprocess.call(bat_file, shell=True)
os.remove(bat_file)
'''

    encoded_code = base64.b64encode(generated_code.encode("utf-8")).decode("utf-8")
    wrapper_code = f'''import base64
exec(base64.b64decode("{encoded_code}"))
'''

    temp_dir = tempfile.mkdtemp()
    script_path = os.path.join(temp_dir, "generated_script.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(wrapper_code)

    messagebox.showinfo("Proceso", "Iniciando conversión. Esto puede tardar unos minutos.")

    cmd = ["pyinstaller", "--onefile", script_path, "--name", "TareasU_MX_Converter"]
    if icon_path and os.path.isfile(icon_path):
        cmd.extend(["--icon", icon_path])
    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Éxito", "La conversión se completó exitosamente.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error en la conversión: {e}")
    finally:
        shutil.rmtree(temp_dir)

    dist_folder = os.path.join(os.getcwd(), "dist")
    exe_path = os.path.join(dist_folder, "TareasU_MX_Converter.exe")
    if os.path.exists(exe_path):
        guide_path = os.path.join(dist_folder, "Guia_de_usuario.txt")
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write("Guía de usuario para Tareas U. MX Converter\n")
            f.write("1. Ejecuta el archivo .exe generado para correr el programa.\n")
            f.write("2. Sigue las instrucciones en pantalla para realizar la conversión de tus archivos .bat.\n")
            f.write("Tareas U. MX. 2025\n")
        messagebox.showinfo("Guía creada", f"La guía de usuario se creó en: {guide_path}")

def change_mode(choice):
    ctk.set_appearance_mode(choice)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Tareas U. MX. facebook.com/trabajosunimx")
app.geometry("700x400")
app.resizable(True, True)

messagebox.showinfo("Bienvenido", "Creado por Tareas U. MX. facebook.com/trabajosunimx")

font_style = ("Ubuntu", 14)

scroll_frame = ctk.CTkScrollableFrame(
    master=app,
    width=680,
    height=300
)
scroll_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

bat_label = ctk.CTkLabel(scroll_frame, text="Archivo .bat:", font=font_style)
bat_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

bat_entry = ctk.CTkEntry(scroll_frame, width=400, font=font_style)
bat_entry.grid(row=0, column=1, padx=10, pady=10)

bat_button = ctk.CTkButton(scroll_frame, text="Seleccionar", command=select_bat_file, font=font_style)
bat_button.grid(row=0, column=2, padx=10, pady=10)

icon_label = ctk.CTkLabel(scroll_frame, text="Icono (.ico o .png):", font=font_style)
icon_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

icon_entry = ctk.CTkEntry(scroll_frame, width=400, font=font_style)
icon_entry.grid(row=1, column=1, padx=10, pady=10)

icon_button = ctk.CTkButton(scroll_frame, text="Seleccionar", command=select_icon_file, font=font_style)
icon_button.grid(row=1, column=2, padx=10, pady=10)

convert_button = ctk.CTkButton(scroll_frame, text="Convertir a .exe", command=convert_bat_to_exe, font=font_style)
convert_button.grid(row=2, column=1, padx=10, pady=20)

mode_label = ctk.CTkLabel(scroll_frame, text="Modo de apariencia:", font=font_style)
mode_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

mode_option = ctk.CTkOptionMenu(scroll_frame, values=["light", "dark", "system"], command=change_mode)
mode_option.grid(row=3, column=1, padx=10, pady=10)
mode_option.set("dark")

app.mainloop()
