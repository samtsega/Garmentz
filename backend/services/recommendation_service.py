from backend.api import saksfifth_data
from ebay_service import fetch_ebay_data
from depop_service import fetch_depop_data
from vestiare_service  import fetch_vestiaire_data
from grailed_service import fetch_grailed_data
from farfetch_service import fetch_farfetch_data
from saksfifth_service import fetch_saksfifth_data
from fashionphile_service import fetch_fashionphile_data
from amazon_service import fetch_amazon_data
from ssense_service import fetch_ssense_data

def get_recommendations(item_name, platforms=None):
    """ Fetch similar items from various platforms based on the item_name.
    Args: item_name (str): The name of the item to get recommendations for. platforms (list): Optional list of platforms to search from, defaults to all platforms.
    Returns: dict: A dictionary containing recommendations from each platform. """

    # Default platforms to search from if none are provided
    if platforms is None:
        platforms = ['ebay', 'amazon', 'ssense', 'fashionphile', 'saksfifth', 'depop', 'vestiaire', 'grailed', 'farfetch']
        recommendations = {}

    # Fetch recommendations from each platform
    if 'ebay' in platforms:
        ebay_data = fetch_ebay_data(item_name)
        recommendations['ebay'] = ebay_data

    if 'amazon' in platforms:
        amazon_data = fetch_amazon_data(item_name)
        recommendations['amazon'] = amazon_data

    if 'depop' in platforms:
        depop_data = fetch_depop_data(item_name)
        recommendations['depop'] = depop_data

    if 'vestiaire' in platforms:
        vestiaire_data = fetch_vestiaire_data(item_name)
        recommendations['vestiaire'] = vestiaire_data

    if 'grailed' in platforms:
        grailed_data = fetch_grailed_data(item_name)
        recommendations['grailed'] = grailed_data

    if 'farfetch' in platforms:
        farfetch_data = fetch_farfetch_data(item_name)
        recommendations['farfetch'] = farfetch_data

    if 'saksfifth' in platforms:
            saksfifth_data = fetch_saksfifth_data(item_name)
            recommendations['saksfifth'] = saksfifth_data

    if 'fashionphile' in platforms:
        fashionphile_data = fetch_fashionphile_data(item_name)
        recommendations['fashionphile'] = fashionphile_data

    return recommendations

def filter_recommendations(recommendations, max_price=None, min_price=None, condition=None):
    """ Filters the recommendations based on price range and condition.
    Args: recommendations (dict): The dictionary containing recommendations from various platforms. max_price (float): The maximum price filter. min_price (float): The minimum price filter. condition (str): The condition filter (e.g., "new", "used").
    Returns: dict: A filtered dictionary of recommendations. """

    filtered_recommendations = {}
    for platform, items in recommendations.items():
        filtered_items = []
        for item in items: # Apply price filtering
            if max_price and item['price'] > max_price:
                continue
            if min_price and item['price'] < min_price:
                continue

            # Apply condition filtering (if the item data contains condition info)
            if condition and item.get('condition') and item['condition'].lower() != condition.lower():
                continue

            filtered_items.append(item)

        filtered_recommendations[platform] = filtered_items

    return filtered_recommendations
