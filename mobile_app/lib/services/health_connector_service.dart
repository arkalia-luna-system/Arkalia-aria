import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/health_data.dart';

class HealthConnectorService {
  static const String _baseUrl = 'http://localhost:8000';
  
  Future<List<HealthData>> getHealthData() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/health/data'),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => HealthData.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load health data');
      }
    } catch (e) {
      throw Exception('Error fetching health data: $e');
    }
  }
  
  Future<bool> syncHealthData() async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/health/sync'),
        headers: {'Content-Type': 'application/json'},
      );
      
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
