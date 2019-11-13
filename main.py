"""Short script to scrape Google Scholar results for evaluating different ML algorithms
by count. Update ALGORITHM_LIST and QUERY_BASE variables according to your needs.
"""
import operator
import re
import sys

import lxml.html
import requests

ALGORITHM_LIST = [
    "Linear Regression", "Logistic Regression", "Decision Tree", "SVM",
    "Naive Bayes", "kNN", "K-Means", "Random Forest",
    "Dimensionality Reduction Algorithms", "Gradient Boosting algorithms",
    "GBM", "XGBoost", "LightGBM", "CatBoost"
]
QUERY_BASE = "machine learning network optimization lte SON parameter"


def main():
    """Main function of this program.
    """
    results = {}
    for ml_alg in ALGORITHM_LIST:
        query = " ".join([QUERY_BASE, ml_alg])
        url = "https://scholar.google.fi/scholar?hl=fi&as_sdt=0%2C5&q={}&btnG=".format(
            query.replace(" ", "+"))
        res = requests.get(url)
        tree = lxml.html.fromstring(res.text)
        results_element = tree.xpath('//*[@id="gs_ab_md"]/div')
        if results_element and results_element[0]:
            total_publications = re.findall("\\d+", results_element[0].text)
            results[ml_alg] = int("".join(total_publications))
    # To align end results print
    longest_alg_length = len(max(ALGORITHM_LIST, key=len))
    if len(results) == 0:
        print("Somehow you did not get any results. " +
              "Check if Google is suspicious of you being a bot.")
        sys.exit(1)
    print("Results for scraping using base query of: \"{}\"".format(QUERY_BASE))
    print("{:<{align_left}}\t{:>8}".format("ML algorithm",
                                           "Number of publications", align_left=longest_alg_length))
    print("-"*(longest_alg_length + 5 + len("Number of publications")))
    # Sort results by highest count.
    for result in sorted(results.items(), key=operator.itemgetter(1), reverse=True):
        print("{:<{align_left}}\t{:>8}".format(
            result[0], result[1], align_left=longest_alg_length))
    sys.exit(0)


if __name__ == "__main__":
    main()
