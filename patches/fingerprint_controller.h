#ifndef THIRD_PARTY_BLINK_RENDERER_CORE_FRAME_FINGERPRINT_CONTROLLER_H_
#define THIRD_PARTY_BLINK_RENDERER_CORE_FRAME_FINGERPRINT_CONTROLLER_H_

#include "third_party/blink/renderer/platform/wtf/text/wtf_string.h"
#include "third_party/blink/renderer/platform/wtf/vector.h"
#include <memory>

namespace blink {

// 指纹控制器 - 统一管理所有指纹修改
class FingerprintController {
 public:
  static FingerprintController* GetInstance();
  
  // 初始化指纹配置
  void Initialize(const String& config_json);
  
  // 语言相关
  bool IsLanguageEnabled() const { return language_enabled_; }
  String GetCustomLanguage() const { return custom_language_; }
  const Vector<String>& GetCustomLanguages() const { return custom_languages_; }
  
  // 时区相关
  bool IsTimezoneEnabled() const { return timezone_enabled_; }
  String GetCustomTimezone() const { return custom_timezone_; }
  
  // 地理位置相关
  bool IsGeolocationEnabled() const { return geolocation_enabled_; }
  double GetCustomLatitude() const { return custom_latitude_; }
  double GetCustomLongitude() const { return custom_longitude_; }
  double GetCustomAccuracy() const { return custom_accuracy_; }
  
  // 屏幕相关
  bool IsScreenResolutionEnabled() const { return screen_resolution_enabled_; }
  int GetCustomScreenWidth() const { return custom_screen_width_; }
  int GetCustomScreenHeight() const { return custom_screen_height_; }
  
  bool IsDisplayZoomEnabled() const { return display_zoom_enabled_; }
  float GetCustomScaleFactor() const { return custom_scale_factor_; }
  
  bool IsScreenSizeEnabled() const { return screen_size_enabled_; }
  int GetCustomAvailableWidth() const { return custom_available_width_; }
  int GetCustomAvailableHeight() const { return custom_available_height_; }
  
  bool IsColorDepthEnabled() const { return color_depth_enabled_; }
  int GetCustomColorDepth() const { return custom_color_depth_; }
  
  bool IsTouchPointsEnabled() const { return touch_points_enabled_; }
  int GetCustomMaxTouchPoints() const { return custom_max_touch_points_; }
  
  // Canvas相关
  bool IsCanvasEnabled() const { return canvas_enabled_; }
  String GetCanvasNoiseMode() const { return canvas_noise_mode_; }
  String GetCanvasNoiseSeed() const { return canvas_noise_seed_; }
  float GetCanvasNoiseLevel() const { return canvas_noise_level_; }
  
  bool IsCanvasFontEnabled() const { return canvas_font_enabled_; }
  const Vector<String>& GetProtectedFonts() const { return protected_fonts_; }
  
  bool IsCssFontEnabled() const { return css_font_enabled_; }
  float GetCssFontNoiseLevel() const { return css_font_noise_level_; }
  
  // WebRTC相关
  bool IsWebRtcEnabled() const { return webrtc_enabled_; }
  String GetWebRtcMode() const { return webrtc_mode_; }
  
  // WebGL相关
  bool IsWebGlEnabled() const { return webgl_enabled_; }
  String GetWebGlNoiseSeed() const { return webgl_noise_seed_; }
  float GetWebGlNoiseLevel() const { return webgl_noise_level_; }
  
  // 硬件相关
  bool IsHardwareConcurrencyEnabled() const { return hardware_concurrency_enabled_; }
  int GetCustomCores() const { return custom_cores_; }
  
  bool IsDeviceMemoryEnabled() const { return device_memory_enabled_; }
  int GetCustomMemoryGB() const { return custom_memory_gb_; }
  
  // 电池相关
  bool IsBatteryEnabled() const { return battery_enabled_; }
  bool GetBatteryCharging() const { return battery_charging_; }
  float GetBatteryLevel() const { return battery_level_; }
  
  // User-Agent相关
  bool IsUserAgentEnabled() const { return user_agent_enabled_; }
  String GetCustomUserAgent() const { return custom_user_agent_; }
  
  // 其他功能开关
  bool IsPortScanProtectionEnabled() const { return port_scan_protection_enabled_; }
  bool IsConsoleOutputDisabled() const { return console_output_disabled_; }
  bool IsDoNotTrackEnabled() const { return do_not_track_enabled_; }
  String GetDoNotTrackValue() const { return do_not_track_value_; }
  bool IsWebDriverDetectionDisabled() const { return webdriver_detection_disabled_; }
  bool IsCdpProtectionEnabled() const { return cdp_protection_enabled_; }
  
 private:
  FingerprintController() = default;
  ~FingerprintController() = default;
  
  // 解析JSON配置
  void ParseConfig(const String& config_json);
  
  // 语言配置
  bool language_enabled_ = false;
  String custom_language_;
  Vector<String> custom_languages_;
  
  // 时区配置
  bool timezone_enabled_ = false;
  String custom_timezone_;
  
  // 地理位置配置
  bool geolocation_enabled_ = false;
  double custom_latitude_ = 0.0;
  double custom_longitude_ = 0.0;
  double custom_accuracy_ = 100.0;
  
  // 屏幕配置
  bool screen_resolution_enabled_ = false;
  int custom_screen_width_ = 1920;
  int custom_screen_height_ = 1080;
  
  bool display_zoom_enabled_ = false;
  float custom_scale_factor_ = 1.0f;
  
  bool screen_size_enabled_ = false;
  int custom_available_width_ = 1880;
  int custom_available_height_ = 1040;
  
  bool color_depth_enabled_ = false;
  int custom_color_depth_ = 24;
  
  bool touch_points_enabled_ = false;
  int custom_max_touch_points_ = 0;
  
  // Canvas配置
  bool canvas_enabled_ = false;
  String canvas_noise_mode_;
  String canvas_noise_seed_;
  float canvas_noise_level_ = 0.0f;
  
  bool canvas_font_enabled_ = false;
  Vector<String> protected_fonts_;
  
  bool css_font_enabled_ = false;
  float css_font_noise_level_ = 0.0f;
  
  // WebRTC配置
  bool webrtc_enabled_ = false;
  String webrtc_mode_;
  
  // WebGL配置
  bool webgl_enabled_ = false;
  String webgl_noise_seed_;
  float webgl_noise_level_ = 0.0f;
  
  // 硬件配置
  bool hardware_concurrency_enabled_ = false;
  int custom_cores_ = 8;
  
  bool device_memory_enabled_ = false;
  int custom_memory_gb_ = 8;
  
  // 电池配置
  bool battery_enabled_ = false;
  bool battery_charging_ = true;
  float battery_level_ = 0.8f;
  
  // User-Agent配置
  bool user_agent_enabled_ = false;
  String custom_user_agent_;
  
  // 其他功能开关
  bool port_scan_protection_enabled_ = false;
  bool console_output_disabled_ = false;
  bool do_not_track_enabled_ = false;
  String do_not_track_value_;
  bool webdriver_detection_disabled_ = false;
  bool cdp_protection_enabled_ = false;
  
  static std::unique_ptr<FingerprintController> instance_;
};

}  // namespace blink

#endif  // THIRD_PARTY_BLINK_RENDERER_CORE_FRAME_FINGERPRINT_CONTROLLER_H_