import os
import sys
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# User credentials and part numbers
credentials = {
    "Usuario": "SC74349",
    "Senha": "Caneca050315"
}
pns_for_scraping = ["77994840", "34343424"]

def E_PER(pns_for_scraping, credentials):
   
    print("\n--- 🚀 Starting E-PER Web Scraping ---")
    if not pns_for_scraping:
        print("No part numbers provided.")
        return {}

    print(f"🔍 Checking {len(pns_for_scraping)} part numbers:")
    for pn in pns_for_scraping:
        print(f"  • {pn}")

    username = credentials["Usuario"]
    password = credentials["Senha"]
    scraped_weights = {}

    try:
        with sync_playwright() as p:

            # C:\Users\perna\Desktop\STALLANTIS\DataBase- PFEP\RPA - FIAPE\Modelos copy.json
            # ✅ Use fixed Chromium path
            Chrome_driver_path = Path("C:/Users/perna/Desktop/STALLANTIS/DataBase- PFEP/RPA - FIAPE/Driver")  / "chrome-win" / "chrome.exe"
            chromium_exe =  Chrome_driver_path
            

            if not chromium_exe.exists():
                raise FileNotFoundError(f"❌ Chromium not found at: {chromium_exe}")

            print(f"✅ Chromium binary path: {chromium_exe}")
            print("🌐 Launching browser...")

            browser = p.chromium.launch(headless=False, executable_path=str(chromium_exe))
            page = browser.new_page()

            try:
                # Login
                print("🔐 Logging into E-PER...")
                page.goto("https://eper-ltm.parts.fiat.com/navi?EU=1&eperLogin=0&sso=false&COUNTRY=076&RMODE=DEFAULT&SEARCH_TYPE=codpart&KEY=HOME")
                page.fill("input[name='username']", username)
                page.fill("input[name='password']", password)
                page.select_option("select[name='loginType']", "Fiat AUTO/MyUser/Link.e.entry")
                page.click("input[type='button']")
                page.wait_for_load_state("networkidle", timeout=60000)
                print("✅ Login successful.")
                # Wait for the dropdown to appear
               
               # 1. Click the parent menu item to open the dropdown
                page.click("text=Marca")

                # 2. Locate all items with the "LangHref" class and click the 4th one (index 3)
                # The .nth() method is zero-indexed, so the 4th item is at index 3.
                page.locator(".LangHref").nth(3).click()             


                print("✅ Dropdown option selected.")
                # If you need to select the fourth <li> in that list (as you mentioned “list 4”), you could instead do:

               
                # Hover over menu
                page.hover("text=Marca")

                # Wait for list and click the 4th li > a
                page.click(".MenuDropLists li:nth-child(4) a")
               










               
                
                for pn in pns_for_scraping:
                    print(f"\n🔎 Searching for PN: {pn}")
                    try:
                        page.fill("input[id='fPNumber']", pn[:-1])
                        page.keyboard.press("Enter")
                        page.wait_for_load_state("networkidle", timeout=50000)
                        time.sleep(2)

                        labels = page.locator("td.part_details_label")
                        values = page.locator("td.part_details_value")

                        for i in range(labels.count()):
                            label_text = labels.nth(i).inner_text().strip()

                            if "Peso em gramas:" in label_text:
                                peso_value = values.nth(i).inner_text().strip()
                                peso_kg = float(peso_value.replace(',', '.')) / 1000
                                scraped_weights[pn] = peso_kg
                                print(f"  ✅ {pn}: {peso_value} g → {peso_kg:.3f} kg")
                                break
                        else:
                            print(f"  ⚠️ Peso not found for PN {pn}")

                    except TimeoutError:
                        print(f"  ❌ Timeout searching for PN {pn}")
                    except Exception as e:
                        print(f"  ❌ Error for PN {pn}: {e}")

                    time.sleep(1)

            except Exception as e:
                print(f"❌ Browser interaction error: {e}")
            finally:
                print("🛑 Closing browser...")
                browser.close()

    except Exception as e:
        print(f"❌ Playwright setup error: {e}")

    print("\n✅ Scraping complete.")
    
    return scraped_weights


E_PER(pns_for_scraping, credentials)