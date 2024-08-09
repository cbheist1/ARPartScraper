import asyncio
import time

import playwright
import requests
import json
import nanoid
from postgrest import APIError

import Part
import re
import psutil
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from supabase import create_client

parts = []


async def handguards():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://bravocompanyusa.com/polymer-handguards/?page=1"
        page_url = page_url[
                      0:page_url.index("?page=")] + "?page=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        time.sleep(5)
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            # Wait for the product items to be loaded
            try:
                product_elements = await page.wait_for_selector(
                    '.product')  # Wait for the product items to be present on the page
            except playwright._impl._errors.TimeoutError:
                return
            product_names = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('.product').forEach(product => {  // Adjust the parent selector if needed
                    const titleElement = product.querySelector('.card-title');
                    const title = titleElement ? titleElement.textContent.trim() : 'N/A';
                    const urlElement = product.querySelector('.card-title a');
                    const url = urlElement ? urlElement.getAttribute('href') : 'N/A';
                    const urlImageElement = product.querySelector('.card-img-container img');
                    const urlImage = urlImageElement ? urlImageElement.getAttribute('src') : 'N/A';
                    const priceElement = product.querySelector('.price--withoutTax');
                    const price = priceElement ? priceElement.textContent.trim() : 'N/A';
                    const brandElement = product.querySelector('.card-text[data-test-info-type="brandName"');
                    const brand = brandElement ? brandElement.textContent.trim() : 'N/A';
                    
                    items.push({ title, price , url , urlImage , brand });
                });
                return items;
            }''')
            print(product_names)
            # Extract and print product names
            for product in product_names:
                if bad_counter >= 3:
                    continue

                product_name = product['title']
                if product_name == "N/A":
                    continue
                product_price = product['price']
                if product_price == "N/A":
                    bad_counter += 1
                    continue

                product_image_url = product['urlImage']
                if product_image_url == "N/A":
                    continue
                product_manufacturer_name = product['brand']
                if product_manufacturer_name == "N/A":
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=False,
                                     attachment=True)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"id": new_part.id,
                              "name": new_part.name,
                              "price": float(
                                  new_part.price[1:].replace(',', '')),
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower,
                              "attachment": new_part.attachment
                              })

            page_number += 1
            page_url = page_url[
                       0:page_url.index("?page=")] + \
                       "?page=" + str(page_number)
            await page.goto(page_url)


async def pistol_grips():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://bravocompanyusa.com/pistol-grips/?page=1"
        page_url = page_url[
                   0:page_url.index("?page=")] + "?page=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        time.sleep(5)
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            # Wait for the product items to be loaded
            try:
                product_elements = await page.wait_for_selector(
                    '.product')  # Wait for the product items to be present on the page
            except playwright._impl._errors.TimeoutError:
                return
            product_names = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('.product').forEach(product => {  // Adjust the parent selector if needed
                    const titleElement = product.querySelector('.card-title');
                    const title = titleElement ? titleElement.textContent.trim() : 'N/A';
                    const urlElement = product.querySelector('.card-title a');
                    const url = urlElement ? urlElement.getAttribute('href') : 'N/A';
                    const urlImageElement = product.querySelector('.card-img-container img');
                    const urlImage = urlImageElement ? urlImageElement.getAttribute('src') : 'N/A';
                    const priceElement = product.querySelector('.price--withoutTax');
                    const price = priceElement ? priceElement.textContent.trim() : 'N/A';
                    const brandElement = product.querySelector('.card-text[data-test-info-type="brandName"');
                    const brand = brandElement ? brandElement.textContent.trim() : 'N/A';

                    items.push({ title, price , url , urlImage , brand });
                });
                return items;
            }''')
            print(product_names)
            # Extract and print product names
            for product in product_names:
                if bad_counter >= 3:
                    continue

                product_name = product['title']
                if product_name == "N/A":
                    continue
                product_price = product['price']
                if product_price == "N/A":
                    bad_counter += 1
                    continue

                product_image_url = product['urlImage']
                if product_image_url == "N/A":
                    continue
                product_manufacturer_name = product['brand']
                if product_manufacturer_name == "N/A":
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=False,
                                     attachment=True)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"id": new_part.id,
                              "name": new_part.name,
                              "price": float(
                                  new_part.price[1:].replace(',', '')),
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower,
                              "attachment": new_part.attachment
                              })

            page_number += 1
            page_url = page_url[
                       0:page_url.index("?page=")] + \
                       "?page=" + str(page_number)
            await page.goto(page_url)


