import requests

# Headers con el User-Agent de Chrome
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


# Hacer una solicitud GET a una URL
# url = 'https://www.google.com/search?q=rafael+ausejo+prieto&source=hp&ei=XnA0ZP2yFKCvkdUP85asiAk&iflsig=AOEireoAAAAAZDR-bu6FSx3Mb0vgN6ugNl0_QFndiSIc&ved=0ahUKEwj92e28kqD-AhWgV6QEHXMLC5EQ4dUDCAs&uact=5&oq=rafael+ausejo+prieto&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEIAEOggILhCPARDqAjoICAAQjwEQ6gI6DgguEIAEELEDEIMBENQCOhQILhCABBCxAxCDARDHARDRAxDUAjoLCC4QgAQQsQMQgwE6CwgAEIoFELEDEIMBOhEILhCABBCxAxCDARDHARDRAzoLCC4QigUQsQMQgwE6CAgAEIAEELEDOgsIABCABBCxAxCDAToICC4Q1AIQgAQ6CAguEIAEELEDOgsILhCABBCxAxDUAjoFCC4QgAQ6CAguEIAEENQCOgoILhCABBCxAxAKOgcILhCABBAKOg0ILhCABBDHARCvARAKOgYIABAWEB46CggAEBYQHhAPEApQ9gNY-RdguhloAXAAeACAAXaIAdgLkgEEMTkuMZgBAKABAbABCg&sclient=gws-wiz'
url ="https://www.google.com/search?q=filetype:pdf+site:sepiocyber.com&num=100"
response = requests.get(url, headers=headers)


# Verificar si la solicitud fue exitosa (código 200)
if response.status_code == 200:
    # Imprimir la respuesta en formato de texto
    print(response.text)
    with open("pagina.html", "w", encoding="utf-8") as f:
        f.write(response.text)
else:
    # Imprimir el código de estado de la respuesta en caso de error
    print(f"Error {response.status_code}: {response.reason}")


