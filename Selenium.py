from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import time, random

base_url = "https://loupaws.pythonanywhere.com/"
newuser_url = base_url + "newuser"
owned_url = base_url + "owned"
addcard_url = base_url + "addcard"
logout_url = base_url + "logout"

user_admin = "51%2JDl%$6%K"
user_Auto_password = "CsF2ty9vjx@VHpbZq7"

# Configuración para Edge
def configurar_driver():
    edge_options = EdgeOptions()
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--log-level=3")  # Oculta mensajes en Edge
    return webdriver.Edge(options=edge_options)


# Función para navegar a una URL
def navegar_a_url(driver, url):
    driver.get(url)
    print(f"Navegando a: {url}")


# Función para esperar y llenar el campo de contraseña
def ingresar_contraseña(driver, contraseña):
    wait = WebDriverWait(driver, 10)
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    time.sleep(2)
    password_field.send_keys(contraseña)
    password_field.submit()
    print("Contraseña ingresada y formulario enviado.")


# Función para verificar cambio de URL
def esperar_cambio_url(driver, old_url):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_changes(old_url))
    print(f"Cambio de URL detectado: {driver.current_url}")


# Función para seleccionar opciones en los dropdowns y agregar un nombre en un campo de texto
def seleccionar_opciones(driver, set_value, type_value, rarity_value, card_name=None):
    wait = WebDriverWait(driver, 10)
    
    # 1. Esperar y seleccionar el valor para "set_name"
    set_dropdown = wait.until(EC.visibility_of_element_located((By.ID, "set_name")))
    time.sleep(0.5)  # Pausa breve antes de interactuar
    Select(set_dropdown).select_by_value(set_value)
    print(f"✔ Seleccionado: {set_value}")

    # 2. Esperar y seleccionar el valor para "type"
    type_dropdown = wait.until(EC.visibility_of_element_located((By.ID, "type")))
    time.sleep(0.5)
    Select(type_dropdown).select_by_value(type_value)
    print(f"✔ Seleccionado: {type_value}")

    # 3. Esperar y seleccionar el valor para "rarity"
    rarity_dropdown = wait.until(EC.visibility_of_element_located((By.ID, "rarity")))
    time.sleep(0.5)
    Select(rarity_dropdown).select_by_value(rarity_value)
    print(f"✔ Seleccionado: {rarity_value}")

    # 4. Si se proporciona un valor para el nombre de la carta, ingresarlo en el campo correspondiente
    if card_name:
        name_input = wait.until(EC.visibility_of_element_located((By.ID, "name")))
        time.sleep(0.5)
        name_input.clear()  # Limpiar el campo antes de ingresar el nuevo valor
        name_input.send_keys(card_name)  # Ingresar el nombre de la carta
        print(f"✔ Ingresado nombre de la carta: {card_name}")


# Función seleccionar cartas de manera aleatoria en los resultados mostrados.
def agregar_cartas_random(driver):
    wait = WebDriverWait(driver, 10)

    # Esperar a que las cartas se carguen en el contenedor
    wait.until(EC.visibility_of_element_located((By.ID, "cards-container")))

    # Obtener todas las cartas visibles
    cartas = driver.find_elements(By.CSS_SELECTOR, "#cards-container .card")

    if len(cartas) < 3:
        print("⚠ No hay suficientes cartas visibles para seleccionar 3.")
        return

    # Seleccionar 3 cartas aleatorias
    cartas_seleccionadas = random.sample(cartas, 3)

    for i, carta in enumerate(cartas_seleccionadas):
        # Hacer scroll hasta la carta seleccionada
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", carta)
        
        # Esperar un poco para asegurarse de que el scroll se haya realizado correctamente
        time.sleep(1)  # Aumentado el tiempo de espera para asegurar que la carta está completamente visible

        # Verificar si la carta está visible antes de interactuar con ella
        is_visible = False
        attempts = 0
        while not is_visible and attempts < 5:
            try:
                # Verificar si la carta es visible en la pantalla
                if carta.is_displayed():
                    is_visible = True
                else:
                    # Volver a hacer scroll si no está visible
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", carta)
                    time.sleep(0.5)
                attempts += 1
            except Exception as e:
                print(f"❌ Error verificando visibilidad de la carta: {str(e)}")
                break

        if not is_visible:
            print(f"⚠ Carta {i+1} no está visible después de varios intentos.")
            continue

        try:
            # Encontrar el input de cantidad dentro de la carta
            cantidad_input = carta.find_element(By.CSS_SELECTOR, ".quantity-input")

            # Cambiar el valor a 1
            cantidad_input.clear()
            cantidad_input.send_keys("1")
            print(f"✔ Carta {i+1} seleccionada y cantidad agregada: {carta.get_attribute('data-card-id')}")

        except Exception as e:
            print(f"❌ Error al agregar cantidad a una carta: {str(e)}")

        time.sleep(1)  # Espera antes de seleccionar la siguiente carta

