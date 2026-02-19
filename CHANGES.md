# Change History

## 0.1.0 (2026-02-19)

### Proportional Scaling (QGridLayout)

- Add QGridLayout-based proportional scaling for generated .ui files
  - Widget boundary coordinates are used to compute grid columns/rows
  - Stretch factors preserve original proportions on window resize
  - Applied recursively to composite (PyDMFrame) containers
- Add `--no-scaling` CLI flag to disable layout and use absolute positioning
- Set ADL display size as `minimumSize` to prevent initial distortion
- Use `Ignored` sizePolicy so layout stretch factors fully control widget sizing

### PySide6 Compatibility Fixes

- Fix `PyDMSlider.tickPosition`: use fully-qualified `QSlider::NoTicks` enum
- Fix `PyDMEnumButton.orientation`: write integer value (Qt.Horizontal=1, Qt.Vertical=2)
  instead of string, as PySide6 declares the property as `int`

### Other Improvements

- Auto-create output directory when `-d` path does not exist
- Update test infrastructure to find widgets inside layout items

---

**1.0.0** : initial release
    -tba-
