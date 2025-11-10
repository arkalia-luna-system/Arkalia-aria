import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/health_data.dart';

class OfflineCacheService {
  static const String _cacheKey = 'health_data_cache';
  
  Future<void> cacheHealthData(List<HealthData> data) async {
    final prefs = await SharedPreferences.getInstance();
    final jsonData = data.map((item) => item.toJson()).toList();
    await prefs.setString(_cacheKey, json.encode(jsonData));
  }
  
  Future<List<HealthData>> getCachedHealthData() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final cachedData = prefs.getString(_cacheKey);
      
      if (cachedData != null) {
        final List<dynamic> data = json.decode(cachedData);
        return data.map((json) => HealthData.fromJson(json)).toList();
      }
      
      return [];
    } catch (e) {
      return [];
    }
  }
  
  Future<void> clearCache() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_cacheKey);
  }
}
