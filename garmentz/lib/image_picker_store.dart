import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class ImagePickerWidget extends StatefulWidget {
  @override
  _ImagePickerWidgetState createState() => _ImagePickerWidgetState();
}

class _ImagePickerWidgetState extends State<ImagePickerWidget> {
  File? _imageFile;
  final ImagePicker _picker = ImagePicker();

  // Function to pick an image from the gallery
  Future<void> _pickImageFromGallery() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      setState(() {
        _imageFile = File(image.path);
      });
    }
  }

  // Function to capture an image using the camera
  Future<void> _captureImageWithCamera() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.camera);
    if (image != null) {
      setState(() {
        _imageFile = File(image.path);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // Display the picked image or a placeholder
        _imageFile == null
            ? Text("No image selected")
            : Image.file(_imageFile!, height: 200, width: 200),

        SizedBox(height: 20),

        // Buttons for picking and capturing images
        ElevatedButton(
          onPressed: _pickImageFromGallery,
          child: Text("Pick Image from Gallery"),
        ),
        ElevatedButton(
          onPressed: _captureImageWithCamera,
          child: Text("Capture Image with Camera"),
        ),
      ],
    );
  }
}
