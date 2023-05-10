from bs4 import BeautifulSoup

with open("pagina.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Encontrar todos los elementos <a> con el atributo "href" que comienza con "http"
links = soup.find_all("a", href=lambda href: href and href.startswith("http"))

# Imprimir los enlaces encontrados
for link in links:
    print(link.get("href"))