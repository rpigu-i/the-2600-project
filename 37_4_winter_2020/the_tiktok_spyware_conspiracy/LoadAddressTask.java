private void loadDistrictFromCity(JSONObject paramJSONObject) throws JSONException {
  if (paramJSONObject == null)
   return;
  ArrayList<AddressInfo> arrayList = new ArrayList();
  JSONArray jSONArray = paramJSONObject.getJSONArray("regionEntitys");
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.append(paramJSONObject.getString("region"));
  stringBuilder.append(paramJSONObject.getString("code"));
  stringBuilder.append("city");
  String str = stringBuilder.toString();
  for (int i = 0; i < jSONArray.length(); i++)
   arrayList.add(new AddressInfo(jSONArray.getJSONObject(i).getString("region"), jSONArray.getJSONObject(i).getString("code"), "district"));
  if (arrayList.size() <= 0) {
   arrayList.add(new AddressInfo(this.DEFAULT_DISTRICT_CHINA, "", "district"));
   mCache.put(str, arrayList);
   mDepthCache.put(str, Integer.valueOf(2));
   return;
  }
  mCache.put(str, arrayList);
  mDepthCache.put(str, Integer.valueOf(2));
 }

private List<AddressInfo> loadProvince(JSONArray paramJSONArray) throws JSONException {
  ArrayList<AddressInfo> arrayList = new ArrayList();
  for (int i = 0; i < paramJSONArray.length(); i++) {
   JSONObject jSONObject = paramJSONArray.getJSONObject(i);
   String str1 = jSONObject.getString("region");
   String str2 = jSONObject.getString("code");
   loadCityFromProvince(jSONObject);
   if (!arrayList.contains(str1))
     arrayList.add(new AddressInfo(str1, str2, "province"));
  }
  mCache.put("province", arrayList);
  mDepthCache.put("province", Integer.valueOf(0));
  return arrayList;
 }


