from ebay_service import fetch_ebay_data
from depop_service import fetch_depop_data
from vestiaire_service import fetch_vestiaire_data
from grailed_service import fetch_grailed_data
from farfetch_service import fetch_farfetch_data
from saksfifth_service import fetch_saksfifth_data
from fashionphile_service import fetch_fashionphile_data
from amazon_service import fetch_amazon_data
from ssense_service import fetch_ssense_data

def aggregate_recommendations(query, max_items=5):
    """ Aggregate clothing recommendations from multiple platforms based on a search query.
        Args: query (str): The search term to find related clothing items.
        max_items (int): The maximum number of items to return from each platform.
        Returns: dict: A dictionary containing aggregated recommendations from various platforms. """

recommendations = {}

# Fetch recommendations from various services

ebay_recommendations = fetch_ebay_data(query)[:max_items]
depop_recommendations = fetch_depop_data(query)[:max_items]
vestiaire_recommendations = fetch_vestiaire_data(query)[:max_items]
grailed_recommendations = fetch_grailed_data(query)[:max_items]
farfetch_recommendations = fetch_farfetch_data(query)[:max_items]
saksfifth_recommendations = fetch_saksfifth_data(query)[:max_items]
fashionphile_recommendations = fetch_fashionphile_data(query)[:max_items]
amazon_recommendations = fetch_amazon_data(query)[:max_items]
ssense_recommendations = fetch_ssense_data(query)[:max_items]

# Compile results from each service
recommendations['ebay'] = ebay_recommendations
recommendations['depop'] = depop_recommendations
recommendations['vestiaire'] = vestiaire_recommendations
recommendations['grailed'] = grailed_recommendations
recommendations['farfetch'] = farfetch_recommendations
recommendations['saksfifth'] = saksfifth_recommendations
recommendations['fashionphile'] = fashionphile_recommendations
recommendations['amazon'] = amazon_recommendations
recommendations['ssense'] = ssense_recommendations
return recommendations

def filter_recommendations_by_brand(recommendations, brand):
""" Filter recommendations to only include items from a specific brand.
        Args: recommendations (dict): Aggregated recommendations from all platforms.
        brand (str): The brand to filter by.
        Returns: dict: A filtered dictionary containing only recommendations for the specified brand. """

filtered_recommendations = {}
for platform, items in recommendations.items():
    filtered_recommendations[platform] = [item for item in items if item['brand'].lower() == brand.lower()]
return filtered_recommendations

def recommend_complementary_items(query, brand=None, max_items=5):
    """ Recommend complementary clothing items based on the given query, and optionally filter by brand.
        Args: query (str): The search query for the main clothing item.
        brand (str, optional): Brand to filter recommendations. Defaults to None. max_items (int, optional): The maximum number of items per platform. Defaults to 5.
        Returns: dict: Aggregated recommendations from different platforms, optionally filtered by brand. """

recommendations = aggregate_recommendations(query, max_items)
if brand: recommendations = filter_recommendations_by_brand(recommendations, brand)

return recommendations