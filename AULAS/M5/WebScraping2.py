import requests
from bs4 import BeautifulSoup


def scrape_python_blog():
    url = 'https://www.python.org/blogs/'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.select('li.medium-widget.blog-widget')

    if not posts:
        print("Nenhum post encontrado.")
        return

    for post in posts:
        link_tag = post.find('a')
        if not link_tag:
            continue

        title = link_tag.get_text(strip=True)
        link = link_tag.get('href', '')

        if not title or not link:
            continue

        print(f"Título: {title}")
        print(f"Link: {link}")
        print("-" * 40)


if __name__ == '__main__':
    scrape_python_blog()










































