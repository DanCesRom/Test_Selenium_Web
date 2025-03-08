# 🖥️ Automatización de Pruebas con Selenium y Pytest  

Este proyecto utiliza **Selenium** y **Pytest** para automatizar pruebas en un sitio web alojado en [`https://loupaws.pythonanywhere.com/`](https://loupaws.pythonanywhere.com/).  

## 📌 Descripción  
El script automatiza la autenticación, navegación y validación de formularios en el sitio web, asegurando su correcto funcionamiento mediante pruebas estructuradas.  

## 📂 Estructura del Proyecto  

📁 proyecto
│── 📄 Test_Selenium.py # Script principal con las pruebas
│── 📄 Selenium.py # Script principal con las acciones a tomar
│── 📄 requirements.txt # Dependencias del proyecto
│── 📄 README.md # Documentación del repositorio


## 🛠️ Tecnologías Utilizadas  
- **Python** (Lenguaje principal)  
- **Selenium** (Automatización del navegador)  
- **Pytest** (Ejecución y organización de pruebas)  

## 📌 Instalación y Configuración  

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   
2. **Crear un entorno virtual (Opcional pero recomendado)**
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3. **nstalar las dependencias**
pip install -r requirements.txt

4. **Configurar WebDriver**
Asegúrate de tener Microsoft Edge instalado y el WebDriver compatible. Puedes descargarlo desde:
Microsoft Edge WebDriver


🚀 Ejecución de las Pruebas
**Para ejecutar los tests, usa el siguiente comando:**
pytest Test_Selenium.py --html=reports/report.html --self-contained-html

Esto generará un reporte HTML en la carpeta reports/ con los resultados de las pruebas.

**✅ Resultados de las Pruebas**

Todas las pruebas han sido ejecutadas con éxito, validando:
- Acceso y autenticación en el sitio web.
- Navegación entre diferentes secciones.
- Verificación de cambios en la URL.
- Interacción con formularios.


