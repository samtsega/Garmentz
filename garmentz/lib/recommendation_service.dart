import 'dart:convert';  // For encoding/decoding JSON data
import 'package:http/http.dart' as http;  // To make HTTP requests
import 'package:garmentz/constants.dart';  // Import constants for base URL and other config

class RecommendationService {
  final String baseUrl = Constants.baseUrl;  // Assuming you have defined your base URL in constants.dart

  // Function to fetch recommendations
  Future<List<dynamic>> fetchRecommendations(String userId) async {
    final String apiUrl = '$baseUrl/recommendations';  // Endpoint for recommendations API

    try {
      // Create the HTTP request with the userId
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'userId': userId,  // Send the userId as part of the request payload
        }),
      );

      // If the server returns a successful response (status code 200)
      if (response.statusCode == 200) {
        // Decode the response body and return it as a list of recommendations
        return jsonDecode(response.body) as List<dynamic>;
      } else {
        // If the server did not return a 200 OK response, throw an exception.
        throw Exception('Failed to load recommendations');
      }
    } catch (e) {
      // Handle any exceptions that occur during the API call
      print('Error fetching recommendations: $e');
      return [];
    }
  }
}
