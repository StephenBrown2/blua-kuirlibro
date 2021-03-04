from datetime import timedelta
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class RecipeParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")

    def __repr__(self):
        return (
            "<"
            + " ".join(
                [
                    "ParsedRecipe",
                    f"name={self.name!r}",
                    f"len(ingredients)={len(self.ingredients)!r}",
                    f"tools={self.tools!r}",
                    f"total_time={self.total_time!r}",
                    f"yields={self.yields!r}",
                    f"tags={self.tags!r}",
                    f"steps={[s['title'] for s in self.steps]!r}",
                ]
            )
            + ">"
        )

    @property
    def name(self):
        """
        Returns a str of the recipe name
        """
        return (
            self.soup.find("h1", class_="ba-recipe-title__main").text.strip()
            + " "
            + self.soup.find("h2", class_="ba-recipe-title__sub").text.strip()
        )

    @property
    def nutrition_label(self):
        return self.soup.find("a", id="recipe-nutrition-label-link").attrs["href"]

    @property
    def ingredients(self):
        """
        Returns a list of ingredients

        ['1 pound of ground beef',
        'lots of veggies', ...]
        """
        return [
            x.text.replace("\n", " ").strip()
            for x in self.soup.find_all(
                "li", class_="ba-info-list__item", itemprop="recipeIngredient"
            )
        ]

    @property
    def tools(self):
        return [
            x.text.strip() for x in self.soup.find_all("a", class_="js-ToolModalLink")
        ]

    @property
    def total_time(self):
        return self.soup.find("span", class_="total-time").text

    @property
    def total_timedelta(self):
        regex = re.compile(
            r"""^P(
                ((?P<years>[0-9]+)Y)?
                ((?P<months>[0-9]+)M)?
                ((?P<days>[0-9]+)D)?
            )?
            (T
                ((?P<hours>[0-9]+)H)?
                ((?P<minutes>[0-9]+)M)?
                ((?P<seconds>[0-9]+)S)?
        )?$""",
            re.X,
        )
        match = re.search(
            regex, self.soup.find("span", itemprop="totalTime").attrs["content"]
        )
        return timedelta(
            hours=int(match.group("hours") or 0),
            minutes=int(match.group("minutes") or 0),
            seconds=int(match.group("seconds") or 0),
        )

    @property
    def yields(self):
        return (
            self.soup.find("span", itemprop="recipeYield")
            .parent.text.replace("\n", " ")
            .strip()
        )

    @property
    def tags(self):
        return [
            x.text.strip()
            for x in self.soup.find_all("div", class_="culinary-badge-name")
        ]

    @property
    def steps(self):
        """
        Returns a list of the steps of the recipe

        [
            {
                'number': '1',
                'title': 'Step title',
                'steps': ['This is the first sentence',
                          'This is the second sentence',
                          ],
                'image': 'https://media.blueapron.com/recipes/...'
            },
            {
                'number': '2':
                'title': 'Step title',
                'steps': ['This is the first', ...],
                'image': 'https://media.blueapron.com/recipes/...'
            }
        ]
        """
        recipe = []
        # get the recipe step blocks
        instructions = self.soup.find("section", class_="recipe-instructions")
        numbers = instructions.find_all("span", class_="step-number")
        titles = instructions.find_all("span", class_="step-title")
        texts = instructions.find_all("div", class_="step-txt")
        imgs = instructions.find_all("img", class_="img-max")
        for i in range(len(numbers)):
            recipe.append(
                {
                    "number": int(numbers[i].text),
                    "title": titles[i].text.strip().strip(": "),
                    "steps": texts[i].text.strip().replace("\xa0", " ").split(". "),
                    "image": (
                        urlparse(imgs[i].attrs["src"])._replace(query=None).geturl()
                    ),
                }
            )
        return recipe
