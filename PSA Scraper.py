import asyncio
import time

import playwright

import nanoid
from selenium.webdriver import chromium

import Part
import re
import psutil
import supabase

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


parts = []


async def complete_rifles():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await stealth_async(page)

        rifles_url = "https://palmettostatearmory.com/ar-15/rifles.html" \
                     "?product_list_mode=list "
        pistols_url = "https://palmettostatearmory.com/ar-15/pistols.html" \
                      "?product_list_mode=list "
        await page.goto(pistols_url)

        all_product_names = []

        await page.get_by_role("button", name="Yes").click(button="left")
        time.sleep(2)

        while True:
            await page.wait_for_timeout(
                1000)  # Wait for a short interval after scrolling
            await page.wait_for_selector('.product-item-link')

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')
            for link in product_names:
                await page.goto(link, timeout=30000)
                time.sleep(3)
                product_name = await page.evaluate('''() => {
                    const element = document.querySelector('.page-title');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                product_price = await page.evaluate('''() => {
                    const element = document.querySelector('.price');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                product_image_url = await page.evaluate('''() => {
                    const element = document.querySelector('.fotorama__stage__frame');
                    return element ? element.getAttribute('href') : 'Image not found';
                }''')
                product_manufacturer_name = await page.evaluate('''() => {
                            const element = document.querySelector('.col.data[data-th="Brand"]');
                            return element ? element.textContent.trim() : 'Brand text not found';
                        }''')
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url, product_manufacturer_name,
                                     bcg=True,
                                     charging_handle=True,
                                     upper=True, lower=True)
                print(new_part.name)
                await page.go_back(timeout=30000)
                time.sleep(1)

            all_product_names.extend(product_names)
            try:
                next_button = await page.get_by_role("link",
                                                     name="Next ").click(
                    button="left")
                # Wait for the page navigation to complete
                time.sleep(2)
            except Exception as e:
                print("Finished")
                break  # Exit the loop if there is no next page

        await browser.close()


async def lowers():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await stealth_async(page)

        lowers_url = "https://palmettostatearmory.com/ar-15/lowers/complete-lowers.html"
        await page.goto(lowers_url)

        all_product_names = []

        await page.get_by_role("button", name="Yes").click(button="left")
        time.sleep(3)

        while True:
            await page.wait_for_timeout(
                1000)  # Wait for a short interval after scrolling
            await page.wait_for_selector('.product-item-link')

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')
            for link in product_names:
                await page.goto(link)
                time.sleep(1)
                await page.screenshot(path="should have image url.png")
                product_name = await page.evaluate('''() => {
                    const element = document.querySelector('.page-title');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                product_price = await page.evaluate('''() => {
                    const element = document.querySelector('.price');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                product_image_url = await page.evaluate('''() => {
                    const element = document.querySelector('.fotorama__stage__frame');
                    return element ? element.getAttribute('href') : 'Image not found';
                }''')
                product_manufacturer_name = await page.evaluate('''() => {
                            const element = document.querySelector('.col.data[data-th="Brand"]');
                            return element ? element.textContent.trim() : 'Brand text not found';
                        }''')
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url, product_manufacturer_name,
                                     charging_handle=False,
                                     bcg=False,
                                     upper=False, lower=True)
                print(new_part.name)
                await page.go_back()

            all_product_names.extend(product_names)
            try:
                next_button = await page.get_by_role("link",
                                                     name="Next ").click(
                    button="left")
                # Wait for the page navigation to complete
                time.sleep(2)
            except Exception as e:
                print("Finished")
                break  # Exit the loop if there is no next page

        await browser.close()


async def charging_handles():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await stealth_async(page)

        charging_handles_url = "https://palmettostatearmory.com/ar-15/parts" \
                               "/upper-parts/charging-handles.html "
        await page.goto(charging_handles_url)

        all_product_names = []

        await page.get_by_role("button", name="Yes").click(button="left")
        time.sleep(3)

        while True:
            await page.wait_for_timeout(
                1000)  # Wait for a short interval after scrolling
            await page.wait_for_selector('.product-item-link')

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')
            for link in product_names:
                await page.goto(link)
                time.sleep(1)
                await page.screenshot(path="should have image url.png")
                product_name = await page.evaluate('''() => {
                    const element = document.querySelector('.page-title');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                product_price = await page.evaluate('''() => {
                    const element = document.querySelector('.price');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                product_image_url = await page.evaluate('''() => {
                    const element = document.querySelector('.fotorama__stage__frame');
                    return element ? element.getAttribute('href') : 'Image not found';
                }''')
                product_manufacturer_name = await page.evaluate('''() => {
                            const element = document.querySelector('.col.data[data-th="Brand"]');
                            return element ? element.textContent.trim() : 'Brand text not found';
                        }''')
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url, product_manufacturer_name,
                                     upper=False,
                                     charging_handle=True,
                                     lower=False, bcg=False)
                print(new_part.name)
                await page.go_back()

            all_product_names.extend(product_names)
            try:
                next_button = await page.get_by_role("link",
                                                     name="Next ").click(
                    button="left")
                # Wait for the page navigation to complete
                time.sleep(2)
            except Exception as e:
                print("Finished")
                break  # Exit the loop if there is no next page

        await browser.close()


async def bcgs():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await stealth_async(page)

        charging_handles_url = "https://palmettostatearmory.com/ar-15/parts" \
                               "/upper-parts/bolt-carrier-groups/complete.html"
        await page.goto(charging_handles_url)

        all_product_names = []

        await page.get_by_role("button", name="Yes").click(button="left")
        time.sleep(3)

        while True:
            await page.wait_for_timeout(
                1000)  # Wait for a short interval after scrolling
            await page.wait_for_selector('.product-item-link')

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')
            for link in product_names:
                await page.goto(link)
                time.sleep(1)
                await page.screenshot(path="should have image url.png")
                product_name = await page.evaluate('''() => {
                    const element = document.querySelector('.page-title');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                product_price = await page.evaluate('''() => {
                    const element = document.querySelector('.price');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                product_image_url = await page.evaluate('''() => {
                    const element = document.querySelector('.fotorama__stage__frame');
                    return element ? element.getAttribute('href') : 'Image not found';
                }''')
                product_manufacturer_name = await page.evaluate('''() => {
                            const element = document.querySelector('.col.data[data-th="Brand"]');
                            return element ? element.textContent.trim() : 'Brand text not found';
                        }''')
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url, product_manufacturer_name,
                                     upper=False,
                                     charging_handle=False,
                                     lower=False, bcg=True)
                print(new_part.name)
                await page.go_back()

            all_product_names.extend(product_names)
            try:
                next_button = await page.get_by_role("link",
                                                     name="Next ").click(
                    button="left")
                # Wait for the page navigation to complete
                time.sleep(2)
            except Exception as e:
                print("Finished")
                break  # Exit the loop if there is no next page

        await browser.close()


async def uppers():
    async with async_playwright() as p:
        page_number = 1
        uppers_url = "https://palmettostatearmory.com/ar-15/barreled-upper-assemblies.html?p=1"
        uppers_url = uppers_url[0:uppers_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(uppers_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            await page.wait_for_load_state('networkidle')
            await page.wait_for_selector('.product-item-link')

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                if "kit" in link:
                    continue
                await page.goto(link)
                await page.wait_for_load_state('networkidle')
                product_name = await page.evaluate('''() => {
                    const element = document.querySelector('.page-title');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                if "kit" in product_name:
                    await page.goto(uppers_url)
                    await page.wait_for_load_state('networkidle')
                    continue
                bcg = True
                charging_handle = True
                if re.search(
                        '(without.*(?:bcg|bolt\s+carrier\s+group)|w/o.*(?:bcg|bolt\s+carrier\s+group)|no.*('
                        '?:bcg|bolt\s+carrier\s+group))',
                        product_name.lower()):
                    bcg = False
                if re.search(
                        '(without.*(?:ch|charging\s+handle)|w/o.*(?:ch|charging\s+handle)|no.*('
                        '?:ch|charging\s+handle))',
                        product_name.lower()):
                    charging_handle = False

                if product_name == "Name not found":
                    await page.goto(uppers_url)
                    await page.wait_for_load_state('networkidle')
                    continue
                product_price = await page.evaluate('''() => {
                    const element = document.querySelector('.price');
                    return element ? element.textContent.trim() : 'Name not found';
                }''')
                if product_price == "Name not found":
                    await page.goto(uppers_url)
                    await page.wait_for_load_state('networkidle')
                    continue

                product_image_url = await page.evaluate('''() => {
                    const element = document.querySelector('.fotorama__stage__frame');
                    return element ? element.getAttribute('href') : 'Image not found';
                }''')
                if product_image_url == "Name not found":
                    await page.goto(uppers_url)
                    await page.wait_for_load_state('networkidle')
                    continue
                product_manufacturer_name = await page.evaluate('''() => {
                            const element = document.querySelector('.col.data[data-th="Brand"]');
                            return element ? element.textContent.trim() : 'Brand text not found';
                        }''')
                if product_manufacturer_name == "Name not found":
                    await page.goto(uppers_url)
                    await page.wait_for_load_state('networkidle')
                    continue
                new_part = Part.Part(product_name, product_price,
                                     product_image_url,
                                     page.url,
                                     product_manufacturer_name,
                                     upper=False,
                                     charging_handle=charging_handle,
                                     lower=False, bcg=bcg)
                generate_nano_id(new_part)
                print(new_part.__str__())
                parts.append({"nano_id": new_part.nano_id,
                              "name": new_part.name,
                              "price": new_part.price,
                              "image_url": new_part.image_url,
                              "url": new_part.url,
                              "manufacturer": new_part.manufacturer,
                              "upper": new_part.upper,
                              "charging_handle": new_part.charging_handle,
                              "bcg": new_part.bcg,
                              "lower": new_part.lower
                              })
                await page.goto(uppers_url)
                await page.wait_for_load_state('networkidle')

            next_button_enabled = await page.query_selector(
                'a[title="Next"][disabled]') is None
            time.sleep(2)
            if next_button_enabled:
                print("button is enabled")
                page_number += 1
                uppers_url = uppers_url[
                             0:uppers_url.index("?p=")] + \
                             "?p=" + str(page_number)
                await page.goto(uppers_url)
            else:
                print("Finished")
                break


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
    part.nano_id = nanoid.generate(size=8)


def upload_parts():
    # Replace with your Supabase credentials
    supabase_url = 'https://zlcjginwzjvtkktudpem.supabase.co'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpsY2pnaW53emp2dGtrdHVkcGVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzgzODYwMTcsImV4cCI6MTk5Mzk2MjAxN30.XgpdXsVdErMHatAAnpn2sfAhM5gEDJH33qCWQNNsoO4'

    # Initialize Supabase client
    client = supabase.Client(supabase_url, supabase_key)

    for part in parts:
        # 'parts' is the name of the table
        # 'returning="minimal"' specifies to return only the count of affected rows
        response = client.table('parts').insert(part, returning="minimal")

    # Example query to fetch data from 'parts' table
    query = client.from_('new_parts').select('*')

    # Execute the query
    response = query.execute()

    # Print fetched data
    print(response)


#asyncio.run(uppers())
tes_data
upload_parts()
