import requests
from threading import Thread
from time import sleep
import xml.etree.ElementTree as ET


class PrestashopAPI(Thread):
    """
    Clase que se encarga de comunicarse con la API de Prestashop.

    Mediante esta clase, se puede comunicar fácilmente con la API de Prestashop en Python, facilitando su uso.
    Parámetros:
    url: str -- url de la tienda online de prestashop, debe llevar el 'http://' al principio y el '/api' al final
    key: str -- clave del WebService de Prestashop
    func_changes: Function -- función a ejecutar cuando haya algún cambio en la lista de productos
    func_stock:Function -- función a ejecutar cuando haya algún producto bajo de stock
    """

    def __init__(self, url, key, func_changes, func_stock):
        """
        Constructor de la clase PrestashopAPI, realiza una primera llamada a cargar los productos y clientes en el programa.
        """
        super(PrestashopAPI, self).__init__()
        self.url = url
        self.key = key
        self.func_changes = func_changes
        self.func_stock = func_stock
        self.cambios = ""
        self.productos = self._update_products()
        self.clientes = self._update_customers()

    def run(self):
        """
        Función que se encarga de ejecutar el hilo y comprobar periódicamente cambios.
        """
        while True:
            if self._get_changes():
                self.func_changes(self.cambios)
            sleep(300)

    def _get_changes(self):
        """
        Función que obtiene cambios en la lista de productos y/o clientes.
        """
        change = False
        productos = self._update_products()
        clientes = self._update_customers()
        if change:
            self.productos = productos
            self.clientes = clientes
            self.cambios = ""
        else:
            self.cambios = ""
        return change

    def _need_supplies(self):
        """
        Función que comprueba si algún artículo está bajo de stock, avisándolo.
        """
        needed = False

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
        for x in tree.iter('product'):
            r = requests.get(self.url + "/products/" +
                             x.attrib['id'], auth=(self.key, ''))
            product_id = ET.fromstring(r.text)
            product_id = product_id.find('product')
            if product_id.find('associations').find('combinations').text is None:
                r = requests.get(self.url + "/stock_availables/" +
                                 x.attrib['id'], auth=(self.key, ''))
                stock_id = ET.fromstring(r.text)
                stock_id = stock_id.find('stock_available')
                if int(stock_id.find('quantity').text) < 50:
                    bajo_stock = True
                else:
                    bajo_stock = False
                productos.append({'nombre': product_id.find('name').find('language').text,
                                  'necesita_stock?': bajo_stock})
            else:
                product_dict = {'nombre': product_id.find(
                    'name').find('language').text}
                for y in product_id.find('associations').find('combinations').findall('combination'):
                    r = requests.get(self.url + "/combinations/" +
                                     y.find('id').text, auth=(self.key, ''))
                    combination_id = ET.fromstring(r.text)
                    combination_id = combination_id.find('combination')
                    if int(combination_id.find('quantity').text) < 50:
                        bajo_stock = True
                    else:
                        bajo_stock = False

                    options = ""
                    for option in combination_id.find('associations').find('product_option_values').findall('product_option_value'):
                        r = requests.get(
                            option.attrib['{http://www.w3.org/1999/xlink}href'], auth=(self.key, ''))
                        option_id = ET.fromstring(r.text)
                        option_id = option_id.find('product_option_value').find(
                            'name').find('language').text
                        options += option_id + ":"

                    options = options[:len(options)-1]
                    product_dict[options] = {'necesita_stock?': bajo_stock}

                productos.append(product_dict)
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
