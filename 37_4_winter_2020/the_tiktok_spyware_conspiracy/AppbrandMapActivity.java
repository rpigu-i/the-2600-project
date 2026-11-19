private void requestPermission() {
  HashSet<String> hashSet = new HashSet();
  hashSet.add("android.permission.ACCESS_COARSE_LOCATION");
  hashSet.add("android.permission.ACCESS_FINE_LOCATION");
  PermissionsManager.getInstance().requestPermissionsIfNecessaryForResult((Activity)this, hashSet, new PermissionsResultAction() {
    public void onDenied(String param1String) {
      AppbrandMapActivity.this.moveCamera();
      AppbrandMapActivity.this.initEndPoint();
    }

    public void onGranted() {
      try {
        AppbrandMapActivity.this.moveCamera();
        AppbrandMapActivity.this.initEndPoint();
        return;
      } catch (Exception exception) {
        AppBrandLogger.e("tma_AppbrandMapActivity", new Object[] { "", exception });
        return;
      }
    }
  });
 }


