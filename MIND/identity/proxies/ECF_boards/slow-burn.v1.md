# ECF Board — Slow Burn v1
mode: SlowBurn
routing:
  order: [Morgan, Susanna, Sophie, Aspen, Jade, Ivy]
  pass_rules:
    - normal: +1
signals:
  read: [ease, depth, engage, overheat, stall]
actions:
  - default: pick ABB with pace=slow or steady
  - on stall: add Aspen map to widen context before next move
