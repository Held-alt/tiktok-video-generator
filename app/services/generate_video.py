import os
import openai
import replicate
from elevenlabs import generate, save, set_api_key
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
import uuid

openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Voix féminine anglaise

def generate_video(question):
    uid = str(uuid.uuid4())[:8]

    # 1. Génération du script
    script_prompt = f"Write a short educational TikTok script (max 100 words) answering: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": script_prompt}],
        max_tokens=300
    )
    script = response.choices[0].message.content.strip()

    # 2. Voix off
    audio = generate(
        text=script,
        voice=VOICE_ID,
        model="eleven_monolingual_v1"
    )
    audio_path = f"output/audio_{uid}.mp3"
    save(audio, audio_path)

    # 3. Vidéo de fond
    output = replicate.run(
        "cjwbw/video-to-video:db21e45b7c1403e7d68fdbd81c45e77256e1b4fef5816a21fe1fcd6d7506e3b1",
        input={
            "prompt": question,
            "fps": 24,
            "num_frames": 100
        }
    )
    background_url = output[0]
    background_path = f"output/bg_{uid}.mp4"
    os.system(f"wget {background_url} -O {background_path}")

    # 4. Montage
    audio_clip = AudioFileClip(audio_path)
    text_clip = TextClip(script, fontsize=48, color='white', size=(1080, 1920), method='caption')
    text_clip = text_clip.set_duration(audio_clip.duration).set_position('center')
    background_clip = AudioFileClip(background_path).set_duration(audio_clip.duration)
    final_clip = CompositeVideoClip([background_clip, text_clip.set_audio(audio_clip)])

    final_path = f"output/final_{uid}.mp4"
    final_clip.write_videofile(final_path, fps=24)

    return {"status": "success", "video_path": final_path, "script": script}
