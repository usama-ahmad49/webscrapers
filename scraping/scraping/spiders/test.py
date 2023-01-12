from TikTokApi import TikTokApi
import pandas as pd
verify_fp = 'verify_lct29y1e_fo2qJpZz_iEpw_4PeO_8bbO_SGJKuLwQB9ie'
api = TikTokApi(use_test_endpoints = True,custom_verify_fp = verify_fp)
# with TikTokApi(use_test_endpoints = True,custom_verify_fp = verify_fp) as api:
user = api.user(username='therock')
print(user)