async def vertical_grips():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://bravocompanyusa.com/vertical-grips-hand-stops/?page=1"
        page_url = page_url[
                   0:page_url.index("?page=")] + "?page=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        time.sleep(5)
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            # Wait for the product items to be loaded
            try:
                product_elements = await page.wait_for_selector(
                    '.product')  # Wait for the product items to be present on the page
            except playwright._impl._errors.TimeoutError:
                return
            product_names = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('.product').forEach(product => {  // Adjust the parent selector if needed
                    const titleElement = product.querySelector('.card-title');
                    const title = titleElement ? titleElement.textContent.trim() : 'N/A';
                    const urlElement = product.querySelector('.card-title a');
                    const url = urlElement ? urlElement.getAttribute('href') : 'N/A';
                    const urlImageElement = product.querySelector('.card-img-container img');
                    const urlImage = urlImageElement ? urlImageElement.getAttribute('src') : 'N/A';
                    const priceElement = product.querySelector('.price--withoutTax');
                    const price = priceElement ? priceElement.textContent.trim() : 'N/A';
                    const brandElement = product.querySelector('.card-text[data-test-info-type="brandName"');
                    const brand = brandElement ? brandElement.textContent.trim() : 'N/A';

                    items.push({ title, price , url , urlImage , brand });
                });
                return items;
            }''')
            print(product_names)
            # Extract and print product names
            for product in product_names:
                if bad_counter >= 3:
                    continue

                product_name = product['title']
                if product_name == "N/A":
                    continue
                product_price = product['price']
                if product_price == "N/A":
                    bad_counter += 1
                    continue

                product_image_url = product['urlImage']
                if product_image_url == "N/A":
                    continue
                product_manufacturer_name = product['brand']
                if product_manufacturer_name == "N/A":
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=False,
                                     attachment=True)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"id": new_part.id,
                              "name": new_part.name,
                              "price": float(
                                  new_part.price[1:].replace(',', '')),
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower,
                              "attachment": new_part.attachment
                              })

            page_number += 1
            page_url = page_url[
                       0:page_url.index("?page=")] + \
                       "?page=" + str(page_number)
            await page.goto(page_url)


async def optics():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://bravocompanyusa.com/optics-iron-sights-and-mounts/optics/?page=1"
        page_url = page_url[
                   0:page_url.index("?page=")] + "?page=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        time.sleep(5)
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            # Wait for the product items to be loaded
            try:
                product_elements = await page.wait_for_selector(
                    '.product')  # Wait for the product items to be present on the page
            except playwright._impl._errors.TimeoutError:
                return
            product_names = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('.product').forEach(product => {  // Adjust the parent selector if needed
                    const titleElement = product.querySelector('.card-title');
                    const title = titleElement ? titleElement.textContent.trim() : 'N/A';
                    const urlElement = product.querySelector('.card-title a');
                    const url = urlElement ? urlElement.getAttribute('href') : 'N/A';
                    const urlImageElement = product.querySelector('.card-img-container img');
                    const urlImage = urlImageElement ? urlImageElement.getAttribute('src') : 'N/A';
                    const priceElement = product.querySelector('.price--withoutTax');
                    const price = priceElement ? priceElement.textContent.trim() : 'N/A';
                    const brandElement = product.querySelector('.card-text[data-test-info-type="brandName"');
                    const brand = brandElement ? brandElement.textContent.trim() : 'N/A';

                    items.push({ title, price , url , urlImage , brand });
                });
                return items;
            }''')
            print(product_names)
            # Extract and print product names
            for product in product_names:
                if bad_counter >= 3:
                    continue

                product_name = product['title']
                if product_name == "N/A":
                    continue
                product_price = product['price']
                if product_price == "N/A":
                    bad_counter += 1
                    continue

                product_image_url = product['urlImage']
                if product_image_url == "N/A":
                    continue
                product_manufacturer_name = product['brand']
                if product_manufacturer_name == "N/A":
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=False,
                                     attachment=True)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"id": new_part.id,
                              "name": new_part.name,
                              "price": float(
                                  new_part.price[1:].replace(',', '')),
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower,
                              "attachment": new_part.attachment
                              })

            page_number += 1
            page_url = page_url[
                       0:page_url.index("?page=")] + \
                       "?page=" + str(page_number)
            await page.goto(page_url)


