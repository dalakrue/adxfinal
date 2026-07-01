# Protected Hash Comparison

## Before

```text
4f45a5a8f43c9dc481713949ec332f064863e059b48f48c9e998a7446330df38  app.py
945473775a4d0b795603eef476ecb5c773e38e02fe1f1295c861e8a3a89cdf4e  core/one_hour_direction_confirmation_20260626.py
d72cd38ff7f9cefbc9a1ad5c738875cbb2b886143c381e810286d0f276802094  lunch/field_01/renderer.py
0705bf091f921399694158ba91c5fdc63e6f7497a44c8bc8146023076ec9be85  lunch/field_02/renderer.py
a4d3b001ce2b73a2c9008aa12f28146129ee217b794310dc6c0da291e480f75a  lunch/field_03/renderer.py
```

## After

```text
4f45a5a8f43c9dc481713949ec332f064863e059b48f48c9e998a7446330df38  app.py
6f689003ff3881fa32b62a1e88e37dd6ef23199692020350ee48bce173ae177b  core/one_hour_direction_confirmation_20260626.py
0bceab82f863f88dea7d1f839e0ba795fdb618b4e58b5eeccdce07a549a6bdbc  lunch/field_01/renderer.py
0705bf091f921399694158ba91c5fdc63e6f7497a44c8bc8146023076ec9be85  lunch/field_02/renderer.py
a4d3b001ce2b73a2c9008aa12f28146129ee217b794310dc6c0da291e480f75a  lunch/field_03/renderer.py
```

`app.py`, the Field 2 wrapper, and the Field 3 wrapper are unchanged. The Field 1 wrapper changed only to place the additive operational section before the protected history. No protected production calculation or raw Power BI central-path producer was edited.
