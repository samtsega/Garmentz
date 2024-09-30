import 'package:flutter/material.dart';

class ClothingCard extends StatelessWidget
{
    final String title;
    final String imageUrl;
    final String price; ClothingCard({required this.title, required this.imageUrl, required this.price});

    @override
    Widget build(BuildContext context) {
      return Card(
        elevation: 4,
        margin: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
        child: ListTile(
              leading: Image.network(imageUrl, width: 50, height: 50),
              title: Text(title, style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Price: $price'),
              trailing: Icon(Icons.arrow_forward),
            ),
      );
    }
}