async def optic_mounts():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://bravocompanyusa.com/optics-iron-sights-and-mounts/optic-mounts/?page=1"
        page_url = page_url[
                   0:page_url.index("?page=")] + "?page=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        time.sleep(5)
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            # Wait for the product items to be loaded
            try:
                product_elements = await page.wait_for_selector(
                    '.product')  # Wait for the product items to be present on the page
            except playwright._impl._errors.TimeoutError:
                return
            product_names = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('.product').forEach(product => {  // Adjust the parent selector if needed
                    const titleElement = product.querySelector('.card-title');
                    const title = titleElement ? titleElement.textContent.trim() : 'N/A';
                    const urlElement = product.querySelector('.card-title a');
                    const url = urlElement ? urlElement.getAttribute('href') : 'N/A';
                    const urlImageElement = product.querySelector('.card-img-container img');
                    const urlImage = urlImageElement ? urlImageElement.getAttribute('src') : 'N/A';
                    const priceElement = product.querySelector('.price--withoutTax');
                    const price = priceElement ? priceElement.textContent.trim() : 'N/A';
                    const brandElement = product.querySelector('.card-text[data-test-info-type="brandName"');
                    const brand = brandElement ? brandElement.textContent.trim() : 'N/A';

                    items.push({ title, price , url , urlImage , brand });
                });
                return items;
            }''')
            print(product_names)
            # Extract and print product names
            for product in product_names:
                if bad_counter >= 3:
                    continue

                product_name = product['title']
                if product_name == "N/A":
                    continue
                product_price = product['price']
                if product_price == "N/A":
                    bad_counter += 1
                    continue

                product_image_url = product['urlImage']
                if product_image_url == "N/A":
                    continue
                product_manufacturer_name = product['brand']
                if product_manufacturer_name == "N/A":
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=False,
                                     attachment=True)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"id": new_part.id,
                              "name": new_part.name,
                              "price": float(
                                  new_part.price[1:].replace(',', '')),
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower,
                              "attachment": new_part.attachment
                              })

            page_number += 1
            page_url = page_url[
                       0:page_url.index("?page=")] + \
                       "?page=" + str(page_number)
            await page.goto(page_url)


async def iron_sights():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://bravocompanyusa.com/optics-iron-sights-and-mounts/iron-sights/?page=1"
        page_url = page_url[
                   0:page_url.index("?page=")] + "?page=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        time.sleep(5)
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            # Wait for the product items to be loaded
            try:
                product_elements = await page.wait_for_selector(
                    '.product')  # Wait for the product items to be present on the page
            except playwright._impl._errors.TimeoutError:
                return
            product_names = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('.product').forEach(product => {  // Adjust the parent selector if needed
                    const titleElement = product.querySelector('.card-title');
                    const title = titleElement ? titleElement.textContent.trim() : 'N/A';
                    const urlElement = product.querySelector('.card-title a');
                    const url = urlElement ? urlElement.getAttribute('href') : 'N/A';
                    const urlImageElement = product.querySelector('.card-img-container img');
                    const urlImage = urlImageElement ? urlImageElement.getAttribute('src') : 'N/A';
                    const priceElement = product.querySelector('.price--withoutTax');
                    const price = priceElement ? priceElement.textContent.trim() : 'N/A';
                    const brandElement = product.querySelector('.card-text[data-test-info-type="brandName"');
                    const brand = brandElement ? brandElement.textContent.trim() : 'N/A';

                    items.push({ title, price , url , urlImage , brand });
                });
                return items;
            }''')
            print(product_names)
            # Extract and print product names
            for product in product_names:
                if bad_counter >= 3:
                    continue

                product_name = product['title']
                if product_name == "N/A":
                    continue
                product_price = product['price']
                if product_price == "N/A":
                    bad_counter += 1
                    continue

                product_image_url = product['urlImage']
                if product_image_url == "N/A":
                    continue
                product_manufacturer_name = product['brand']
                if product_manufacturer_name == "N/A":
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=False,
                                     attachment=True)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"id": new_part.id,
                              "name": new_part.name,
                              "price": float(
                                  new_part.price[1:].replace(',', '')),
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower,
                              "attachment": new_part.attachment
                              })

            page_number += 1
            page_url = page_url[
                       0:page_url.index("?page=")] + \
                       "?page=" + str(page_number)
            await page.goto(page_url)


