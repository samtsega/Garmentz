import 'package:flutter/material.dart';
import 'font.dart'; // Import your fonts file

// A custom button widget
class CustomButton extends StatelessWidget {
  final String text;                  // The text to display on the button
  final VoidCallback onPressed;       // The callback function to execute when the button is pressed
  final Color color;                  // The background color of the button
  final Color textColor;              // The color of the button text
  final double elevation;              // The elevation of the button (shadow)
  final double borderRadius;           // The radius of the button corners

  // Constructor with required and optional parameters
  const CustomButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.color = Colors.black,          // Default color
    this.textColor = Colors.white,     // Default text color
    this.elevation = 2.0,              // Default elevation
    this.borderRadius = 8.0,           // Default border radius
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed, // Callback when the button is pressed
      style: ElevatedButton.styleFrom(
        primary: color,                  // Background color
        onPrimary: textColor,            // Text color
        elevation: elevation,            // Shadow elevation
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(borderRadius), // Rounded corners
        ),
        padding: EdgeInsets.symmetric(vertical: 15.0, horizontal: 20.0), // Padding
      ),
      child: Text(
        text,
        style: TextStyle(fontSize: 16.0), // Text style
      ),
    );
  }
}
