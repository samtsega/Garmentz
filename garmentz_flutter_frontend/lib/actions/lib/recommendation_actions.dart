import 'package:flutter_flux/
flutter_flux.dart'';

// Define an action to trigger the clothing recommendations fetching process
final Action<String>
fetchRecommendationsAction =
Action<String>();

// This action will receive the image path (as a String) to make API requests
void fetchRecommendations(String imagePath) {

// Dispatch the action, passing the image path (or other necessary data)
fetchRecommendationsAction(imagePath);
}