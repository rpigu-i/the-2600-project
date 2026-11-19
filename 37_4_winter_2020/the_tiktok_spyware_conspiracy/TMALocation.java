public static TMALocation fromJson(JSONObject paramJSONObject) throws JSONException {
  if (paramJSONObject == null)
    return null;
  TMALocation tMALocation = new TMALocation(paramJSONObject.optString("provider"));
  tMALocation.setLatitude(paramJSONObject.optDouble("latitude"));
  tMALocation.setLongitude(paramJSONObject.optDouble("longitude"));
  tMALocation.setTime(paramJSONObject.optLong("loc_time"));
      tMALocation.setSpeed((float)paramJSONObject.optDouble("speed", 0.0D));
  tMALocation.setAccuracy((float)paramJSONObject.optDouble("accuracy"));
  tMALocation.setAltitude(paramJSONObject.optDouble("altitude"));
  tMALocation.setStatusCode(paramJSONObject.optInt("statusCode"));
  tMALocation.setRawImplStatusCode(paramJSONObject.optInt("rawImplStatusCode"));
  tMALocation.setAddress(paramJSONObject.optString("address"));
  tMALocation.setCountry(paramJSONObject.optString("country"));
  tMALocation.setProvince(paramJSONObject.optString("province"));
  tMALocation.setCity(paramJSONObject.optString("city"));
  tMALocation.setDistrict(paramJSONObject.optString("district"));
  tMALocation.setLocType(paramJSONObject.optInt("loctype"));
  if (Build.VERSION.SDK_INT >= 26)
    tMALocation.setVerticalAccuracyMeters(0.0F);
  return tMALocation;
 }


 // code code code it's too long to put it all

 public JSONObject toJson() {
  JSONObject jSONObject = new JSONObject();
  try {
    jSONObject.putOpt("provider", getProvider());
    jSONObject.putOpt("latitude", Double.valueOf(getLatitude()));
    jSONObject.putOpt("longitude", Double.valueOf(getLongitude()));
    jSONObject.putOpt("loc_time", Long.valueOf(getTime()));
    jSONObject.putOpt("speed", Float.valueOf(getSpeed()));
    jSONObject.putOpt("accuracy", Float.valueOf(getAccuracy()));
    jSONObject.putOpt("altitude", Double.valueOf(getAltitude()));
    jSONObject.putOpt("statusCode", Integer.valueOf(getStatusCode()));
    jSONObject.putOpt("rawImplStatusCode", Integer.valueOf(getRawImplStatusCode()));
    jSONObject.putOpt("address", getAddress());
    jSONObject.putOpt("country", getCountry());
    jSONObject.putOpt("province", getProvince());
    jSONObject.putOpt("city", getCity());
    jSONObject.putOpt("district", getDistrict());
    jSONObject.putOpt("loctype", Integer.valueOf(getLocType()));
    float f = 0.0F;
    if (Build.VERSION.SDK_INT >= 26)
      f = getVerticalAccuracyMeters();
    jSONObject.put("verticalAccuracy", f);
    return jSONObject;
  } catch (JSONException jSONException) {
    AppBrandLogger.eWithThrowable("TMALocation", "tojson", (Throwable)jSONException);
    return jSONObject;
  }
 }


