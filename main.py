import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import logging
import yaml
import sys
import time
import random
import undetected_chromedriver as udc

load_dotenv()

logging.basicConfig(
    format="%(levelname)s:%(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("/tmp/out.log"), logging.StreamHandler(sys.stdout)],
)


class Prenota:
    @staticmethod
    def check_file_exists(file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        return os.path.isfile(file_path)

    @staticmethod
    def load_config(file_path):
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    @staticmethod
    def check_for_dialog(driver):
        """Verifica se há diálogo de 'não disponível'"""
        try:
            dialog = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            button_inside_dialog = dialog.find_element(
                By.XPATH, "//button[contains(text(),'ok')]"
            )
            button_inside_dialog.click()
            logging.info(
                f"Timestamp: {str(datetime.now())} - Scheduling is not available right now."
            )
            return True
        except NoSuchElementException:
            logging.info(
                f"Timestamp: {str(datetime.now())} - Slot available. Filling forms..."
            )
            return False

    @staticmethod
    def fill_passport_form(driver, user_config):
        """Preenche o formulário de primeiro passaporte"""
        try:
            time.sleep(10)
            driver.get("https://prenotami.esteri.it/Services/Booking/1319")
            time.sleep(5)

            if not Prenota.check_for_dialog(driver):
                logging.info(f"Timestamp: {str(datetime.now())} - Filling passport form...")
                
                # Salva HTML para debug
                with open("files/passport_form.html", "w") as f:
                    f.write(driver.page_source)

                # Pergunta 1: Você possui passaporte expirado?
                try:
                    q0 = Select(driver.find_element(By.ID, "ddls_0"))
                    q0.select_by_visible_text(user_config.get("possess_expired_passport", "Não"))
                    logging.info("✓ Q1 filled: Possess expired passport")
                except Exception as e:
                    logging.warning(f"Warning filling Q1: {e}")

                # Pergunta 2: Está em posse de passaporte?
                try:
                    q1 = Select(driver.find_element(By.ID, "ddls_1"))
                    q1.select_by_visible_text(user_config.get("possess_expired_passport", "Não"))
                    logging.info("✓ Q2 filled: In possession of passport")
                except Exception as e:
                    logging.warning(f"Warning filling Q2: {e}")

                # Campo 3: Total de filhos
                try:
                    q2 = driver.find_element(By.ID, "DatiAddizionaliPrenotante_2___testo")
                    q2.send_keys(str(user_config.get("total_children", "0")))
                    logging.info("✓ Q3 filled: Total children")
                except Exception as e:
                    logging.warning(f"Warning filling Q3: {e}")

                # Campo 4: Endereço completo
                try:
                    q3 = driver.find_element(By.ID, "DatiAddizionaliPrenotante_3___testo")
                    q3.clear()
                    q3.send_keys(user_config.get("full_address", ""))
                    logging.info("✓ Q4 filled: Full address")
                except Exception as e:
                    logging.warning(f"Warning filling Q4: {e}")

                # Pergunta 5: Estado civil
                try:
                    q4 = Select(driver.find_element(By.ID, "ddls_4"))
                    q4.select_by_visible_text(user_config.get("marital_status", "Solteiro"))
                    logging.info("✓ Q5 filled: Marital status")
                except Exception as e:
                    logging.warning(f"Warning filling Q5: {e}")

                time.sleep(1)

                # Upload arquivo de identidade
                try:
                    file0 = driver.find_element(By.XPATH, '//*[@id="File_0"]')
                    file0.send_keys(os.getcwd() + "/files/identidade.pdf")
                    logging.info("✓ Identity document uploaded")
                except Exception as e:
                    logging.warning(f"Warning uploading identity: {e}")

                time.sleep(1)

                # Upload arquivo de residência
                try:
                    file1 = driver.find_element(By.XPATH, '//*[@id="File_1"]')
                    file1.send_keys(os.getcwd() + "/files/residencia.pdf")
                    logging.info("✓ Residency document uploaded")
                except Exception as e:
                    logging.warning(f"Warning uploading residency: {e}")

                # Aceitar termos de privacidade
                try:
                    checkBox = driver.find_element(By.ID, "PrivacyCheck")
                    checkBox.click()
                    logging.info("✓ Privacy terms accepted")
                except Exception as e:
                    logging.warning(f"Warning accepting privacy: {e}")

                # Submeter formulário
                try:
                    form_submit = driver.find_element(By.ID, "btnAvanti")
                    form_submit.click()
                    logging.info("✓ Form submitted")
                    return True
                except Exception as e:
                    logging.warning(f"Warning submitting form: {e}")
                    return False
        except Exception as e:
            logging.info(f"Exception in fill_passport_form: {e}")
            return False

    @staticmethod
    def fill_citizenship_form(driver, user_config):
        """Preenche o formulário de cidadania"""
        try:
            driver.get("https://prenotami.esteri.it/Services/Booking/2392")
            time.sleep(6)
            if not Prenota.check_for_dialog(driver):
                logging.info(f"Timestamp: {str(datetime.now())} - Filling citizenship form...")
                
                file_location = os.path.join("files/residencia.pdf")
                choose_file = driver.find_elements(By.ID, "File_0")
                choose_file[0].send_keys(file_location)
                
                privacy_check = driver.find_elements(By.ID, "PrivacyCheck")
                privacy_check[0].click()
                
                submit = driver.find_elements(By.ID, "btnAvanti")
                submit[0].click()
                
                with open("files/citizenship_form.html", "w") as f:
                    f.write(driver.page_source)
                return True
        except Exception as e:
            logging.info(f"Exception: {e}")
            return False

    @staticmethod
    def run():
        """Função principal"""
        if not Prenota.check_file_exists("files/residencia.pdf"):
            logging.error(
                "Required files are not available. Check the required files in README.md file. Ending execution."
            )
            sys.exit(0)

        logging.info(f"Timestamp: {str(datetime.now())} - Required files available.")
        
        email = os.getenv("USERNAME") or os.getenv("username")
        password = os.getenv("PASSWORD") or os.getenv("password")
        
        if not email or not password:
            logging.error("USERNAME and PASSWORD environment variables are required in .env file")
            sys.exit(1)
        
        user_config = Prenota.load_config("parameters.yaml")
        logging.info(f"Loaded config for: {user_config.get('full_name', 'Unknown')}")
        
        options = udc.ChromeOptions()
        options.headless = False
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        driver = udc.Chrome(use_subprocess=True, options=options)
        driver.delete_all_cookies()

        try:
            logging.info(f"Timestamp: {str(datetime.now())} - Starting login process...")
            driver.get("https://prenotami.esteri.it/")
            
            email_box = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "login-email"))
            )
            password_box = driver.find_element(By.ID, "login-password")
            
            email_box.send_keys(email)
            password_box.send_keys(password)
            time.sleep(4)
            
            # Clica no botão de login (com reCAPTCHA)
            button = driver.find_elements(
                By.XPATH, "//button[contains(@class,'button primary g-recaptcha')]"
            )
            if button:
                button[0].click()
                logging.info(f"Timestamp: {str(datetime.now())} - Login button clicked.")
            
            logging.info(f"Timestamp: {str(datetime.now())} - Successfully logged in.")
            time.sleep(10)
        except Exception as e:
            logging.error(f"Exception during login: {e}")
            driver.quit()
            return

        # Tenta preencher o formulário múltiplas vezes
        for i in range(200):
            random_number = random.randint(1, 5)
            logging.info(f"Attempt {i+1}/200")

            if user_config["request_type"] == "citizenship":
                if Prenota.fill_citizenship_form(driver, user_config):
                    break
            elif user_config["request_type"] == "passport":
                if Prenota.fill_passport_form(driver, user_config):
                    break

            time.sleep(random_number)

        # Aguarda por entrada manual do usuário
        user_input = input(
            f"Timestamp: {str(datetime.now())} - Go ahead and fill manually the rest of the process. "
            f"When finished, type 'quit' to exit the program and close the browser: "
        )
        while True:
            if user_input.lower() == "quit":
                driver.quit()
                logging.info("Browser closed. Program exiting.")
                break
            user_input = input("Type 'quit' to exit: ")


if __name__ == "__main__":
    try:
        Prenota.run()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
