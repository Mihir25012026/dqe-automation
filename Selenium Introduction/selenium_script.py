from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv


class DriverManager:

    def __enter__(self):
        print("Starting browser...")

        options = Options()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing browser...")
        self.driver.quit()


if __name__ == "__main__":
    with DriverManager() as driver:

        # Open local HTML
        file_path = "file:///C:/Users/Mangesh_Kapgate/report.html"
        driver.get(file_path)

        # Wait for table
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "table"))
        )

        # Locate table
        table = driver.find_element(By.CLASS_NAME, "table")
        columns = table.find_elements(By.CLASS_NAME, "y-column")

        headers = []
        column_data = []

        # Extract data column-wise
        for col in columns:
            header = col.find_element(By.ID, "header").text.strip()
            headers.append(header)

            cells = col.find_elements(By.CLASS_NAME, "cell-text")
            values = [c.text for c in cells if c.text != header]
            column_data.append(values)

        # Convert columns → rows
        rows = list(zip(*column_data))

        # Save CSV
        with open("table.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print("table.csv created successfully!")

        chart = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pielayer")))
        chart.screenshot("screenshot0.png")

        labels = chart.find_elements(By.CSS_SELECTOR, "text.slicetext[data-notex='1']")

        chart_data = []

        for label in labels:
            tspans = label.find_elements(By.TAG_NAME, "tspan")
            category = tspans[0].text
            value = tspans[1].text
            chart_data.append([category, value])
            print(chart_data)

        with open("doughnut0.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Facility Type", "Value"])
            writer.writerows(chart_data)

        legend = driver.find_element(By.CLASS_NAME, "scrollbox")
        items = legend.find_elements(By.CLASS_NAME, "traces")

        for i, item in enumerate(items):

            try:
                print(f"Clicking filter {i}")

                # click filter
                item.click()

                # wait for chart update
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pielayer"))
                )

                # small delay (important for UI update)
                import time

                time.sleep(1)

                # screenshot
                if chart.size['width'] > 0 and chart.size['height'] > 0:
                    chart.screenshot(f"screenshot{i + 1}.png")
                else:
                    print(f"Skipping screenshot for filter {i} (chart empty)")

                # extract data again
                labels = chart.find_elements(By.CSS_SELECTOR, "text.slicetext[data-notex='1']")

                chart_data = []

                for label in labels:
                    tspans = label.find_elements(By.TAG_NAME, "tspan")
                    category = tspans[0].text
                    value = tspans[1].text
                    chart_data.append([category, value])

                # save CSV
                with open(f"doughnut{i + 1}.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Facility Type", "Value"])
                    writer.writerows(chart_data)

            except Exception as e:
                print(f"Error on filter {i}: {e}")
