 import 'package:flutter_flux/flutter_flux.dart';
 import 'dart:convert'; // Store to hold the recommendation data class RecommendationStore extends Store {

    List<Map<String, String>>
 _recommendations = []; // Getter to access the recommendations list
    List<Map<String, String>> get recommendations => _recommendations;

    RecommendationStore() { // Listen to the fetchRecommendationsAction and fetch data
 triggerOnAction(fetchRecommendationsAction, _handleFetchRecommendations); } // Function to handle fetching of recommendations

  Future<void> _handleFetchRecommendations(String imagePath) async { // Simulate API call - replace with actual API call await
  Future.delayed(Duration(seconds: 2)); // Simulate network delay

// Simulated response from API

List<Map<String, String>> response = [
    {
        'title': 'Stylish Jacket',
        'price': '\$120',
        'imageUrl': 'https://example.com/jacket.jpg'
       },
       {
        'title': 'Cool T-Shirt',
        'price': '\$40',
        'imageUrl': 'https://example.com/tshirt.jpg'
       },
     ];

     // Update the state with new recommendations
        _recommendations = response;

// Notify listeners about the state update
    trigger();
   }
 }

// Initialize the recommendation store

final StoreToken recommendationStoreToken = StoreToken(RecommendationStore());
void initializeRecommendationStore() {
    // Initialize the store so it's ready for use
    registerStore(recommendationStoreToken, RecommendationStore());
}