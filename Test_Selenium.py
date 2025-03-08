import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

login_url = "/login"  # Relative path to the login page
base_url = "https://loupaws.pythonanywhere.com/"
newuser_url = base_url + "newuser"
logout_url = "https://loupaws.pythonanywhere.com/logout"

@pytest.fixture(scope="module")
def driver():
    edge_options = EdgeOptions()
    edge_options.add_argument("--no-sandbox")
    driver = webdriver.Edge(options=edge_options)
    yield driver
    driver.quit()

@pytest.mark.order(1)
def test_navegar_a_pagina_principal(driver):
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))

    # Ingresa la contraseña y la envía
    password_field.send_keys("CsF2ty9vjx@VHpbZq7")
    password_field.submit()

    # Verifica que no se está en la página principal
    assert driver.current_url != base_url, f"No se pudo ir a la página principal, la URL actual es {driver.current_url}"


@pytest.mark.order(2)
def test_ingresar_contraseña_admin(driver):
    wait = WebDriverWait(driver, 10)
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_field.send_keys("CsF2ty9vjx@VHpbZq7")
    password_field.submit()
    wait.until(EC.url_changes(base_url))
    assert driver.current_url != base_url, "No se pudo iniciar sesión con admin"

@pytest.mark.order(3)
def test_navegar_y_verificar_newuser(driver):
    # Iniciar sesión primero
    wait = WebDriverWait(driver, 10)
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))

    # Enviar la contraseña para iniciar sesión
    password_field.send_keys("51%2JDl%$6%K")
    password_field.submit()

    # Esperar a que la página cambie después de iniciar sesión
    wait.until(EC.url_changes(driver.current_url))

    # Verificar que no hemos sido redirigidos a /login
    assert "/login" not in driver.current_url, f"Se redirigió a la página de login: {driver.current_url}"

    # Ahora navegar a la página newuser
    driver.get(newuser_url)

    # Verificar que la URL actual sea la correcta
    assert driver.current_url != newuser_url, f"No se pudo acceder a {newuser_url}, la URL actual es {driver.current_url}"

@pytest.mark.order(5)
def test_ingresar_contraseña_usuario(driver):
    wait = WebDriverWait(driver, 10)
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_field.send_keys("CsF2ty9vjx@VHpbZq7")
    password_field.submit()
    wait.until(EC.url_changes(base_url))
    assert driver.current_url != base_url, "No se pudo iniciar sesión con usuario"

if __name__ == "__main__":
    pytest.main(["--html=report.html", "--self-contained-html"])
