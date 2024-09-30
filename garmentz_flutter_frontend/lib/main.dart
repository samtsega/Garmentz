import 'package:flutter/material.dart';
import 'package:flutter_flux/flutter_flux.dart'; // Flux package for state management
import 'screens/recommendation_store/image_picker_screen.dart';
import 'stores/recommendation_store/recommendation_store.dart'; // Importing the store for recommendation state
void main() { // Initialize Flux stores before running the app
    initializeRecommendationStore(); runApp(MyApp());
}

class MyApp extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            title: 'Recommendations by Garmentz',
            theme: ThemeData(
                primarySwatch: Colors.teal,
                visualDensity: VisualDensity.adaptivePlatformDensity,
                textTheme: TextTheme( headline6: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                bodyText2: TextStyle(fontSize: 16),
                ),
             ),
             home: ImagePickerScreen(), // Main screen with image picker and recommendation feature
             );
            }
           }