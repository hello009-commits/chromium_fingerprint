#include "third_party/blink/renderer/core/frame/fingerprint_controller.h"

#include "base/json/json_reader.h"
#include "base/values.h"
#include "third_party/blink/renderer/platform/wtf/text/wtf_string.h"

namespace blink {

std::unique_ptr<FingerprintController> FingerprintController::instance_;

FingerprintController* FingerprintController::GetInstance() {
  if (!instance_) {
    instance_ = std::make_unique<FingerprintController>();
  }
  return instance_.get();
}

void FingerprintController::Initialize(const String& config_json) {
  if (!config_json.IsEmpty()) {
    ParseConfig(config_json);
  }
}

void FingerprintController::ParseConfig(const String& config_json) {
  std::string json_string = config_json.Utf8();
  
  auto parsed_json = base::JSONReader::ReadAndReturnValueWithError(json_string);
  if (!parsed_json.has_value() || !parsed_json->is_dict()) {
    return;
  }
  
  const base::Value::Dict& config = parsed_json->GetDict();
  const base::Value::Dict* settings = config.FindDict("settings");
  if (!settings) {
    return;
  }
  
  // 解析语言配置
  const base::Value::Dict* language = settings->FindDict("language");
  if (language) {
    language_enabled_ = language->FindBool("enabled").value_or(false);
    if (language_enabled_) {
      const base::Value::Dict* params = language->FindDict("params");
      if (params) {
        const std::string* lang = params->FindString("language");
        if (lang) {
          custom_language_ = String::FromUTF8(*lang);
        }
        
        const base::Value::List* langs = params->FindList("languages");
        if (langs) {
          custom_languages_.clear();
          for (const auto& lang_value : *langs) {
            if (lang_value.is_string()) {
              custom_languages_.push_back(String::FromUTF8(lang_value.GetString()));
            }
          }
        }
      }
    }
  }
  
  // 解析时区配置
  const base::Value::Dict* timezone = settings->FindDict("timezone");
  if (timezone) {
    timezone_enabled_ = timezone->FindBool("enabled").value_or(false);
    if (timezone_enabled_) {
      const base::Value::Dict* params = timezone->FindDict("params");
      if (params) {
        const std::string* tz = params->FindString("timezone");
        if (tz) {
          custom_timezone_ = String::FromUTF8(*tz);
        }
      }
    }
  }
  
  // 解析地理位置配置
  const base::Value::Dict* geolocation = settings->FindDict("geolocation");
  if (geolocation) {
    geolocation_enabled_ = geolocation->FindBool("enabled").value_or(false);
    if (geolocation_enabled_) {
      const base::Value::Dict* params = geolocation->FindDict("params");
      if (params) {
        custom_latitude_ = params->FindDouble("latitude").value_or(0.0);
        custom_longitude_ = params->FindDouble("longitude").value_or(0.0);
        custom_accuracy_ = params->FindDouble("accuracy").value_or(100.0);
      }
    }
  }
  
  // 解析屏幕分辨率配置
  const base::Value::Dict* screen_resolution = settings->FindDict("screen_resolution");
  if (screen_resolution) {
    screen_resolution_enabled_ = screen_resolution->FindBool("enabled").value_or(false);
    if (screen_resolution_enabled_) {
      const base::Value::Dict* params = screen_resolution->FindDict("params");
      if (params) {
        custom_screen_width_ = params->FindInt("width").value_or(1920);
        custom_screen_height_ = params->FindInt("height").value_or(1080);
      }
    }
  }
  
  // 解析显示缩放配置
  const base::Value::Dict* display_zoom = settings->FindDict("display_zoom");
  if (display_zoom) {
    display_zoom_enabled_ = display_zoom->FindBool("enabled").value_or(false);
    if (display_zoom_enabled_) {
      const base::Value::Dict* params = display_zoom->FindDict("params");
      if (params) {
        custom_scale_factor_ = static_cast<float>(params->FindDouble("scale_factor").value_or(1.0));
      }
    }
  }
  
  // 解析可用屏幕尺寸配置
  const base::Value::Dict* screen_size = settings->FindDict("screen_size");
  if (screen_size) {
    screen_size_enabled_ = screen_size->FindBool("enabled").value_or(false);
    if (screen_size_enabled_) {
      const base::Value::Dict* params = screen_size->FindDict("params");
      if (params) {
        custom_available_width_ = params->FindInt("available_width").value_or(1880);
        custom_available_height_ = params->FindInt("available_height").value_or(1040);
      }
    }
  }
  
  // 解析颜色深度配置
  const base::Value::Dict* color_depth = settings->FindDict("color_depth");
  if (color_depth) {
    color_depth_enabled_ = color_depth->FindBool("enabled").value_or(false);
    if (color_depth_enabled_) {
      const base::Value::Dict* params = color_depth->FindDict("params");
      if (params) {
        custom_color_depth_ = params->FindInt("depth").value_or(24);
      }
    }
  }
  
  // 解析触控点配置
  const base::Value::Dict* touch_points = settings->FindDict("touch_points");
  if (touch_points) {
    touch_points_enabled_ = touch_points->FindBool("enabled").value_or(false);
    if (touch_points_enabled_) {
      const base::Value::Dict* params = touch_points->FindDict("params");
      if (params) {
        custom_max_touch_points_ = params->FindInt("max_touch_points").value_or(0);
      }
    }
  }
  
  // 解析Canvas配置
  const base::Value::Dict* canvas = settings->FindDict("canvas");
  if (canvas) {
    canvas_enabled_ = canvas->FindBool("enabled").value_or(false);
    if (canvas_enabled_) {
      const std::string* mode = canvas->FindString("mode");
      if (mode) {
        canvas_noise_mode_ = String::FromUTF8(*mode);
      }
      
      const base::Value::Dict* params = canvas->FindDict("params");
      if (params) {
        const std::string* seed = params->FindString("noise_seed");
        if (seed) {
          canvas_noise_seed_ = String::FromUTF8(*seed);
        }
        canvas_noise_level_ = static_cast<float>(params->FindDouble("noise_level").value_or(0.0));
      }
    }
  }
  
  // 解析Canvas字体配置
  const base::Value::Dict* canvas_font = settings->FindDict("canvas_font");
  if (canvas_font) {
    canvas_font_enabled_ = canvas_font->FindBool("enabled").value_or(false);
    if (canvas_font_enabled_) {
      const base::Value::Dict* params = canvas_font->FindDict("params");
      if (params) {
        const base::Value::List* fonts = params->FindList("protected_fonts");
        if (fonts) {
          protected_fonts_.clear();
          for (const auto& font_value : *fonts) {
            if (font_value.is_string()) {
              protected_fonts_.push_back(String::FromUTF8(font_value.GetString()));
            }
          }
        }
      }
    }
  }
  
  // 解析CSS字体配置
  const base::Value::Dict* css_font = settings->FindDict("css_font");
  if (css_font) {
    css_font_enabled_ = css_font->FindBool("enabled").value_or(false);
    if (css_font_enabled_) {
      const base::Value::Dict* params = css_font->FindDict("params");
      if (params) {
        css_font_noise_level_ = static_cast<float>(params->FindDouble("noise_level").value_or(0.0));
      }
    }
  }
  
  // 解析WebRTC配置
  const base::Value::Dict* webrtc = settings->FindDict("webrtc");
  if (webrtc) {
    webrtc_enabled_ = webrtc->FindBool("enabled").value_or(false);
    if (webrtc_enabled_) {
      const std::string* mode = webrtc->FindString("mode");
      if (mode) {
        webrtc_mode_ = String::FromUTF8(*mode);
      }
    }
  }
  
  // 解析WebGL配置
  const base::Value::Dict* webgl = settings->FindDict("webgl");
  if (webgl) {
    webgl_enabled_ = webgl->FindBool("enabled").value_or(false);
    if (webgl_enabled_) {
      const base::Value::Dict* params = webgl->FindDict("params");
      if (params) {
        const std::string* seed = params->FindString("noise_seed");
        if (seed) {
          webgl_noise_seed_ = String::FromUTF8(*seed);
        }
        webgl_noise_level_ = static_cast<float>(params->FindDouble("noise_level").value_or(0.0));
      }
    }
  }
  
  // 解析硬件并发数配置
  const base::Value::Dict* hardware_concurrency = settings->FindDict("hardware_concurrency");
  if (hardware_concurrency) {
    hardware_concurrency_enabled_ = hardware_concurrency->FindBool("enabled").value_or(false);
    if (hardware_concurrency_enabled_) {
      const base::Value::Dict* params = hardware_concurrency->FindDict("params");
      if (params) {
        custom_cores_ = params->FindInt("cores").value_or(8);
      }
    }
  }
  
  // 解析设备内存配置
  const base::Value::Dict* device_memory = settings->FindDict("device_memory");
  if (device_memory) {
    device_memory_enabled_ = device_memory->FindBool("enabled").value_or(false);
    if (device_memory_enabled_) {
      const base::Value::Dict* params = device_memory->FindDict("params");
      if (params) {
        custom_memory_gb_ = params->FindInt("memory_gb").value_or(8);
      }
    }
  }
  
  // 解析电池配置
  const base::Value::Dict* battery = settings->FindDict("battery");
  if (battery) {
    battery_enabled_ = battery->FindBool("enabled").value_or(false);
    if (battery_enabled_) {
      const base::Value::Dict* params = battery->FindDict("params");
      if (params) {
        battery_charging_ = params->FindBool("charging").value_or(true);
        battery_level_ = static_cast<float>(params->FindDouble("level").value_or(0.8));
      }
    }
  }
  
  // 解析User-Agent配置
  const base::Value::Dict* user_agent = settings->FindDict("user_agent");
  if (user_agent) {
    user_agent_enabled_ = user_agent->FindBool("enabled").value_or(false);
    if (user_agent_enabled_) {
      const base::Value::Dict* params = user_agent->FindDict("params");
      if (params) {
        const std::string* ua = params->FindString("user_agent");
        if (ua) {
          custom_user_agent_ = String::FromUTF8(*ua);
        }
      }
    }
  }
  
  // 解析其他功能开关
  const base::Value::Dict* port_scan_protection = settings->FindDict("port_scan_protection");
  if (port_scan_protection) {
    port_scan_protection_enabled_ = port_scan_protection->FindBool("enabled").value_or(false);
  }
  
  const base::Value::Dict* console_output = settings->FindDict("console_output");
  if (console_output) {
    const std::string* mode = console_output->FindString("mode");
    console_output_disabled_ = (mode && *mode == "disable");
  }
  
  const base::Value::Dict* do_not_track = settings->FindDict("do_not_track");
  if (do_not_track) {
    do_not_track_enabled_ = do_not_track->FindBool("enabled").value_or(false);
    if (do_not_track_enabled_) {
      const base::Value::Dict* params = do_not_track->FindDict("params");
      if (params) {
        const std::string* value = params->FindString("value");
        if (value) {
          do_not_track_value_ = String::FromUTF8(*value);
        }
      }
    }
  }
  
  const base::Value::Dict* webdriver_detection = settings->FindDict("webdriver_detection");
  if (webdriver_detection) {
    const std::string* mode = webdriver_detection->FindString("mode");
    webdriver_detection_disabled_ = (mode && *mode == "disable");
  }
  
  const base::Value::Dict* cdp_protection = settings->FindDict("cdp_protection");
  if (cdp_protection) {
    cdp_protection_enabled_ = cdp_protection->FindBool("enabled").value_or(false);
  }
}

}  // namespace blink