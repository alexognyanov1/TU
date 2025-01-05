# Description: This script is a Flask API that scrapes cost of living data (purchasing power and average salary) from Numbeo website URLs provided in a POST request.  It handles multiple URLs and returns a JSON response with the extracted data or error messages.
# Tags: Web Scraping, API, Numbeo, Cost of Living, Data Extraction, JSON

from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = "https://www.numbeo.com/cost-of-living/compare_cities.jsp"


def get_cost_of_living(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find(
            'table', class_='table_indices_diff limit_size_ad_right')

        purchasing_power_row = table.find_all(
            'tr')
        purchasing_power_text = None

        for row in purchasing_power_row:
            if "Local Purchasing Power" in row.get_text():
                purchasing_power_text = row.get_text(strip=True)
                break

        if purchasing_power_text:

            purchasing_power = purchasing_power_text.split(
                "is")[-1].split("%")[0].strip()
        else:
            purchasing_power = "N/A"

        salary_row = soup.find(
            'td', string="Average Monthly Net Salary (After Tax)")
        if salary_row:

            percentage_cell = salary_row.find_next_sibling(
                'td').find_next_sibling('td').find_next_sibling('td')
            salary_percentage = percentage_cell.get_text(
                strip=True).split("%")[0].strip() + "%"
        else:
            salary_percentage = "N/A"

        return {
            "Local Purchasing Power": purchasing_power,
            "Average Monthly Net Salary (After Tax)": salary_percentage
        }
    except Exception as e:
        return {"error": str(e)}


@app.route('/get_cost_of_living', methods=['POST'])
def get_cost_of_living_api():
    data = request.get_json()
    if not data or not isinstance(data.get('urls'), list):
        return jsonify({"error": "Invalid input. Provide a JSON object with an array of URLs under 'urls' key."}), 400

    results = []
    for url in data['urls']:
        if not url.startswith(BASE_URL):
            results.append({"error": "Invalid URL"})
        else:
            result = get_cost_of_living(url)
            results.append(result)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=3008, host='0.0.0.0')