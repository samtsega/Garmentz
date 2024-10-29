import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';

// Define a model class for recommendations
class Recommendation {
  final String title;
  final String imageUrl;
  final double price;

  Recommendation({required this.title, required this.imageUrl, required this.price});

  factory Recommendation.fromJson(Map<String, dynamic> json) {
    return Recommendation(
      title: json['title'] as String,
      imageUrl: json['imageUrl'] as String,
      price: json['price'] as double,
    );
  }
}

// Function to fetch recommendations from the backend
Future<List<Recommendation>> fetchRecommendations(String imagePath) async {
  final response = await http.post(
    Uri.parse('YOUR_BACKEND_API_URL/recommendations'), // Replace with your API URL
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'imagePath': imagePath, // Send the image path to your backend for processing
    }),
  );

  if (response.statusCode == 200) {
    // Parse the JSON response
    final List<dynamic> recommendationsJson = json.decode(response.body);
    return recommendationsJson.map((json) => Recommendation.fromJson(json)).toList();
  } else {
    throw Exception('Failed to load recommendations');
  }
}

// Widget to display recommendations
class RecommendationsList extends StatelessWidget {
  final String imagePath;

  RecommendationsList({required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Recommendation>>(
      future: fetchRecommendations(imagePath), // Fetch recommendations
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator()); // Loading indicator
        } else if (snapshot.hasError) {
          return Center(child: Text('Error: ${snapshot.error}')); // Error message
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(child: Text('No recommendations found.')); // No data message
        }

        // Display the list of recommendations
        final recommendations = snapshot.data!;
        return ListView.builder(
          itemCount: recommendations.length,
          itemBuilder: (context, index) {
            final recommendation = recommendations[index];
            return ListTile(
              leading: Image.network(recommendation.imageUrl),
              title: Text(recommendation.title),
              subtitle: Text('\$${recommendation.price.toStringAsFixed(2)}'),
              onTap: () {
                // Handle item tap, e.g., navigate to detail page
              },
            );
          },
        );
      },
    );
  }
}