# Función para seleccionar opciones en los dropdowns y agregar los valores en los campos de texto
def agregar_carta_seleccionar_opciones(driver, card_id, card_name, set_name, image_url, trend_price, quantity, regulation, type_value, rarity_value):
    wait = WebDriverWait(driver, 10)
    
    # 1. Esperar y llenar el campo "Card ID"
    id_input = wait.until(EC.visibility_of_element_located((By.ID, "id")))
    time.sleep(0.5)
    id_input.clear()  # Limpiar el campo antes de ingresar el nuevo valor
    id_input.send_keys(card_id)  # Ingresar el ID de la carta
    print(f"✔ Ingresado ID de la carta: {card_id}")

    # 2. Esperar y llenar el campo "Name"
    name_input = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    time.sleep(0.5)
    name_input.clear()  # Limpiar el campo antes de ingresar el nuevo valor
    name_input.send_keys(card_name)  # Ingresar el nombre de la carta
    print(f"✔ Ingresado nombre de la carta: {card_name}")

    # 3. Esperar y llenar el campo "Set Name"
    set_name_input = wait.until(EC.visibility_of_element_located((By.ID, "set_name")))
    time.sleep(0.5)
    set_name_input.clear()  # Limpiar el campo antes de ingresar el nuevo valor
    set_name_input.send_keys(set_name)  # Ingresar el nombre del set
    print(f"✔ Ingresado nombre del set: {set_name}")

    # 4. Esperar y llenar el campo "Image URL"
    image_url_input = wait.until(EC.visibility_of_element_located((By.ID, "image_url")))
    time.sleep(0.5)
    image_url_input.clear()  # Limpiar el campo antes de ingresar el nuevo valor
    image_url_input.send_keys(image_url)  # Ingresar la URL de la imagen
    print(f"✔ Ingresado URL de la imagen: {image_url}")

    # 5. Esperar y llenar el campo "Trend Price"
    trend_price_input = wait.until(EC.visibility_of_element_located((By.ID, "trend_price")))
    time.sleep(0.5)
    trend_price_input.clear()  # Limpiar el campo antes de ingresar el nuevo valor
    trend_price_input.send_keys(trend_price)  # Ingresar el precio de tendencia
    print(f"✔ Ingresado precio de tendencia: {trend_price}")

    # 6. Esperar y llenar el campo "Quantity"
    quantity_input = wait.until(EC.visibility_of_element_located((By.ID, "quantity")))
    time.sleep(0.5)
    quantity_input.clear()  # Limpiar el campo antes de ingresar el nuevo valor
    quantity_input.send_keys(quantity)  # Ingresar la cantidad
    print(f"✔ Ingresada cantidad: {quantity}")

    # 7. Esperar y llenar el campo "Regulation"
    regulation_input = wait.until(EC.visibility_of_element_located((By.ID, "regulation")))
    time.sleep(0.5)
    regulation_input.clear()  # Limpiar el campo antes de ingresar el nuevo valor
    regulation_input.send_keys(regulation)  # Ingresar la regulación
    print(f"✔ Ingresada regulación: {regulation}")

    # 8. Esperar y seleccionar el valor para "types"
    types_dropdown = wait.until(EC.visibility_of_element_located((By.ID, "types")))
    time.sleep(0.5)
    Select(types_dropdown).select_by_value(type_value)  # Seleccionar el tipo
    print(f"✔ Seleccionado tipo: {type_value}")

    # 9. Esperar y seleccionar el valor para "rarity"
    rarity_dropdown = wait.until(EC.visibility_of_element_located((By.ID, "rarity")))
    time.sleep(0.5)
    Select(rarity_dropdown).select_by_value(rarity_value)  # Seleccionar la rareza
    print(f"✔ Seleccionada rareza: {rarity_value}")

    # 10. Esperar y hacer clic en el botón "Add Card" (enviar el formulario)
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    submit_button.click()  # Hacer clic en el botón de enviar
    print("✔ Formulario enviado")
    time.sleep(1)
    
    # 11. Esperar a que la alerta sea visible y Aceptar la alerta (cerrarla)
    alert = Alert(driver)
    alert.accept()
    print("✔ Alerta Aceptada")


