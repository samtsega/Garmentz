import 'image_service.dart';

class SomeScreen extends StatefulWidget {
  @override
  _SomeScreenState createState() => _SomeScreenState();
}

class _SomeScreenState extends State<SomeScreen> {
  final ImageService _imageService = ImageService();
  File? _imageFile;

  void _pickImage() async {
    final selectedImage = await _imageService.pickImageFromGallery();
    setState(() {
      _imageFile = selectedImage;
    });
  }

  void _captureImage() async {
    final capturedImage = await _imageService.captureImageWithCamera();
    setState(() {
      _imageFile = capturedImage;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Image Service Example"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _imageService.displayImage(_imageFile),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: Text("Pick Image from Gallery"),
            ),
            ElevatedButton(
              onPressed: _captureImage,
              child: Text("Capture Image with Camera"),
            ),
          ],
        ),
      ),
    );
  }
}
