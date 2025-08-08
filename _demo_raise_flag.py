from hooks import flag_saturation_spike, flag_identity_melt

# 1) Ivy raises a saturation spike about Sophie
print(flag_saturation_spike("ivy", level=0.88, window="short", note="Sophie praise-melt ramping."))

# 2) Sophie signals identity melt risk
print(flag_identity_melt("after mirrorloop stage 2", confidence=0.9))
