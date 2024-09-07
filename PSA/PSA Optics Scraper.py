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


async def pistol_red_dots():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/red-dot-sights/pistol-red-dots.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector(
                    'a[title="Next"]'):  # if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                               0:page_url.index("?p=")] + \
                               "?p=" + str(page_number)
                    await page.goto(page_url)
                else:
                    print("Finished")
                    break
            else:
                print("Finished")
                break


async def red_dot_magnifier_combos():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/red-dot-sights/red-dot-magnifier-combos.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector('a[title="Next"]'): #if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                               0:page_url.index("?p=")] + \
                               "?p=" + str(page_number)
                    try:
                        await page.goto(page_url)
                    except Exception as e:
                        await retry_page(page, page_url)
                else:
                    print("Finished")
                    break
            else:
                print("Finished")
                break


async def optic_plates():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/red-dot-sights/optic-plates.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector('a[title="Next"]'): #if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                               0:page_url.index("?p=")] + \
                               "?p=" + str(page_number)
                    try:
                        await page.goto(page_url)
                    except Exception as e:
                        await retry_page(page, page_url)
                else:
                    print("Finished")
                    break
            else:
                print("Finished")
                break


async def riser_mounts():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/red-dot-sights/rise-mounts.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector('a[title="Next"]'): #if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                               0:page_url.index("?p=")] + \
                               "?p=" + str(page_number)
                    try:
                        await page.goto(page_url)
                    except Exception as e:
                        await retry_page(page, page_url)
                else:
                    print("Finished")
                    break
            else:
                print("Finished")
                break


async def holographic_sights():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/holographic-sights.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector('a[title="Next"]'): #if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                               0:page_url.index("?p=")] + \
                               "?p=" + str(page_number)
                    try:
                        await page.goto(page_url)
                    except Exception as e:
                        await retry_page(page, page_url)
                else:
                    print("Finished")
                    break
            else:
                print("Finished")
                break


async def ar_iron_sights():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/rifle-iron-sights/ar-iron-sights.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector('a[title="Next"]'): #if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                               0:page_url.index("?p=")] + \
                               "?p=" + str(page_number)
                    try:
                        await page.goto(page_url)
                    except Exception as e:
                        await retry_page(page, page_url)
                else:
                    print("Finished")
                    break
            else:
                print("Finished")
                break


async def magnifiers():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/magnifiers.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector('a[title="Next"]'): #if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                               0:page_url.index("?p=")] + \
                               "?p=" + str(page_number)
                    try:
                        await page.goto(page_url)
                    except Exception as e:
                        await retry_page(page, page_url)
                else:
                    print("Finished")
                    break
            else:
                print("Finished")
                break


async def scopes():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/scopes/rifle-scopes.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector('a[title="Next"]'): #if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                                 0:page_url.index("?p=")] + \
                                 "?p=" + str(page_number)
                    try:
                        await page.goto(page_url)
                    except Exception as e:
                        await retry_page(page, page_url)
                else:
                    print("Finished")
                    break
            else:
                print("Finished")
                break


async def scope_mounts():
    async with async_playwright() as p:
        parts_count = 0
        bad_counter = 0
        page_number = 1
        page_url = "https://palmettostatearmory.com/sights-optics-scopes/scope-accessories/mounts.html?p=1"
        page_url = page_url[0:page_url.index("?p=")] + "?p=" + str(
            page_number)
        print("started")
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(page_url)
        await page.wait_for_load_state('networkidle')
        all_product_names = []
        age_button = page.get_by_role("button", name="Yes")
        await age_button.click(button="left", timeout=30000)
        while True:
            print("\n" + page.url)
            time.sleep(3)
            try:
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.product-item-link')
            except:
                continue

            # Extract the product names from the current page
            product_names = await page.evaluate('''() => {
                const names = [];
                document.querySelectorAll('.product-item-link').forEach(element => {
                    names.push(element.href.trim());
                });
                return names;
            }''')

            for link in product_names:
                try:
                    if bad_counter >= 3:
                        continue
                    if "kit" in link:
                        continue
                    try:
                        await page.goto(link)
                    except Exception as e:
                        continue
                    await page.wait_for_load_state('networkidle')
                    product_name = await page.evaluate('''() => {
                        const element = document.querySelector('.page-title');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if "kit" in product_name:
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    if product_name == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_price = await page.evaluate('''() => {
                        const element = document.querySelector('.final-price');
                        return element ? element.textContent.trim() : 'Name not found';
                    }''')
                    if product_price == "Name not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        bad_counter += 1
                        continue

                    product_image_url = await page.evaluate('''() => {
                        const element = document.querySelector('.fotorama__stage__frame');
                        return element ? element.getAttribute('href') : 'Image not found';
                    }''')
                    if product_image_url == "Image not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
                        continue
                    product_manufacturer_name = await page.evaluate('''() => {
                                const element = document.querySelector('.col.data[data-th="Brand"]');
                                return element ? element.textContent.trim() : 'Brand text not found';
                            }''')
                    if product_manufacturer_name == "Brand text not found":
                        await page.goto(page_url)
                        await page.wait_for_load_state('networkidle')
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
                    #parts_count += 1
                    #if parts_count >= 2:
                    #    break
                    await page.goto(page_url)
                    await page.wait_for_load_state('networkidle')
                except Exception as e:
                    continue

            #if parts_count >= 2:
            #    break

            if await page.query_selector('a[title="Next"]'): #if the next button exists
                next_button_enabled = await page.query_selector(
                    'a[title="Next"][disabled]') is None
                time.sleep(2)
                if next_button_enabled:
                    print(next_button_enabled)
                    print("button is enabled")
                    page_number += 1
                    page_url = page_url[
                                 0:page_url.index("?p=")] + \
                                 "?p=" + str(page_number)
                    try:
                        await page.goto(page_url)
                    except Exception as e:
                        await retry_page(page, page_url)
                else:
                    print("Finished")
                    break
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
                response = supabase.table(table_name).update({'name': part["name"], 'price': part["price"], 'url': part["url"], 'image_url': part["image_url"]}).eq(column='name', value=part["name"]).execute()




asyncio.run(pistol_red_dots())
upload_parts()
parts = []
asyncio.run(red_dot_magnifier_combos())
upload_parts()
parts = []
asyncio.run(optic_plates())
upload_parts()
parts = []
asyncio.run(riser_mounts())
upload_parts()
parts = []
asyncio.run(holographic_sights())
upload_parts()
parts = []
asyncio.run(ar_iron_sights())
upload_parts()
parts = []
asyncio.run(magnifiers())
upload_parts()
parts = []
asyncio.run(scopes())
upload_parts()
parts = []
asyncio.run(scope_mounts())
upload_parts()
