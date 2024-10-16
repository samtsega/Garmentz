import 'package:flutter/material.dart';
import 'recommendations_page.dart'; // Import the recommendations page

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Garmentz Home"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "Welcome to Garmentz!",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Navigate to the recommendations page
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => RecommendationsPage(clothingItem: "T-shirt"), // Example item
                  ),
                );
              },
              child: Text("Get Recommendations"),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Implement garment scanning functionality here
                // You might navigate to a scanning page or show a scanner widget
              },
              child: Text("Scan Garment"),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            IconButton(
              icon: Icon(Icons.home),
              onPressed: () {
                // Home action
              },
            ),
            IconButton(
              icon: Icon(Icons.settings),
              onPressed: () {
                // Navigate to settings or other options
              },
            ),
          ],
        ),
      ),
    );
  }
}