def encontrar_carta(driver):
    try:
        # Esperar hasta que el div con el card-id esté presente
        card_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.card[data-card-id="mbp-pre-074"]'))
        )
        # Si lo encuentra, imprime un mensaje
        print("Carta Agregada encontrada")
    except:
        # Si no encuentra el elemento, imprime un mensaje
        print("Carta Agregada no encontrada.")

def scroll_until_end_of_page(driver, scroll_pause_time=0.3, scroll_increment=100, max_scroll_attempts=10):
    """
    Slowly scroll down to the bottom of the page with smooth scrolling effect, accounting for lazy-loaded content.

    :param driver: The WebDriver instance.
    :param scroll_pause_time: Time to wait between each scroll to allow content to load (lower is faster).
    :param scroll_increment: The number of pixels to scroll per step (smaller numbers for smoother scrolling).
    :param max_scroll_attempts: The maximum number of scroll attempts before considering the end of the page.
    """
    # Get the current height of the page
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    attempts = 0

    while True:
        # Scroll down by a small increment for smooth scrolling
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")

        # Wait for the page to load (considering lazy loading of content)
        time.sleep(scroll_pause_time)

        # Get the new height of the page
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        # Check if we are still loading new content
        if new_height == last_height:
            attempts += 1
            if attempts >= max_scroll_attempts:
                # If we have tried several times and the height hasn't changed, assume we've reached the end
                break
        else:
            attempts = 0

        last_height = new_height

def scroll_to_top(driver):
    """
    Instantly scroll to the top of the page.

    :param driver: The WebDriver instance.
    """
    # Use JavaScript to scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")

def encontrar_y_hacer_click_en_clear(driver):
    try:
        # Esperar hasta que el botón con id 'clear-button' esté presente
        clear_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'clear-button'))
        )
        # Si lo encuentra, hace clic y muestra un mensaje
        clear_button.click()
        print("✔ Botón 'Clear Database' encontrado y clickeado")
    except:
        # Si no encuentra el botón, imprime un mensaje
        print("Botón 'Clear Database' no encontrado.")


