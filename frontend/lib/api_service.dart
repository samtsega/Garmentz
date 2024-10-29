import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/constants.dart';



class ApiService {
  final String baseUrl; // Base URL for the API

  ApiService({required this.baseUrl});

  // Function to fetch recommendations based on clothing item
  Future<List<dynamic>> fetchRecommendations(String clothingItem) async {
    final response = await http.get(Uri.parse('$baseUrl/recommendations?item=$clothingItem'));

    if (response.statusCode == 200) {
      // Parse the JSON data
      return json.decode(response.body);
    } else {
      // Handle error response
      throw Exception('Failed to load recommendations');
    }
  }

  // Function to scan garment and get pricing info
  Future<Map<String, dynamic>> scanGarment(String imagePath) async {
    final request = http.MultipartRequest('POST', Uri.parse('$baseUrl/scan'));

    // Add the image file to the request
    request.files.add(await http.MultipartFile.fromPath('image', imagePath));

    // Send the request and await the response
    final response = await request.send();

    if (response.statusCode == 200) {
      final responseBody = await response.stream.bytesToString();
      return json.decode(responseBody);
    } else {
      // Handle error response
      throw Exception('Failed to scan garment');
    }
  }

  // You can add more API functions as needed
}
