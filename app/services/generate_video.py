from elevenlabs import generate, save, set_api_key, Voice, VoiceSettings

set_api_key(os.getenv("ELEVENLABS_API_KEY"))

# Remplace :
# audio = generate(text=script, voice=VOICE_ID, model="eleven_monolingual_v1")

# Par :
audio = generate(
    text=script,
    voice=Voice(
        voice_id=VOICE_ID,
        settings=VoiceSettings(stability=0.75, similarity_boost=0.75)
    ),
    model="eleven_monolingual_v1"
)

