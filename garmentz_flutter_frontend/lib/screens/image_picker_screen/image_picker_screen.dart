 import 'package:flutter/material.dart';
 import 'package:image_picker/image_picker.dart';
 import 'dart:io';
 import 'package:flutter_flux/flutter_flux.dart';
 import '../actions/recommendation_store/recommendation_actions.dart';
 import '../stores/recommendation_store/recommendation_store.dart';
 import '../widgets/recommendation_store/clothing_card.dart';

class ImagePickerScreen extends StatefulWidget {
    @override _ImagePickerScreenState createState() => _ImagePickerScreenState();
}

class _ImagePickerScreenState extends State<ImagePickerScreen> with StoreWatcherMixin<ImagePickerScreen> {
    File? _image; // Holds the selected image
    final ImagePicker _picker = ImagePicker();
    late RecommendationStore _recommendationStore; // Store for recommendations

    @override
    void initState() {
        super.initState();
        // Register the store to listen for changes
        _recommendationStore = listenToStore(recommendationStoreToken);
    }

        // Pick image from gallery
        Future<void> _pickImageFromGallery() async {
            final pickedFile = await _picker.pickImage(source: ImageSource.gallery);
            if (pickedFile != null) {
                setState(() { _image = File(pickedFile.path);
            // Trigger the action to fetch recommendations based on the image

        fetchRecommendations(pickedFile.path);
           });
         }
       }

       // Take photo using camera
       Future<void> _takePhotoWithCamera()
       async {
         final pickedFile = await _picker.pickImage(source: ImageSource.camera);
         if (pickedFile != null) {
            setState(() {
              _image = File(pickedFile.path);
              // Trigger the action to fetch recommendations based on the image
              fetchRecommendations(pickedFile.path);
                  });
                }
              }
              @override
              Widget build(BuildContext context) {
              // Retrieve the current list of recommendations from the store
                final recommendations = _recommendationStore.recommendations;
                return Scaffold(
                    appBar: AppBar( title: Text('Garmentz'), backgroundColor: Colors.teal, ),
                    body: Padding(
                      padding: const
                    EdgeInsets.all(16.0),
                      child: Column(
                        mainAxisAlignment:MainAxisAlignment.center, children: [
                          Text( 'Scan your clothing to get recommendations.',
                            style: Theme.of(context).textTheme.headline6,
                            textAlign: TextAlign.center,
                ),
                SizedBox(height: 20),

                _image != null ?
                Image.file(_image!) : Container(),
                SizedBox(height: 20),
                ElevatedButton.icon( onPressed: _pickImageFromGallery,
                icon: Icon(Icons.image),
                label: Text('Pick your clothing from your gallery.'),
                style: ElevatedButton.styleFrom(
                  primary: Colors.teal,
                  padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                                    ),
                                  ),
                                ),
                                SizedBox(height: 10),
                                ElevatedButton.icon(
                                  onPressed:
                _takePhotoWithCamera,
                icon: Icon(Icons.camera_alt),
                label: Text('Take a Photo'),
                style: ElevatedButton.styleFrom(
                primary: Colors.teal,
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                shape:
                RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                                              ),
                                            ),
                                          ),
                                          SizedBox(height: 20),
                                          recommendations.isNotEmpty
                                          ? Expanded(
                                            child:
                ListView.builder(
                                              itemCount: recommendations.length,
                                              itemBuilder:

                                              (context, index) {
                                                final item =
                                                recommendations[index];
                                                return ClothingCard(
                                                  title: item['title']!,
                                                  imageUrl: item['imageUrl']!,
                                                  price: item['price']!,
                                                );
                                                },
                                              ),
                                            )
                                          : Container(), // Empty state when no recommendations
                                        ],
                                      ),
                                    ),
                                  );
                                }
                              }