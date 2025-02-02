import 'package:flutter/material.dart';
import 'colors.dart'; // Import your custom colors
import 'font.dart'; // Import your fonts file

class AppConstants {
  // API Base URL
  static const String apiBaseUrl = 'garmentz.ngrok.app ';

 // Image reference for logos or icons
static const AssetImage logoImage = AssetImage('assets/logo.png');


  // Color Constants
  static const Color primaryColor = Color(E5989B);
  static const Color secondaryColor = Color(FFB4A2);
  static const Color accentColor = Color(FFCDB2);

  // Text Styles
  static const TextStyle titleTextStyle = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: Colors.black,
  );

  static const TextStyle bodyTextStyle = TextStyle(
    fontSize: 16,
    color: Colors.black87,
  );

  // Padding Constants
  static const double defaultPadding = 16.0;
  static const double smallPadding = 8.0;
  static const double largePadding = 32.0;

  // Other constants
  static const int maxImageSize = 5 * 1024 * 1024; // 5 MB
  static const String appTitle = 'Garmentz';
}

