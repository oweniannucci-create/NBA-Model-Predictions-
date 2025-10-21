from bs4 import BeautifulSoup

# Specify the path to your local HTML file
file_path = 'Data/NBA Trades.html'  # Replace with the actual path to your HTML file
traded_players={}
try:
    # Open the HTML file in read mode with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # To find all paragraphs and print their text:
    trade_tables = soup.find_all(class_="tradetable")
    print("\nParagraphs:")
    for table in trade_tables:
        trade_data = table.find_all(class_='tradedata')
        for trade in trade_data:
            players = trade.find_all(class_="tradeplayer")
            for player in players:
                traded_players[trade.find_next('span').text.replace(" acquires","")].append(player.find_next('a').text)

    print(traded_players)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")