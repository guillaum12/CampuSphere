import random
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Post
from profiles.models import Profile
from django.test import LiveServerTestCase

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class SignupTest(LiveServerTestCase):
  def testform(self):

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    selenium = webdriver.Chrome(options=options)

    #Choose your url to visit
    selenium.get('http://127.0.0.1:8000/auth/signup/')
    random_number = random.randint(0, 100000).__str__()
    # Remplissez le formulaire avec des données de test
    selenium.find_element(By.ID, 'id_username').send_keys('testuser' + random_number)
    selenium.find_element(By.ID, 'id_email').send_keys('test' +random_number+ '@example.com')
    selenium.find_element(By.ID, 'id_password1').send_keys('Testpassword758!')
    selenium.find_element(By.ID, 'id_password2').send_keys('Testpassword758!')
    selenium.find_element(By.CLASS_NAME, 'button').click()

    # selenium.get("http://127.0.0.1:8000/posts/feedback/")

    for i in range(2):
      selenium.implicitly_wait(5)
      selenium.find_element(By.ID, 'newPostButton').click()

      selenium.find_element(By.ID, 'id_title').send_keys('test ' + i.__str__())
      selenium.find_element(By.ID, 'newPostSubmit').send_keys(Keys.ENTER)


