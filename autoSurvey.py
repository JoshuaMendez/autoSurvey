from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import time
import pyotp

def generate_code(secret):
    secretKey = secret.replace(' ', '')
    return pyotp.TOTP(secretKey).now()

def login(username, password, secret_key, driver, temp_key):
    driver.get('https://mg-local.servicios.javerianacali.edu.co/')
    time.sleep(1)
    doble_factor_button = driver.find_element(By.CLASS_NAME, "img-doble-factor")
    doble_factor_button.click()
    time.sleep(1)
    username_input = driver.find_element(By.XPATH, "//input[@placeholder='Username']")
    username_input.send_keys(username)
    time.sleep(1)
    password_input = driver.find_element(By.XPATH, "//input[@type='password' and @autocomplete='do-not-save-password' and @name='not-password' and @id='password']")
    password_input.send_keys(password)
    time.sleep(1)
    iniciar_sesion = driver.find_element(By.XPATH, "//input[@type='submit' and @class='button button--submit' and @value='Iniciar sesión']")
    iniciar_sesion.click()
    time.sleep(1)

    # Generar el código y enviarlo
    fa = driver.find_element(By.ID, 'token')
    sk = secret_key
    if len(sk) > 0:
        sk = generate_code(secret_key)
    else:
        sk = temp_key
    fa.send_keys(sk)
    time.sleep(1)

    enviar = driver.find_element(By.XPATH, "//input[@type='submit' and @class='button button--submit ' and @value='Enviar']")
    enviar.click()

    # Espera a que la URL cambie para asegurarse de que el login fue exitoso
    WebDriverWait(driver, 10).until(EC.url_changes('https://mg-local.servicios.javerianacali.edu.co/'))

def evaluacion_docentes(calificacion, comment, driver):
    driver.get('https://valora.servicios.javerianacali.edu.co/EvaluacionDocenteEst/views/evaluacion/encuestasEstudiante.xhtml')
    
    while True:
        encuesta_links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-link')))
        
        if not encuesta_links:
                break

        encuesta_links[0].click()
        driver.switch_to.window(driver.window_handles[-1])  # Cambiar a la nueva ventana
        time.sleep(2)
        complete_survey(calificacion, comment, driver)
        driver.close()  # Cierra la ventana de la encuesta
        driver.switch_to.window(driver.window_handles[0])  # Regresa a la ventana original
        
        # Recargar la lista de encuestas
        driver.get('https://valora.servicios.javerianacali.edu.co/EvaluacionDocenteEst/views/evaluacion/encuestasEstudiante.xhtml')
        time.sleep(5)
        driver.refresh()

def complete_survey(calificacion, comment, driver):
    time.sleep(3)
    first_page(calificacion, driver)
    time.sleep(1)
    second_page(calificacion, comment, driver)
    time.sleep(1)
    third_page(calificacion, driver)
    time.sleep(1)
    fourth_page(calificacion, driver)
    time.sleep(1)

def first_page(calificacion, driver):
    radio_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mat-radio-button')))
    
    for opt in radio_buttons:
        sel = opt.find_element(By.CLASS_NAME, 'mat-form-field')
        if sel.text == str(calificacion):
            opt.click()
    
    siguiente = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(span/text(), 'Siguiente') and not(contains(@class, 'disabled'))]"))
    )
    siguiente.click()

def second_page(calificacion, comment, driver):
    radio_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mat-radio-button')))
    
    for opt in radio_buttons:
        sel = opt.find_element(By.CLASS_NAME, 'mat-form-field')
        if sel.text == str(calificacion):
            opt.click()
    
    textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='mat-input-0']")))
    textarea.send_keys(comment)

    siguiente = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(span/text(), 'Siguiente') and not(contains(@class, 'disabled'))]"))
    )
    siguiente.click()

def third_page(calificacion, driver):
    radio_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mat-radio-button')))
    
    for opt in radio_buttons:
        sel = opt.find_element(By.CLASS_NAME, 'mat-form-field')
        if sel.text == str(calificacion):
            opt.click()

    siguiente = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(span/text(), 'Siguiente') and not(contains(@class, 'disabled'))]"))
    )
    siguiente.click()

def fourth_page(calificacion, driver):
    radio_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mat-radio-button')))
    
    for opt in radio_buttons:
        sel = opt.find_element(By.CLASS_NAME, 'mat-form-field')
        if sel.text == str(calificacion):
            opt.click()
    
    guardar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(span/text(), 'Guardar') and not(contains(@class, 'disabled'))]"))
    )
    guardar.click()

def toggle_password():
    if passw.cget('show') == '':
        passw.config(show='*')  # Oculta la contraseña
        ojo_button.config(text='👁️')  # Cambia el ícono
    else:
        passw.config(show='')  # Muestra la contraseña
        ojo_button.config(text='👁️*')  # Cambia el ícono

def main():
    tab = tk.Tk()
    tab.title("AutoSurvey")
    tab.geometry("300x350")
    tk.Label(tab, text="Username").pack()
    user = tk.Entry(tab, width=30)
    user.pack()
    tk.Label(tab, text="Password").pack()
    pass_frame = tk.Frame(tab)  # Un frame para colocar la contraseña y el botón de mostrar
    pass_frame.pack()
    global passw, ojo_button
    passw = tk.Entry(pass_frame, show='*', width=25)  # Oculta la contraseña por defecto
    passw.pack(side='left')
    
    ojo_button = tk.Button(pass_frame, text='👁️', command=toggle_password)
    ojo_button.pack(side='left')
    
    # opcion = tk.StringVar(value="secret")  # Valor por defecto
    # tk.Radiobutton(tab, text="Usar Secret Key", variable=opcion, value="secret", command=habilitar_campo).pack()
    # tk.Radiobutton(tab, text="Usar Temp Key", variable=opcion, value="temp", command=habilitar_campo).pack()

    tk.Label(tab, text="Secret Key").pack()
    secret = tk.Entry(tab, width=30)
    secret.pack()
    tk.Label(tab, text="Temp Key").pack()
    tempKey = tk.Entry(tab, width=30)
    tempKey.pack()
    tk.Label(tab, text="Calificacion").pack()
    calif = tk.Scale(tab, from_=1, to=5, orient=tk.HORIZONTAL)
    calif.pack()
    tk.Label(tab, text="Comentario").pack()
    comment = tk.Text(tab, height=3, width=30)
    comment.pack()
    boton = tk.Button(tab, text="Iniciar", command=tab.quit)
    boton.configure(bg="blue", fg="white")
    boton.pack()
    tk.Label(tab, text="Made by LaRata", font=("Helvetica", 8, "italic")).pack()
    tab.mainloop()
    username = user.get()
    password = passw.get()
    secret_key = secret.get()
    temp_key = tempKey.get()
    comment = comment.get("1.0", tk.END).strip()
    calificacion = calif.get()

    driver = webdriver.Chrome()
    login(username, password, secret_key, driver, temp_key)
    evaluacion_docentes(calificacion, comment, driver)
    driver.quit()

main()