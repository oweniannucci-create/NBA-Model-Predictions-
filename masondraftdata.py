import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from pandasgui import show


def fetch_salary_cap_history():
    url = 'https://www.basketball-reference.com/contracts/salary-cap-history.html'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/117.0.0.0 Safari/537.36'
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    table = soup.find('table', {'id': 'salary_cap_history'})

    df = pd.read_html(StringIO(str(table)))[0]

    df.columns = ['Year', 'Salary Cap', 'Luxury Tax Threshold', 'Apron']

    for col in ['Salary Cap', 'Luxury Tax Threshold', 'Apron']:
        df[col] = df[col].replace({r'\$': '', ',': ''}, regex=True).astype(float)

    df['Year'] = df['Year'].str[:4].astype(int)
    show(df)
    return df


def main():
    salary_cap_df = fetch_salary_cap_history()
    print(salary_cap_df)
    salary_cap_df.to_csv('nba_salary_cap_history.csv', index=False)
    print("Saved salary cap history to 'nba_salary_cap_history.csv'")


if __name__ == '__main__':
    main()

