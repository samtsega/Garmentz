import 'package:flutter/material.dart';
import 'home_screen.dart';               // Import your home screen
import 'recommendation_screen.dart';    // Import recommendation screen
import 'settings_screen.dart';           // Import settings screen
import 'constants.dart';                 // Import constants file

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppConstants.appTitle,
      theme: ThemeData(
        primarySwatch: Colors.blue,          // Primary color for the app
        accentColor: AppConstants.secondaryColor, // Accent color from constants
        textTheme: TextTheme(
          headline1: AppConstants.titleTextStyle, // Title text style
          bodyText1: AppConstants.bodyTextStyle,   // Body text style
        ),
      ),
      home: HomeScreen(),                        // Set the home screen of the app
      routes: {