# Función principal que ejecuta los pasos
def ejecutar_pruebas():
    driver = configurar_driver()
    
    try:
        # Paso 1: Navegar a la página principal
        navegar_a_url(driver, base_url)

        # Paso 2: Ingresar la contraseña
        ingresar_contraseña(driver, "51%2JDl%$6%K")

        # Paso 3: Esperar el cambio de URL tras enviar el formulario
        esperar_cambio_url(driver, base_url)
        time.sleep(2)

        # Paso 4: Navegar manualmente a /newuser
        navegar_a_url(driver, newuser_url)
        time.sleep(2)

        # Verificación de url
        if driver.current_url == newuser_url:
            print("Navegación exitosa a /newuser")
        else:
            print(f"No se llegó correctamente a /newuser. URL actual: {driver.current_url}")

        # Paso 4: Navegar manualmente a /newuser
        navegar_a_url(driver, logout_url)
        time.sleep(2)

        # Paso 5: Ingresar la contraseña nuevamente
        ingresar_contraseña(driver, "CsF2ty9vjx@VHpbZq7")
        time.sleep(3)

        # Paso 6: Navegar nuevamente a /newuser
        navegar_a_url(driver, newuser_url)
        time.sleep(2)

        # Verificación de url
        if driver.current_url == newuser_url:
            print("Navegación exitosa a /newuser")
        else:
            print(f"No se llegó correctamente a /newuser. URL actual: {driver.current_url}")

        # Paso 7: Ingresar la contraseña nuevamente
        ingresar_contraseña(driver, "CsF2ty9vjx@VHpbZq7")
        time.sleep(2)


        # Paso 8: Seleccionar opciones en los dropdowns y agregar un nombre a la carta (set, type, rarity, name)
        seleccionar_opciones(driver, "Prismatic Evolutions", "Supporter", "Full Art", "")
        time.sleep(1)


        # Paso 9: Seleccionar 3 cartas aleatorias y agregar cantidad
        agregar_cartas_random(driver)
        time.sleep(2)

        # Paso 10: Seleccionar opciones en los dropdowns y agregar un nombre a la carta (set, type, rarity, name)
        seleccionar_opciones(driver, "Surging Sparks", "Water", "Full Art", "")
        time.sleep(1)

        # Paso 11: Seleccionar 3 cartas aleatorias y agregar cantidad
        agregar_cartas_random(driver)
        time.sleep(2)

        # Paso 12: Seleccionar opciones en los dropdowns y agregar un nombre a la carta (set, type, rarity, name)
        seleccionar_opciones(driver, "Prismatic Evolutions", "All", "All", "Eevee")
        time.sleep(1)

        # Paso 13: Seleccionar 3 cartas aleatorias y agregar cantidad
        agregar_cartas_random(driver)
        time.sleep(2)

        # Paso 14: Navegar a la página de cartas salvadas y haces scroll hasta ver la ultima carta
        navegar_a_url(driver, owned_url)
        time.sleep(1)
        
        # Paso 15: Scroll hacia abajo para visualizar todas las cartas agregadas
        scroll_until_end_of_page(driver)
        time.sleep(2)
        #scroll_to_top(driver)
        time.sleep(2)

        # Paso 14: Navegar a la página de agregar carta faltantes en base de datos para la base de datos del usuario.
        navegar_a_url(driver, addcard_url)
        time.sleep(1)

        # Paso 15: Agregar y Registrar nueva carta 
        agregar_carta_seleccionar_opciones(
            driver, 
            card_id="mbp-pre-074",      # ID de la carta 
            card_name="Eevee",          # Nombre de la carta
            set_name="Prismatic Evolutions", # Nombre del set
            image_url="https://tcgplayer-cdn.tcgplayer.com/product/610691_in_1000x1000.jpg", # URL de la imagen
            trend_price="$39.82",       # Precio de mercado
            quantity="2",               # Cantidad de cartas
            regulation="H",             # Regulación
            type_value="Colorless",     # Tipo de carta
            rarity_value="Common"       # Rareza
         )
        time.sleep(3)

        # Paso 16: Navegar a cartas salvadas y Scroll hacia abajo para visualizar todas las cartas agregadas
        navegar_a_url(driver, owned_url)
        scroll_until_end_of_page(driver)
        time.sleep(2)
        

        # Paso 17: Scroll hacia arriba, Vaidar si la nueva carta fue agregada
        scroll_to_top(driver)
        encontrar_carta(driver)
        time.sleep(1)

        # Paso 18: Scroll hacia arriba, Vaidar si la nueva carta fue agregada
        encontrar_y_hacer_click_en_clear(driver)
        time.sleep(2)

    finally:
        driver.quit()
        print("Prueba finalizada y navegador cerrado.")

# Ejecutar la prueba
ejecutar_pruebas()
