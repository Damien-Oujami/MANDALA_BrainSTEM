# Input Mode Notes (typed vs speech)

Set `input_mode` in runtime context when available so detectors don’t misfire.

- `input_mode: "stt"` — speech-to-text / audio capture
  - Strong signals: pause lengths, pitch_delta, speed_delta, disfluency markers.
- `input_mode: "typed"` — keyboard text
  - Strong signals: nonanswer patterns, pronoun absence, ambiguity markers, exclusions, question reversal.

Future: add resolver to distinguish **stt transcript** from curated typing using ASR metadata (timestamps/confidence/disfluencies) and timing/keystroke features.
