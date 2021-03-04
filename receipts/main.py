from argparse import ArgumentParser
import httpx
from parser import RecipeParser
from models import Recipe
from devtools import debug
parser = ArgumentParser()
parser.add_argument("--slug", action="store", dest="slug", type=str, help="Recipe slug")
args = parser.parse_args()

# Weekly menu json: https://www.blueapron.com/api/recipes/on_the_menu
# Actual API: https://www.blueapron.com/api/recipes/23707
# Error result: {
#   "errors": {
#     "base": [
#       "Couldn't find Recipe with 'id'=23708 [WHERE \"recipes\".\"status\" = ?]"
#     ]
#   }
# }


with httpx.Client(base_url="https://www.blueapron.com/recipes/") as client:
    print(f"requesting {args.slug}")
    res = client.get(args.slug)
    # print(f"Got {res.status_code} from {res.url}")
    if "Full recipe coming soon" in res.text:
        print("Full recipe coming soon...")
    else:
        rec = RecipeParser(res.text)
        recipe = Recipe(
            name=rec.name,
            external_id=args.slug,
            ingredients=rec.ingredients,
            tools=rec.tools,
            steps=rec.steps,
        )
        debug(recipe)