async def stocks():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://bravocompanyusa.com/bcm-stocks/?page=1"
        page_url = page_url[
                   0:page_url.index("?page=")] + "?page=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        time.sleep(5)
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            # Wait for the product items to be loaded
            try:
                product_elements = await page.wait_for_selector(
                    '.product')  # Wait for the product items to be present on the page
            except playwright._impl._errors.TimeoutError:
                return
            product_names = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('.product').forEach(product => {  // Adjust the parent selector if needed
                    const titleElement = product.querySelector('.card-title');
                    const title = titleElement ? titleElement.textContent.trim() : 'N/A';
                    const urlElement = product.querySelector('.card-title a');
                    const url = urlElement ? urlElement.getAttribute('href') : 'N/A';
                    const urlImageElement = product.querySelector('.card-img-container img');
                    const urlImage = urlImageElement ? urlImageElement.getAttribute('src') : 'N/A';
                    const priceElement = product.querySelector('.price--withoutTax');
                    const price = priceElement ? priceElement.textContent.trim() : 'N/A';
                    const brandElement = product.querySelector('.card-text[data-test-info-type="brandName"');
                    const brand = brandElement ? brandElement.textContent.trim() : 'N/A';

                    items.push({ title, price , url , urlImage , brand });
                });
                return items;
            }''')
            print(product_names)
            # Extract and print product names
            for product in product_names:
                if bad_counter >= 3:
                    continue

                product_name = product['title']
                if (product_name == "N/A") or ("kit" in product_name.lower()):
                    continue
                product_price = product['price']
                if product_price == "N/A":
                    bad_counter += 1
                    continue

                product_image_url = product['urlImage']
                if product_image_url == "N/A":
                    continue
                product_manufacturer_name = product['brand']
                if product_manufacturer_name == "N/A":
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=False,
                                     attachment=True)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"id": new_part.id,
                              "name": new_part.name,
                              "price": float(
                                  new_part.price[1:].replace(',', '')),
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower,
                              "attachment": new_part.attachment
                              })

            page_number += 1
            page_url = page_url[
                       0:page_url.index("?page=")] + \
                       "?page=" + str(page_number)
            await page.goto(page_url)


async def muzzle_devices():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://bravocompanyusa.com/ar-15-upper-parts/flash-hiders-compensators-muzzle-brakes/?page=1"
        page_url = page_url[
                   0:page_url.index("?page=")] + "?page=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        time.sleep(5)
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            # Wait for the product items to be loaded
            try:
                product_elements = await page.wait_for_selector(
                    '.product')  # Wait for the product items to be present on the page
            except playwright._impl._errors.TimeoutError:
                return
            product_names = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('.product').forEach(product => {  // Adjust the parent selector if needed
                    const titleElement = product.querySelector('.card-title');
                    const title = titleElement ? titleElement.textContent.trim() : 'N/A';
                    const urlElement = product.querySelector('.card-title a');
                    const url = urlElement ? urlElement.getAttribute('href') : 'N/A';
                    const urlImageElement = product.querySelector('.card-img-container img');
                    const urlImage = urlImageElement ? urlImageElement.getAttribute('src') : 'N/A';
                    const priceElement = product.querySelector('.price--withoutTax');
                    const price = priceElement ? priceElement.textContent.trim() : 'N/A';
                    const brandElement = product.querySelector('.card-text[data-test-info-type="brandName"');
                    const brand = brandElement ? brandElement.textContent.trim() : 'N/A';

                    items.push({ title, price , url , urlImage , brand });
                });
                return items;
            }''')
            print(product_names)
            # Extract and print product names
            for product in product_names:
                if bad_counter >= 3:
                    continue

                product_name = product['title']
                if (product_name == "N/A") or ("washer" in product_name.lower()):
                    continue
                product_price = product['price']
                if product_price == "N/A":
                    bad_counter += 1
                    continue

                product_image_url = product['urlImage']
                if product_image_url == "N/A":
                    continue
                product_manufacturer_name = product['brand']
                if product_manufacturer_name == "N/A":
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=False,
                                     attachment=True)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"id": new_part.id,
                              "name": new_part.name,
                              "price": float(
                                  new_part.price[1:].replace(',', '')),
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower,
                              "attachment": new_part.attachment
                              })

            page_number += 1
            page_url = page_url[
                       0:page_url.index("?page=")] + \
                       "?page=" + str(page_number)
            await page.goto(page_url)


