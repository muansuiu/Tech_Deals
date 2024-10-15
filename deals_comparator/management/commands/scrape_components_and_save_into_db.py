from django.core.management.base import BaseCommand
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from deals_comparator.utility.utils import Utils
from deals_comparator.models import Components


class Command(BaseCommand):
    help = 'Scrape data from websites'
    utils = Utils()
    vendors_json_file = "vendors_url_mapping.json"

    def add_arguments(self, parser):
        parser.add_argument('vendor_name', type=str, help='Selects the vendor the program wants to scrape')

    def handle(self, *args, **kwargs):
        vendor = kwargs['vendor_name']
        self.select_vendor(vendor=vendor)
        
    def select_vendor(self, vendor):
        driver = self.utils.get_chrome_driver()
        vendors_data = self.utils.read_json_file(filepath=self.vendors_json_file)
        vendor_url = vendors_data.get(vendor)

        if vendor == "startech":
            scraped_data = self.scrape_startech_keyboards(url=vendor_url,driver=driver)
        
        elif vendor == "skyland":
            scraped_data = self.scrape_skyland_keyboards(url=vendor_url,driver=driver)
            
        self.insert_data_into_db(scraped_data=scraped_data)
    
    def scrape_startech_keyboards(self, url, driver):
        
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        content_div = wait.until(EC.presence_of_element_located((By.ID, "content")))

        # Find all product items
        items = content_div.find_elements(By.CLASS_NAME, "p-item")

        products = []

        # extracting products name, image url, description, price etc
        for item in items:
            product = {}
            
            try:
                name_element = item.find_element(By.CLASS_NAME, "p-item-name")
                product['name'] = name_element.text.strip()
            
            except:
                product['name'] = "N/A"

            
            try: 
                img_element = item.find_element(By.CSS_SELECTOR, ".p-item-img img")
                product['image_url'] = img_element.get_attribute('src')
            
            except:
                product['image_url'] = "N/A"

            try:
                desc_element = item.find_element(By.CLASS_NAME, "short-description")
                product['description'] = desc_element.text.strip()
            except:
                product['description'] = "N/A"

            try:
                price_element = item.find_element(By.CLASS_NAME, "p-item-price")
                product['price'] = price_element.text.strip()

            except:
                product['price'] = 0

            if product['price'] == "Out Of Stock" or product['price'] == 0:
                product['price'] = None
                product['available'] = False

            else:
                product['available'] = True

            product['component_type'] = 'keyboard'

            product['vendor'] = 'startech'
            
            
            products.append(product)

        # Close the browser
        driver.quit()

        return products
        
    def scrape_skyland_keyboards(self, url, driver):
        
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        
        product_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-layout")))

        products = []

        # extracting products name, image url, description, price etc
        
        for product_element in product_elements:
            product = {}
            
            try:
                name_elem = product_element.find_element(By.CSS_SELECTOR, "div.name a")
                product['name'] = name_elem.text.strip()
            except:
                product['name'] = "N/A"
            
            try:
                desc_elem = product_element.find_element(By.CLASS_NAME, "description")
                product['description'] = desc_elem.text.strip()
            except:
                product['description'] = "N/A"
            
            try:
                img_elem = product_element.find_element(By.CSS_SELECTOR, "div.product-thumb div.image-group div.image img")
                product['image_url'] = img_elem.get_attribute('src')
            except:
                product['image_url'] = "N/A"

            if len(product['image_url']) > 200:
                product['image_url'] = product['image_url'][:200]
            
            try:
                price_elem = product_element.find_element(By.CLASS_NAME, "price-new")
                product['price'] = price_elem.text.strip()
            except:
                product['price'] = 0

            if product['price'] == '' or product['price'] == 0:
                product['price'] = None
                product['available'] = False
            
            else:
                product['available'] = True

            product['component_type'] = 'keyboard'

            product['vendor'] = "skyland"
            
            products.append(product)

        # Close the browser
        driver.quit()
        
        return products
    
    def insert_data_into_db(self, scraped_data):
        components_instances = [Components(**data) for data in scraped_data]
        
        Components.objects.bulk_create(components_instances)

        print(f"Inserted {len(scraped_data)} components into DB")