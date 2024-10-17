import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart'; // Import for image picking
import 'colors.dart'; // Import your custom colors
import 'home_page.dart'; // Import your home page
import 'recommendations_service.dart'; // Import for recommendations service if needed
import 'image_processing.dart'; // Import for image processing functionality
import 'font.dart'; // Import your fonts file

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Garmentz',
      theme: ThemeData(
        primaryColor: AppColors.primaryColor, // Use your custom primary color
        accentColor: AppColors.accentColor, // Use your custom accent color
        textTheme: TextTheme(
          bodyText1: TextStyle(color: AppColors.secondaryColor), // Example of text styling
        ),
        // Additional theme configurations can go here
      ),
      home: HomePage(), // Set your home page here
    );
  }
}

class HomePage extends StatelessWidget {
  final ImagePicker _picker = ImagePicker(); // Instance of ImagePicker

  Future<void> _pickImage() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.camera);
    if (image != null) {
      // Call your image processing function here
      // Example: await processImage(image.path);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Welcome to Garmentz'),
      ),
      body: Center(
        child: Text(
          'Get an accurate pricing with Garmentz.',
          style: TextStyle(fontSize: 24, color: AppColors.accentColor),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _pickImage, // Call the image picking function
        child: Icon(Icons.camera_alt),
        backgroundColor: AppColors.primaryColor,
      ),
    );
  }
}