async def retry_page(page, url):
    time.sleep(3)
    await page.goto(url, timeout=30000)


def kill_node_exe_processes_older_than(minutes: int):
    current_time = time.time()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'node.exe':
            process_age_seconds = current_time - proc.create_time()
            if process_age_seconds > (minutes * 60):
                print(
                    f"Killing node.exe process {proc.pid} because it is older than {minutes} minutes")
                proc.kill()
    time.sleep(5)


def generate_nano_id(part):
    part.id = nanoid.generate(size=8)


def upload_parts():
    # Replace with your Supabase credentials
    supabase_url = 'https://wvilawdesqanosmhdrcn.supabase.co'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind2aWxhd2Rlc3Fhbm9zbWhkcmNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjI3OTY2MTgsImV4cCI6MjAzODM3MjYxOH0.E3ZvWAPYvkcSEYo8NG6L8X2f0_7f1dgq_gNxrlKBhRQ'
    table_name = "new_parts"
    json_data = json.dumps(parts)
    supabase = create_client(supabase_url, supabase_key)
    print(supabase)
    endpoint = f"{supabase_url}/table/{table_name}"  # Replace
    # 'table-name' with your actual table name
    print(endpoint)
    headers = {
        'apikey': supabase_key,
        'Content-Type': 'application/json'
    }
    for part in parts:
        #part = {'id': 'YEsdKXSg', 'name': "Toolcraft Logo'd Premium 5.56 Nickel Boron BCG with Carpenter 158 Bolt - 5165449729", 'price': 109.99, 'image_url': 'https://palmettostatearmory.com/media/catalog/product/cache/7af8331bf1196ca28793bd1e8f6ecc7b/5/1/5165449729_052724_3.jpg', 'url': 'https://palmettostatearmory.com/toolcraft-logo-d-premium-5-56-nickel-boron-bcg-with-carpenter-158-bolt-5165449729.html', 'manufacturer': 'Palmetto State Armory', 'upper': False, 'charging_handle': False, 'bcg': True, 'lower': False}
        try:
            #print("Part: " + str(part))
            response = supabase.table(table_name).insert(part).execute()
        except APIError as e:
            # Handle the specific APIError that indicates a unique constraint
            # violation
            if e.message == ("duplicate key value violates unique constraint "
                             "\"new_parts_name_key\""):
                print("Duplicate Value for \"" + part["name"] + "\" found. Part"
                                                                " insertion "
                                                                "updated "
                                                                "instead of "
                                                                "skipped.")
                #response = supabase.table(table_name).delete().eq('name', part['name']).execute()
                #response = supabase.table(table_name).insert(part).execute()
                #response = supabase.table(table_name).upsert({'name': part["name"], 'price': part["price"], 'url': part["url"], 'image_url': part["image_url"]}).execute()
                response = supabase.table(table_name).update(
                    {'name': part["name"], 'price': part["price"],
                     'url': part["url"], 'image_url': part["image_url"]}).eq(
                    column='name', value=part["name"]).execute()


#asyncio.run(handguards())
#upload_parts()
#parts = []
#asyncio.run(pistol_grips())
#upload_parts()
#parts = []
#asyncio.run(vertical_grips())
#upload_parts()
#parts = []
#asyncio.run(optics())
#upload_parts()
#parts = []
#asyncio.run(optic_mounts())
#upload_parts()
#parts = []
#asyncio.run(iron_sights())
#upload_parts()
#parts = []
#asyncio.run(stocks())
#upload_parts()
#parts = []
asyncio.run(muzzle_devices())
upload_parts()
