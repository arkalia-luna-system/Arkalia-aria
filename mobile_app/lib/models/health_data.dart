class HealthData {
  final String id;
  final DateTime timestamp;
  final String source;
  final double? heartRate;
  final double? bloodPressure;
  final double? bloodGlucose;
  final double? bodyTemperature;
  final double? weight;
  final double? height;
  final double? bmi;
  final Map<String, dynamic>? rawData;

  const HealthData({
    required this.id,
    required this.timestamp,
    required this.source,
    this.heartRate,
    this.bloodPressure,
    this.bloodGlucose,
    this.bodyTemperature,
    this.weight,
    this.height,
    this.bmi,
    this.rawData,
  });

  factory HealthData.fromJson(Map<String, dynamic> json) {
    return HealthData(
      id: json['id'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      source: json['source'] as String,
      heartRate: json['heart_rate'] as double?,
      bloodPressure: json['blood_pressure'] as double?,
      bloodGlucose: json['blood_glucose'] as double?,
      bodyTemperature: json['body_temperature'] as double?,
      weight: json['weight'] as double?,
      height: json['height'] as double?,
      bmi: json['bmi'] as double?,
      rawData: json['raw_data'] as Map<String, dynamic>?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'timestamp': timestamp.toIso8601String(),
      'source': source,
      'heart_rate': heartRate,
      'blood_pressure': bloodPressure,
      'blood_glucose': bloodGlucose,
      'body_temperature': bodyTemperature,
      'weight': weight,
      'height': height,
      'bmi': bmi,
      'raw_data': rawData,
    };
  }
}
