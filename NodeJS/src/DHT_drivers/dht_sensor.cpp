#include <node.h>
#include "pi_2_dht_read.h"
#include "pi_dht_read.h"
#include "bbb_dht_read.h"

namespace dht {

  using v8::FunctionCallbackInfo;
  using v8::Isolate;
  using v8::Local;
  using v8::Object;
  using v8::String;
  using v8::Value;
  using v8::Number;
  using v8::Exception;

  void Method(const FunctionCallbackInfo<Value>& args) {
    Isolate* isolate = args.GetIsolate();

    int platform = args[0]->IntegerValue();
    int sensor = args[1]->IntegerValue();
    int pin = args[2]->IntegerValue();
    int gpio_number = args[3]->IntegerValue();

    float humidity;
    float temperature;

    int errorCode = 0;
    if (platform == 0) {
      // pin is gpio_base in this case
      errorCode = bbb_dht_read(sensor, pin, gpio_number, &humidity, &temperature);
    } else if (platform == 1) {
      errorCode = pi_dht_read(sensor, pin, &humidity, &temperature);
    } else if (platform == 2) {
      errorCode = pi_2_dht_read(sensor, pin, &humidity, &temperature);
    }

    if (errorCode == DHT_ERROR_GPIO) {
      isolate->ThrowException(Exception::TypeError(String::NewFromUtf8(isolate, "Error accessing GPIO.")));
      return;
    }
    else if (errorCode != DHT_SUCCESS) {
      isolate->ThrowException(Exception::TypeError(String::NewFromUtf8(isolate, "Could not read data from DHT sensor.")));
      return;
    }

    Local<Object> obj = Object::New(isolate);
    obj->Set(String::NewFromUtf8(isolate, "humidity"), Number::New(isolate, humidity));
    obj->Set(String::NewFromUtf8(isolate, "temperature"), Number::New(isolate, temperature));
    args.GetReturnValue().Set(obj);
  }

  void init(Local<Object> exports) {
    NODE_SET_METHOD(exports, "read", Method);
  }

  NODE_MODULE(addon, init)

}  // namespace demo
