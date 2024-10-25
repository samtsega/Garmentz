import 'package:flutter/material.dart';
import 'models/recommendation.dart';  // Import the Recommendation model

class RecommendationsList extends StatelessWidget {
  final List<Recommendation> recommendations;

  // Constructor to receive the list of recommendations
  RecommendationsList({required this.recommendations});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: recommendations.length,  // Number of items in the list
      itemBuilder: (context, index) {
        final recommendation = recommendations[index];  // Get the current recommendation

        return Card(
          margin: EdgeInsets.symmetric(vertical: 10.0, horizontal: 15.0),
          child: ListTile(
            leading: recommendation.imageUrl.isNotEmpty
                ? Image.network(recommendation.imageUrl, width: 50, height: 50, fit: BoxFit.cover)
                : Icon(Icons.image, size: 50),  // Fallback if no image URL
            title: Text(recommendation.itemName, style: TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Price: \$${recommendation.price.toStringAsFixed(2)}'),
                Text('Brand: ${recommendation.brand}'),
                Text('Wear Status: ${recommendation.wearStatus}'),
                Text('Age: ${recommendation.age} years old'),
              ],
            ),
            trailing: Icon(Icons.arrow_forward),
            onTap: () {
              // Handle tap (e.g., navigate to a detailed screen)
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => RecommendationDetailScreen(recommendation: recommendation),
                ),
              );
            },
          ),
        );
      },
    );
  }
}
