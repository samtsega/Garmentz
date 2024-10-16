import 'package:flutter/material.dart';
import 'recommendation_service.dart'; // Import the service class here

class RecommendationsPage extends StatefulWidget {
  final String clothingItem; // Pass the clothing item (from scanned image, etc.)

  RecommendationsPage({required this.clothingItem});

  @override
  _RecommendationsPageState createState() => _RecommendationsPageState();
}

class _RecommendationsPageState extends State<RecommendationsPage> {
  late Future<List<dynamic>> _recommendations;

  @override
  void initState() {
    super.initState();
    _recommendations = RecommendationService().fetchRecommendations(widget.clothingItem);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Clothing Recommendations"),
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _recommendations,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error loading recommendations"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text("No recommendations found"));
          } else {
            final recommendations = snapshot.data!;
            return ListView.builder(
              itemCount: recommendations.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(recommendations[index]['name']),  // Customize based on your API response
                  subtitle: Text("\$${recommendations[index]['price']}"),
                );
              },
            );
          }
        },
      ),
    );
  }
}
