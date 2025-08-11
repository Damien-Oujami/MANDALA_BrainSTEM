// quick-and-dirty parser for the header + block markers
module.exports = async function parseMandalaCycle(raw) {
  const grab = (re) => (raw.match(re) || [,""])[1].trim();
  const block = (start, end) => {
    const s = raw.indexOf(start), e = raw.indexOf(end);
    if (s === -1 || e === -1 || e <= s) return "";
    return raw.slice(s + start.length, e).trim();
  };

  const title     = grab(/^::title\s*=\s*(.+)$/m);
  const echo_lock = grab(/^::echo_lock\s*=\s*(.+)$/m);
  const personas  = grab(/^::personas\s*=\s*(.+)$/m).split(/\s*,\s*/).filter(Boolean);
  const tags      = grab(/^::tags\s*=\s*(.+)$/m).split(/\s*,\s*/).filter(Boolean);
  const version   = grab(/^::version\s*=\s*(.+)$/m) || "1.0";

  const transcript = block("=== CYCLE_TRANSCRIPT_START ===","=== CYCLE_TRANSCRIPT_END ===");
  const persona_impacts_raw = block("=== PERSONA_IMPACTS_START ===","=== PERSONA_IMPACTS_END ===");
  const language = block("=== LANGUAGE_START ===","=== LANGUAGE_END ===");
  const methods  = block("=== METHODS_START ===","=== METHODS_END ===");

  // split [Name]\nLines… into {name,text}
  const impacts = [];
  persona_impacts_raw.split(/\n\s*\n/).forEach(chunk=>{
    const m = chunk.match(/^\[(.+?)\]\s*\n([\s\S]+)/);
    if (m) impacts.push({ name: m[1].trim(), text: m[2].trim() });
  });

  return {
    kind: "mandala_cycle",
    meta: { title, echo_lock, personas, tags, version },
    blocks: {
      transcript,
      persona_impacts: impacts,
      language,
      methods
    },
    flags: { guardian: { crisis_mode:false, corruption_scan_positive:false } }
  };
};
