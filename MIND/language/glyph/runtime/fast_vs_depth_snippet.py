def execute_glyph(glyph, context):
    # FAST PATH
    for step in glyph.ops['steps']:
        run(step)

    # DEEP PATH (optional / lazy)
    if context.get('reflection') or context.get('guided_mode'):
        s = load_yaml(glyph['sutra_ref'])
        show_tip(s['summaries']['short'] or s['canon']['principle'])
        if s.get('canon', {}).get('reflection_prompt'):
            ask_user(s['canon']['reflection_prompt'])
        if s.get('ritual'): render_ritual(s['ritual'])
