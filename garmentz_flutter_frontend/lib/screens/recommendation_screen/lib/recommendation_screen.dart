import 'package:flutter/material.dart';
import 'recommendation_service.dart'; // Import the service class

class RecommendationsPage extends StatefulWidget {
  final String clothingItem; // This will be the item to get recommendations for

  RecommendationsPage({required this.clothingItem});

  @override
  _RecommendationsPageState createState() => _RecommendationsPageState();
}

class _RecommendationsPageState extends State<RecommendationsPage> {
  late Future<List<dynamic>> _recommendations;

  @override
  void initState() {
    super.initState();
    // Fetch recommendations when the page is initialized
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
                return Card(
                  margin: EdgeInsets.all(8),
                  child: ListTile(
                    title: Text(recommendations[index]['name']),
                    subtitle: Text("\$${recommendations[index]['price']}"),
                    trailing: IconButton(
                      icon: Icon(Icons.favorite_border),
                      onPressed: () {
                        // Implement favorite functionality here if needed
                      },
                    ),
                  ),
                );
              },
            );
          }
        },
      ),
    );
  }
}
