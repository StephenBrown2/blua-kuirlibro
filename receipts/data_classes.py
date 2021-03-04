import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from devtools import debug
from pydantic import BaseModel, HttpUrl


class MainDishImage(BaseModel):
    high_feature: HttpUrl
    medium_feature: HttpUrl
    thumb: HttpUrl


class Image(BaseModel):
    format: str
    type: str
    url: HttpUrl


class Medium(BaseModel):
    url: HttpUrl


class Thumb(BaseModel):
    url: HttpUrl


class MainImage(BaseModel):
    url: HttpUrl
    medium: Medium
    thumb: Thumb


class BadgeImage(BaseModel):
    url: HttpUrl = None
    alt: str = None


class Badge(BaseModel):
    description: str
    id: str
    image: BadgeImage
    label: str
    name: str
    sort_order: int
    type: str


class IngredientName(BaseModel):
    descriptor: str
    quantity: str
    unit: str


class Story(BaseModel):
    description: str
    external_url: Optional[HttpUrl]
    external_url_text: str
    id: int
    is_blog: bool
    main_image: MainImage
    main_image_url: HttpUrl
    product_id: Optional[str]
    relative_sort_order: int
    renderable_main_image_url: HttpUrl
    spree_product: Optional[str]
    status: str
    title: str
    variant_id: Optional[str]
    video_url: HttpUrl


class Ingredient(BaseModel):
    customer_facing_ingredient_name: str
    customer_facing_name: str
    customer_facing_quantity: str
    description: str
    id: int
    name: IngredientName
    renderable_image_url: Optional[str]
    sort_order: int
    stories: List[Story]


class LastDelivery(BaseModel):
    delivered_at: datetime
    recipe_type_id: int


class Names(BaseModel):
    full: str
    main: str
    sub: str


class PrepTime(BaseModel):
    min: Optional[int]
    max: Optional[int]


class Tags(BaseModel):
    cuisine_tag_list: List[str]
    feature_tag_list: List[str]
    main_ingredient_list: List[str]


class Prep(BaseModel):
    min: Optional[int]
    avg: Optional[int]
    max: Optional[int]


class Cook(BaseModel):
    min: Optional[int]
    avg: Optional[int]
    max: Optional[int]


class Overall(BaseModel):
    min: int
    avg: int
    max: int


class Times(BaseModel):
    prep: Prep
    cook: Cook
    overall: Overall


class SubSteps(BaseModel):
    sort_order: int
    text: str


class RecipeSteps(BaseModel):
    id: int
    recipe_id: int
    step_number: int
    step_text: str
    recipe_step_image_url: HttpUrl
    renderable_recipe_step_image_url: HttpUrl
    step_title: str
    sub_steps: List[SubSteps]


class Recipe(BaseModel):
    badges: List[Badge]
    c_main_dish_image: MainDishImage
    calories_per_serving: str
    centered_main_dish_image: MainDishImage
    created_at: datetime
    culinary_number: Optional[str]
    description: str
    guest_chef_name: Optional[str]
    high_menu_thumb_url: HttpUrl
    id: int
    images: List[Image]
    ingredient_image_url: HttpUrl
    ingredients: List[Ingredient]
    is_complete: bool
    is_gluten_free: bool
    is_masked: bool
    last_delivery: LastDelivery
    location: str
    main_title: str
    max_cook_time: Optional[int]
    min_cook_time: Optional[int]
    names: Names
    prep_time: PrepTime
    product_id: int
    product_sku: str
    redirect_url_for_masked: Optional[str]
    renderable_ingredient_image_url: HttpUrl
    renderable_main_dish_image_url: HttpUrl
    renderable_square_hi_res_image_url: HttpUrl
    servings: str
    slug: str
    sort_order: int
    square_hi_res_image_url: HttpUrl
    status: str
    sub_title: str
    tags: Tags
    times: Times
    title: str
    updated_at: datetime
    vegetarian: bool
    recipe_steps: List[RecipeSteps]
    stories: List[Story]


class GeneratedClass(BaseModel):
    recipe: Recipe


recipath = Path("/Users/step7212/git/lab/blua-kuirlibro/api_recipes_23707.json")
recip1 = json.load(recipath.open())
genrep = GeneratedClass(**recip1)
debug(genrep)
