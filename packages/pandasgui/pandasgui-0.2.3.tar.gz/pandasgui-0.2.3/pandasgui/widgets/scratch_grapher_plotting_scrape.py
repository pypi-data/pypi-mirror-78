def generate_schemas_full():
    from pandasgui.widgets.grapher_plotting import schemas

    schemas_full = []

    from bs4 import BeautifulSoup
    from urllib.request import urlopen

    url = "https://plotly.com/python-api-reference/plotly.express.html"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find(id="plotly-express-high-level-interface-for-data-visualization").find("tbody").find_all("tr")

    # Iterate over rows in table of links to each plotly express plot
    for row in rows:
        plot_name = row.find_all("td")[0].find("a").text
        if plot_name not in [schema.name for schema in schemas]:
            continue

        plot_url = f"https://plotly.com/python-api-reference/generated/plotly.express.{plot_name}.html"
        plot_page = urlopen(plot_url)
        plot_html = plot_page.read().decode("utf-8")
        plot_soup = BeautifulSoup(plot_html, "html.parser")
        parameters = plot_soup.find('dl', {"class": "field-list simple"}).findChildren(recursive=False)[1].find(
            'ul').findChildren('li', recursive=False)

        schema = {}
        schema['name'] = plot_name
        schema['args'] = []
        # Iterate over table of arguments for this plotly express plot
        for param in parameters:
            arg_description = param.text
            arg_name = arg_description.split(' ', 1)[0]
            schema['args'].append({"arg_name": arg_name})

        schemas_full.append(schema)

    return schemas_full


schemas_full = generate_schemas_full()
print(schemas_full)
