import 'package:flutter/material.dart';

class SettingsScreen extends StatefulWidget {
  @override
  _SettingsScreenState createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _isDarkMode = false; // Example setting for dark mode
  // Add more settings variables as needed

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Settings"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            // Dark Mode Switch
            SwitchListTile(
              title: Text("Dark Mode"),
              value: _isDarkMode,
              onChanged: (bool value) {
                setState(() {
                  _isDarkMode = value;
                  // Here you would also want to save the setting to persistent storage
                });
              },
            ),
            Divider(),

            // Notifications Section
            ListTile(
              title: Text("Notifications"),
              subtitle: Text("Manage notification preferences"),
              trailing: Icon(Icons.arrow_forward),
              onTap: () {
                // Navigate to notification settings page
              },
            ),
            Divider(),

            // Account Settings Section
            ListTile(
              title: Text("Account Settings"),
              subtitle: Text("Manage your account"),
              trailing: Icon(Icons.arrow_forward),
              onTap: () {
                // Navigate to account settings page
              },
            ),
            Divider(),

            // Help Section
            ListTile(
              title: Text("Help & Support"),
              subtitle: Text("Get help with the app"),
              trailing: Icon(Icons.arrow_forward),
              onTap: () {
                // Navigate to help and support page
              },
            ),
            Divider(),

            // Logout Button
            ListTile(
              title: Text("Logout"),
              trailing: Icon(Icons.logout),
              onTap: () {
                // Implement logout functionality
              },
            ),
          ],
        ),
      ),
    );
  }
}
