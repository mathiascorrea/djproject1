from django.test import TestCase

# Create your tests here.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException 
 
class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    #fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        #creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()


    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()

    def test_staff_permissions(self):
            #Test para crear un usuario staff y verificar permisos

        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
 
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
 
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # Ir a la página de creación de usuarios
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/auth/user/add/'))

        # Rellenar datos del usuario
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('staffuser')
        password_input = self.selenium.find_element(By.NAME,"password1")
        password_input.send_keys('pirineus')
        password_input = self.selenium.find_element(By.NAME,"password2")
        password_input.send_keys('pirineus')
        #self.selenium.find_element(By.NAME, "_save").click() 
        self.selenium.find_element(By.XPATH,'//input[@value="Save and continue editing"]').click()
        #self.selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Editar permisos del usuario (convertirlo en staff)
        #self.selenium.get('%s%s' % (self.live_server_url, '/admin/auth/user/'))
        self.selenium.find_element(By.LINK_TEXT, "staffuser").click()
        self.selenium.find_element(By.NAME, "is_staff").click()  # Activar staff

        # Asignar permisos de Questions
        self.selenium.find_element(By.ID, "id_user_permissions_add_all_link").click()
        self.selenium.find_element(By.NAME, "_save").click()

        # Cerrar sesión del admin
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/logout/'))

        # Borra todas las cookies después de cerrar sesión
        self.selenium.delete_all_cookies()

        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/?next=/admin/'))
        #http://127.0.0.1:8000/admin/login/?next=/admin/

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('staffuser')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()


        # Loguearse con el usuario staff
        #self.login("staffuser", "pirineus")

        # Comprobar acceso a Questions
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        self.assertTrue("Questions" in self.selenium.page_source)

        # Intentar acceder a Users (debería fallar)
        try:
            self.selenium.find_element(By.XPATH,"//a[text()='Users']") 
            assert False, "Trobat element que NO hi ha de ser"
        except NoSuchElementException: 
            pass