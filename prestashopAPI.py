import xml.etree.ElementTree as ET
from threading import Thread
from time import sleep

import requests


class PrestashopAPI(Thread):
    """
    Clase que se encarga de comunicarse con la API de Prestashop.

    Mediante esta clase, se puede comunicar fácilmente con la API de Prestashop en Python, facilitando su uso.
    Por ahora, solo funciona con los productos que sean simples, sin combinaciones.
    Parámetros:
    url: str -- url de la tienda online de prestashop, debe llevar el 'http://' al principio y el '/api' al final
    key: str -- clave del WebService de Prestashop
    func_changes: Function -- función a ejecutar cuando haya algún cambio en la lista de productos
    func_stock:Function -- función a ejecutar cuando haya algún producto bajo de stock
    """

    def __init__(self, url, key, func_changes, func_stock, time):
        """
        Constructor de la clase PrestashopAPI, realiza una primera llamada a cargar los productos y clientes en el programa.
        """
        super(PrestashopAPI, self).__init__()
        self.url = url
        self.key = key
        self.func_changes = func_changes
        self.func_stock = func_stock
        self.cambios = ""
        self.stock = ""
        self.estado = True
        self.time = time
        self.valor = 0
        self.productos = self._update_products()
        self.clientes = self._update_customers()

    def run(self):
        """
        Función que se encarga de ejecutar el hilo y comprobar periódicamente cambios.
        """
<<<<<<< HEAD
        while self.estado:
            try:
                if self._get_changes():
                    self.func_changes(self.cambios)
                if self._need_supplies():
                    self.func_stock(self.stock)
                while self.valor < 1200:
                    try:
                        sleep(0.1)
                        self.valor += 1
                    except KeyboardInterrupt:
                        self.valor = 12000
                        print("Captado Ctrl-C")
                self.valor = 0
            except KeyboardInterrupt:
                self.estado = False
                print("Captado Ctrl-C")

    def stop(self):
        self.estado = False
=======
        while True:
            if self._get_changes():
                self.func_changes(self.cambios)
            if self._need_supplies():
                self.func_stock(self.stock)
            sleep(300)
>>>>>>> 63c706e8280d1e463fb6fb7b4a14d4a175773d8b

    def _get_changes(self):
        """
        Función que obtiene cambios en la lista de productos.
        """
        self.cambios = "Se han realizado los siguientes cambios:\n"
        change = False
        cont = 1
        productos = self._update_products()
        if productos != self.productos:
            change = True
            for x in productos:
                cambia = True
                for y in self.productos:
                    if x['nombre'] == y['nombre']:
                        cambia = False
<<<<<<< HEAD
                if cambia == True:
                    self.cambios += str(cont) + ".- " + "Añadido " + x['nombre'] + "\n"
                    cont += 1
=======
                if cambia:
                    self.cambios += "Añadido " + x['nombre'] + "\n"
>>>>>>> 63c706e8280d1e463fb6fb7b4a14d4a175773d8b
            for x in self.productos:
                cambia = True
                for y in productos:
                    if x['nombre'] == y['nombre']:
                        cambia = False
<<<<<<< HEAD
                if cambia == True:
                    self.cambios += str(cont) + ".- " + "Eiiminado " + x['nombre'] + "\n"
                    cont += 1
=======
                if cambia:
                    self.cambios += "Eiiminado " + x['nombre'] + "\n"
>>>>>>> 63c706e8280d1e463fb6fb7b4a14d4a175773d8b
        self.productos = productos
        self.clientes = self._update_customers()
        return change

    def _need_supplies(self):
        """
        Función que comprueba si algún artículo está bajo de stock, avisándolo.
        """
        cont = 1
        self.stock = "Estos artículos necesitan re-stock:\n"
        needed = False
        for x in self.productos:
            if x['necesita_stock?']:
                needed = True
                self.stock += str(cont) + ".- " + x['nombre']
                cont += 1

        return needed

    def _update_products(self):
        """
        Función que retorna la lista de productos de nuestra tienda online.

        Esta función recopila mediante llamadas a la API de Prestashop la lista de productos que se encuentran en
        nuestra tienda OnLine

        :return: productos: Dict -- lista de productos en la tienda OnLine
        """
        productos = []
        products = requests.get(self.url + "/products", auth=(self.key, ''))
        tree = ET.fromstring(products.text)
        tree.find('products')
        for x in tree.iter('product'):
            r = requests.get(
                x.attrib['{http://www.w3.org/1999/xlink}href'], auth=(self.key, ''))
            product_id = ET.fromstring(r.text)
            product_id = product_id.find('product')
<<<<<<< HEAD
            r = requests.get(product_id.find('associations').find('stock_availables').find(
                'stock_available').attrib['{http://www.w3.org/1999/xlink}href'], auth=(self.key, ''))
=======
            r = requests.get(product_id.find('associations').find('stock_availables').find('stock_available').attrib[
                                 '{http://www.w3.org/1999/xlink}href'], auth=(self.key, ''))
>>>>>>> 63c706e8280d1e463fb6fb7b4a14d4a175773d8b
            stock_id = ET.fromstring(r.text)
            stock_id = stock_id.find('stock_available')
            if int(stock_id.find('quantity').text) < 50:
                bajo_stock = True
            else:
                bajo_stock = False
            productos.append({'nombre': product_id.find('name').find('language').text,
                              'necesita_stock?': bajo_stock})
        return productos

    def _update_customers(self):
        """
        Función que retorna la lista de clientes de nuestra tienda online.

        Esta función recopila mediante llamadas a la API de Prestashop la lista de clientes que tenemos en nuestra
        tienda OnLine

        :return: clientes: List -- lista de clientes en nuestra tienda OnLine
        """
        clientes = []
        customers = requests.get(self.url + "/customers", auth=(self.key, ''))
        tree = ET.fromstring(customers.text)
        for x in tree.iter('customer'):
            r = requests.get(self.url + "/customers/" +
                             x.attrib['id'], auth=(self.key, ''))
            customer_id = ET.fromstring(r.text)
            customer_id = customer_id.find('customer')
            clientes.append({'nombre': customer_id.find('firstname').text,
                             'apellidos': customer_id.find('lastname').text,
                             'email': customer_id.find('email').text,
                             'fecha_nacimiento': customer_id.find('birthday').text})
        return clientes

    def get_products(self):
        return self.productos

    def get_customers(self):
        return self.clientes
